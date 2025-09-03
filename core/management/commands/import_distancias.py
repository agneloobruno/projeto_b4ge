from __future__ import annotations
from django.core.management.base import BaseCommand, CommandParser
from django.db import transaction
from core.import_utils import read_csv, ImportResult, pick, to_decimal
from core.models import DistanciaInsumoCidade, Cidade, Material

class Command(BaseCommand):
    help = "Importa Distâncias por Cidade/Material (km)."

    def add_arguments(self, parser: CommandParser) -> None:
        parser.add_argument("csv_path")
        parser.add_argument("--encoding", default="utf-8")
        parser.add_argument("--dry-run", action="store_true")

    @transaction.atomic
    def handle(self, csv_path: str, encoding: str, dry_run: bool, **_):
        res = ImportResult()
        for row in read_csv(csv_path, encoding=encoding):
            cidade_nome = pick(row, "cidade_nome")
            mat_nome    = pick(row, "material_nome")
            dist        = to_decimal(pick(row, "distancia_km"))

            if not (cidade_nome and mat_nome and dist is not None):
                res.skipped += 1; res.errors.append(f"Linha incompleta: {row}"); continue

            cidade = Cidade.objects.filter(nome__iexact=cidade_nome).first()
            mat    = Material.objects.filter(nome=mat_nome).first()
            if not (cidade and mat):
                res.skipped += 1; res.errors.append(f"Cidade/Material não encontrados: {cidade_nome}/{mat_nome}"); continue

            obj = DistanciaInsumoCidade.objects.filter(cidade=cidade, material=mat).first()
            if obj:
                obj.distancia_km = dist
                if not dry_run: obj.save(update_fields=["distancia_km"])
                res.updated += 1
            else:
                if not dry_run: DistanciaInsumoCidade.objects.create(cidade=cidade, material=mat, distancia_km=dist)
                res.created += 1

        if dry_run: self.stdout.write(self.style.WARNING("Dry-run: nenhuma escrita aplicada."))
        self.stdout.write(self.style.SUCCESS(f"Distâncias => criados:{res.created} atualizados:{res.updated} pulados:{res.skipped}"))
        for e in res.errors: self.stdout.write(self.style.NOTICE(f"- {e}"))
