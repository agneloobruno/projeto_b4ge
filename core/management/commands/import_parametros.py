from __future__ import annotations
from django.core.management.base import BaseCommand, CommandParser
from django.db import transaction
from core.import_utils import read_csv, ImportResult, pick, to_decimal
from core.models import ParametrosOperacionais, FatorTransporte, Desperdicio, EtapaConstrutiva

PARAM_FIELDS = [
    "fator_kcal_por_hora_pessoa",
    "pessoas_por_equipe",
    "horas_por_dia",
    "fator_kgCO2e_por_GJ",
    "fator_kgCO2e_eletricidade_por_GJ",
]

class Command(BaseCommand):
    help = "Importa ParametrosOperacionais / FatorTransporte / Desperdicio via coluna 'tipo'."

    def add_arguments(self, parser: CommandParser) -> None:
        parser.add_argument("csv_path")
        parser.add_argument("--encoding", default="utf-8")
        parser.add_argument("--dry-run", action="store_true")

    @transaction.atomic
    def handle(self, csv_path: str, encoding: str, dry_run: bool, **_):
        res = ImportResult()
        for row in read_csv(csv_path, encoding=encoding):
            tipo = (pick(row, "tipo") or "").strip().lower()

            # -------- parametros --------
            if tipo == "param":
                nome = pick(row, "nome") or "padrão"
                obj, created = ParametrosOperacionais.objects.get_or_create(nome=nome)
                updated_fields = []
                # numéricos (aceita faltar alguns)
                for f in PARAM_FIELDS:
                    raw = pick(row, f)
                    if raw is not None and raw != "":
                        val = to_decimal(raw)
                        # pessoas_por_equipe é int
                        if f == "pessoas_por_equipe" and val is not None:
                            try:
                                ival = int(val)
                            except Exception:
                                continue
                            if obj.pessoas_por_equipe != ival:
                                obj.pessoas_por_equipe = ival
                                updated_fields.append("pessoas_por_equipe")
                        elif val is not None and getattr(obj, f) != val:
                            setattr(obj, f, val)
                            updated_fields.append(f)
                if not dry_run and updated_fields:
                    obj.save(update_fields=updated_fields)
                res.created += 1 if created else 0
                res.updated += 0 if created else 1

            # -------- fator_transp --------
            elif tipo == "fator_transp":
                nome = pick(row, "nome") or "padrão"
                ee  = to_decimal(pick(row, "energia_MJ_por_t_km"))
                co2 = to_decimal(pick(row, "co2e_kg_por_t_km"))
                obj, created = FatorTransporte.objects.get_or_create(nome=nome,
                    defaults=dict(
                        energia_MJ_por_t_km=ee or 0,
                        co2e_kg_por_t_km=co2 or 0
                    )
                )
                if not created:
                    changed = []
                    if ee is not None and obj.energia_MJ_por_t_km != ee:
                        obj.energia_MJ_por_t_km = ee; changed.append("energia_MJ_por_t_km")
                    if co2 is not None and obj.co2e_kg_por_t_km != co2:
                        obj.co2e_kg_por_t_km = co2; changed.append("co2e_kg_por_t_km")
                    if not dry_run and changed: obj.save(update_fields=changed)
                    res.updated += 1
                else:
                    if dry_run: obj.delete()
                    else: res.created += 1

            # -------- desperdicio --------
            elif tipo == "desperdicio":
                nome = pick(row, "nome")
                if not nome:
                    res.skipped += 1; res.errors.append(f"Desperdicio sem nome: {row}"); continue
                pct = to_decimal(pick(row, "percentual"), Decimal("0"))
                etapa = (pick(row, "etapa") or "").strip().lower() or None
                if etapa and etapa not in EtapaConstrutiva.values:
                    res.skipped += 1; res.errors.append(f"Etapa inválida '{etapa}' em desperdício {nome}"); continue

                obj, created = Desperdicio.objects.get_or_create(nome=nome,
                    defaults=dict(percentual=pct or 0, etapa=etapa))
                if not created:
                    changed = []
                    if pct is not None and obj.percentual != pct:
                        obj.percentual = pct; changed.append("percentual")
                    if obj.etapa != etapa:
                        obj.etapa = etapa; changed.append("etapa")
                    if not dry_run and changed: obj.save(update_fields=changed)
                    res.updated += 1
                else:
                    if dry_run: obj.delete()
                    else: res.created += 1

            else:
                res.skipped += 1
                res.errors.append(f"Tipo desconhecido: {tipo} (linha {row})")

        if dry_run: self.stdout.write(self.style.WARNING("Dry-run: nenhuma escrita aplicada."))
        self.stdout.write(self.style.SUCCESS(
            f"Parâmetros/Fatores/Desperdícios => criados:{res.created} atualizados:{res.updated} pulados:{res.skipped}"
        ))
        for e in res.errors: self.stdout.write(self.style.NOTICE(f"- {e}"))
