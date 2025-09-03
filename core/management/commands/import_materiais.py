from __future__ import annotations
from decimal import Decimal
from django.core.management.base import BaseCommand, CommandParser
from django.db import transaction
from core.import_utils import read_csv, ImportResult, pick, to_decimal, norm_unit
from core.models import Material

class Command(BaseCommand):
    help = "Importa Materiais (campos exatamente como no modelo)."

    def add_arguments(self, parser: CommandParser) -> None:
        parser.add_argument("csv_path")
        parser.add_argument("--encoding", default="utf-8")
        parser.add_argument("--delimiter", default=None)  # auto-detect por padrão
        parser.add_argument("--dry-run", action="store_true")

    @transaction.atomic
    def handle(self, csv_path: str, encoding: str, delimiter: str | None, dry_run: bool, **_):
        res = ImportResult()
        for row in read_csv(csv_path, delimiter=delimiter, encoding=encoding):
            nome = pick(row, "nome")
            if not nome:
                res.skipped += 1; res.errors.append(f"Material sem nome: {row}"); continue

            unidade = norm_unit(pick(row, "unidade_base")) or "kg"
            dens = to_decimal(pick(row, "densidade_kg_m3"))
            ee_un  = to_decimal(pick(row, "energia_MJ_por_un"))
            co2_un = to_decimal(pick(row, "co2e_kg_por_un"))
            ee_kg  = to_decimal(pick(row, "energia_MJ_por_kg"))
            co2_kg = to_decimal(pick(row, "co2e_kg_por_kg"))

            obj = Material.objects.filter(nome=nome).first()
            fields = dict(unidade_base=unidade)
            if dens  is not None: fields["densidade_kg_m3"]   = dens
            if ee_un is not None: fields["energia_MJ_por_un"] = ee_un
            if co2_un is not None: fields["co2e_kg_por_un"]   = co2_un
            if ee_kg is not None: fields["energia_MJ_por_kg"] = ee_kg
            if co2_kg is not None: fields["co2e_kg_por_kg"]   = co2_kg

            if obj:
                for k, v in fields.items(): setattr(obj, k, v)
                if not dry_run: obj.save(update_fields=list(fields.keys()))
                res.updated += 1
            else:
                if not dry_run: Material.objects.create(nome=nome, **fields)
                res.created += 1

        if dry_run: self.stdout.write(self.style.WARNING("Dry-run: nenhuma escrita aplicada."))
        self.stdout.write(self.style.SUCCESS(f"Materiais => criados:{res.created} atualizados:{res.updated} pulados:{res.skipped}"))
        for e in res.errors: self.stdout.write(self.style.NOTICE(f"- {e}"))
