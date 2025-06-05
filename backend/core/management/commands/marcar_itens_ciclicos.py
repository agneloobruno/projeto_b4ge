from django.core.management.base import BaseCommand
from core.models import Composicao, ComposicaoItem

class Command(BaseCommand):
    help = "Marca como invalido os ComposicaoItem que causam ciclos diretos ou indiretos"

    def detectar_ciclos(self, composicao, visitados=None, caminho=None):
        if visitados is None:
            visitados = set()
        if caminho is None:
            caminho = []

        if composicao.pk in visitados:
            return True, caminho + [composicao.codigo]

        visitados.add(composicao.pk)
        caminho.append(composicao.codigo)

        for item in composicao.itens.filter(valido=True):
            if item.subcomposicao:
                ciclo, caminho_encontrado = self.detectar_ciclos(
                    item.subcomposicao,
                    visitados.copy(),
                    caminho[:]
                )
                if ciclo:
                    return True, caminho_encontrado

        return False, caminho

    def handle(self, *args, **kwargs):
        total_marcados = 0
        ciclos_detectados = []

        for composicao in Composicao.objects.all():
            ciclo, caminho = self.detectar_ciclos(composicao)
            if ciclo:
                for i in range(len(caminho) - 1):
                    pai = caminho[i]
                    filho = caminho[i + 1]
                    item = ComposicaoItem.objects.filter(
                        composicao_pai__codigo=pai,
                        subcomposicao__codigo=filho,
                        valido=True
                    ).first()
                    if item:
                        item.valido = False
                        item.save()
                        total_marcados += 1
                        ciclos_detectados.append((pai, filho, caminho))
                        break

        if ciclos_detectados:
            self.stdout.write(self.style.WARNING("\n⚠️ Ciclos resolvidos:"))
            for i, (pai, filho, caminho) in enumerate(ciclos_detectados, 1):
                self.stdout.write(f"{i}. {' → '.join(caminho)} → marcado como inválido: {pai} → {filho}")

        self.stdout.write(self.style.SUCCESS(f"\n✅ {total_marcados} ComposicaoItem(s) foram marcados como inválidos."))
