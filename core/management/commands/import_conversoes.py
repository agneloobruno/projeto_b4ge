from __future__ import annotations
from django.core.management.base import BaseCommand, CommandParser
from django.db import transaction
from core.import_utils import read_csv, ImportResult, pick, to_decimal, norm_unit
from core.models import ConversaoMaterial, Material

class Command(BaseCommand):
    help = "Importa Conversões (m²/un/m³ → kg) por material."

    def add_arguments(self, parser: CommandParser) -> None:
        parser.add_argument("csv_path")
        parser.add_argument("--encoding", default="utf-8")
        parser.add_argument("--dry-run", action="store_true")

    @transaction.atomic
    def handle(self, csv_path: str, encoding: str, dry_run: bool, **_):
        res = ImportResult()
        for row in read_csv(csv_path, encoding=encoding):
            mat_nome = pick(row, "material_nome")
            if not mat_nome:
                res.skipped += 1; res.errors.append(f"Linha sem material_nome: {row}"); continue
            mat = Material.objects.filter(nome=mat_nome).first()
            if not mat:
                res.skipped += 1; res.errors.append(f"Material não encontrado: {mat_nome}"); continue

            origem  = norm_unit(pick(row, "origem_unidade"))
            destino = norm_unit(pick(row, "destino_unidade")) or "kg"
            esp = to_decimal(pick(row, "espessura_m"))
            fator = to_decimal(pick(row, "fator_massa_kg_por_origem"))

            if not (origem and fator is not None):
                res.skipped += 1; res.errors.append(f"Conversão incompleta: {row}"); continue

            obj = ConversaoMaterial.objects.filter(
                material=mat, origem_unidade=origem, destino_unidade=destino, espessura_m=esp
            ).first()

            fields = dict(fator_massa_kg_por_origem=fator)
            if obj:
                obj.fator_massa_kg_por_origem = fator
                if not dry_run: obj.save(update_fields=["fator_massa_kg_por_origem"])
                res.updated += 1
            else:
                if not dry_run:
                    ConversaoMaterial.objects.create(
                        material=mat,
                        origem_unidade=origem,
                        destino_unidade=destino,
                        espessura_m=esp,
                        **fields,
                    )
                res.created += 1

        if dry_run: self.stdout.write(self.style.WARNING("Dry-run: nenhuma escrita aplicada."))
        self.stdout.write(self.style.SUCCESS(f"Conversões => criados:{res.created} atualizados:{res.updated} pulados:{res.skipped}"))
        for e in res.errors: self.stdout.write(self.style.NOTICE(f"- {e}"))
