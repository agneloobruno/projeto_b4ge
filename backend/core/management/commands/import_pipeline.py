from django.core.management.base import BaseCommand
from django.core.management import call_command

class Command(BaseCommand):
    help = "Executa toda a pipeline de importação e cálculo de impacto ambiental"

    def handle(self, *args, **options):
        steps = [
            ("Importando materiais", "import_materials"),
            ("Importando insumos", "importar_insumos"),
            ("Importando composições", "importar_composicoes"),
            ("Importando dados SINAPI auxiliares", "import_insumos_sinapi"),
            ("Importando aba Lista (B4Ge)", "import_lista_b4ge"),
            ("Marcando composições cíclicas", "marcar_itens_ciclicos"),
            ("Verificando ciclos", "verificar_ciclos"),
            ("Atualizando impacto ambiental", "atualizar_impacto"),
            ("Executando diagnóstico", "diagnostico_impacto")
        ]

        for descricao, comando in steps:
            self.stdout.write(self.style.NOTICE(f"\n▶ {descricao} ({comando})..."))
            try:
                call_command(comando)
            except Exception as e:
                self.stdout.write(self.style.ERROR(f"Erro ao executar {comando}: {str(e)}"))
                break
        else:
            self.stdout.write(self.style.SUCCESS("\n✅ Pipeline de importação e processamento concluída com sucesso!"))
