from __future__ import annotations
from django.core.management.base import BaseCommand, CommandParser
from django.db import transaction
from core.import_utils import read_csv, ImportResult, pick
from core.models import Composicao, EtapaConstrutiva

class Command(BaseCommand):
    help = "Importa Composições (codigo, nome, etapa)."

    def add_arguments(self, parser: CommandParser) -> None:
        parser.add_argument("csv_path")
        parser.add_argument("--encoding", default="utf-8")
        parser.add_argument("--dry-run", action="store_true")

    @transaction.atomic
    def handle(self, csv_path: str, encoding: str, dry_run: bool, **_):
        res = ImportResult()
        for row in read_csv(csv_path, encoding=encoding):
            codigo = pick(row, "codigo")
            nome   = pick(row, "nome")
            etapa  = (pick(row, "etapa") or "").strip().lower()

            if not (codigo and nome and etapa):
                res.skipped += 1; res.errors.append(f"Composição incompleta: {row}"); continue
            if etapa not in EtapaConstrutiva.values:
                res.skipped += 1; res.errors.append(f"Etapa inválida '{etapa}' para {codigo}"); continue

            obj = Composicao.objects.filter(codigo=codigo).first()
            if obj:
                obj.nome = nome
                obj.etapa = etapa
                if not dry_run: obj.save(update_fields=["nome", "etapa"])
                res.updated += 1
            else:
                if not dry_run: Composicao.objects.create(codigo=codigo, nome=nome, etapa=etapa)
                res.created += 1

        if dry_run: self.stdout.write(self.style.WARNING("Dry-run: nenhuma escrita aplicada."))
        self.stdout.write(self.style.SUCCESS(f"Composições => criados:{res.created} atualizados:{res.updated} pulados:{res.skipped}"))
        for e in res.errors: self.stdout.write(self.style.NOTICE(f"- {e}"))
