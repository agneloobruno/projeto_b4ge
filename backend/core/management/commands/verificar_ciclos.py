from django.core.management.base import BaseCommand
from core.models import Composicao

class Command(BaseCommand):
    help = "Detecta composições com ciclos recursivos em subcomposições"

    def verificar_ciclo(self, composicao, visitados=None, caminho=None):
        if visitados is None:
            visitados = set()
        if caminho is None:
            caminho = []

        if composicao.pk in visitados:
            return True, caminho + [composicao.codigo]

        visitados.add(composicao.pk)
        caminho.append(composicao.codigo)

        for item in composicao.itens.all():
            if item.subcomposicao:
                tem_ciclo, caminho_encontrado = self.verificar_ciclo(
                    item.subcomposicao,
                    visitados.copy(),
                    caminho[:]
                )
                if tem_ciclo:
                    return True, caminho_encontrado

        return False, caminho

    def handle(self, *args, **kwargs):
        ciclos_detectados = []

        for composicao in Composicao.objects.all():
            resultado = self.verificar_ciclo(composicao)
            if resultado is not None:
                tem_ciclo, caminho = resultado
                if tem_ciclo:
                    ciclos_detectados.append(caminho)

        if ciclos_detectados:
            self.stdout.write(self.style.WARNING("\n⚠️ Ciclos detectados:"))
            for i, ciclo in enumerate(ciclos_detectados, 1):
                self.stdout.write(f"{i}. {' → '.join(ciclo)}")
        else:
            self.stdout.write(self.style.SUCCESS("✅ Nenhum ciclo detectado."))
