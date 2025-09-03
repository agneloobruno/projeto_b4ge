from __future__ import annotations
from decimal import Decimal
from django.core.management.base import BaseCommand, CommandParser
from django.db import transaction
from core.import_utils import read_csv, ImportResult, pick, to_decimal, norm_unit
from core.models import ItemDeComposicao, Composicao, Material

class Command(BaseCommand):
    help = "Importa Itens de Composição (material + quantidade + unidade + desperdício)."

    def add_arguments(self, parser: CommandParser) -> None:
        parser.add_argument("csv_path")
        parser.add_argument("--encoding", default="utf-8")
        parser.add_argument("--dry-run", action="store_true")

    @transaction.atomic
    def handle(self, csv_path: str, encoding: str, dry_run: bool, **_):
        res = ImportResult()
        pending = []

        for row in read_csv(csv_path, encoding=encoding):
            cod = pick(row, "composicao_codigo")
            mat_nome = pick(row, "material_nome")
            if not (cod and mat_nome):
                res.skipped += 1; res.errors.append(f"Linha sem comp/material: {row}"); continue

            comp = Composicao.objects.filter(codigo=cod).first()
            mat  = Material.objects.filter(nome=mat_nome).first()
            if not (comp and mat):
                res.skipped += 1; res.errors.append(f"Comp/Mat não encontrados: {cod}/{mat_nome}"); continue

            un  = norm_unit(pick(row, "unidade_medida")) or "un"
            qtd = to_decimal(pick(row, "quantidade"), Decimal("0"))
            if qtd is None: qtd = Decimal("0")
            desp = to_decimal(pick(row, "desperdicio_pct"), Decimal("0")) or Decimal("0")

            obj = ItemDeComposicao.objects.filter(
                composicao=comp, material=mat, unidade_medida=un
            ).first()

            if obj:
                obj.quantidade = qtd
                obj.desperdicio_pct = desp
                if not dry_run: obj.save(update_fields=["quantidade", "desperdicio_pct"])
                res.updated += 1
            else:
                data = dict(composicao=comp, material=mat, unidade_medida=un,
                            quantidade=qtd, desperdicio_pct=desp)
                if dry_run:
                    res.created += 1
                else:
                    pending.append(ItemDeComposicao(**data))

        if pending:
            ItemDeComposicao.objects.bulk_create(pending, ignore_conflicts=True)
            res.created += len(pending)

        if dry_run: self.stdout.write(self.style.WARNING("Dry-run: nenhuma escrita aplicada."))
        self.stdout.write(self.style.SUCCESS(f"Itens => criados:{res.created} atualizados:{res.updated} pulados:{res.skipped}"))
        for e in res.errors: self.stdout.write(self.style.NOTICE(f"- {e}"))
