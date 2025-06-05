from core.models import Composicao
from core.utils import calcular_impacto

def diagnosticar_composicoes():
    composicoes = Composicao.objects.filter(itens__valido=True).distinct()
    print(f"\n🔍 {composicoes.count()} composições com itens válidos encontradas.\n")

    for composicao in composicoes:
        print(f"📦 Composição: {composicao.codigo} - {composicao.descricao}")
        impacto = calcular_impacto(composicao)
        print(f"    ➤ Impacto: {impacto}")

        itens = composicao.itens.filter(valido=True)
        if not itens.exists():
            print("    ⚠️ Nenhum item válido na composição.")
            continue

        for item in itens:
            print("    ────────────────")
            print(f"    • Proporção: {item.proporcao}")
            if item.insumo:
                print(f"    • Insumo: {item.insumo.codigo} - {item.insumo.descricao}")
                if item.insumo.material:
                    mat = item.insumo.material
                    print(f"        ↪ Material: {mat.descricao}")
                    print(f"        ↪ Energia MJ/kg: {mat.energia_embutida_mj_kg}, CO2: {mat.co2_kg}")
                else:
                    print("        ⚠️ Insumo sem material vinculado.")
            elif item.subcomposicao:
                print(f"    • Subcomposição: {item.subcomposicao.codigo} - {item.subcomposicao.descricao}")
            else:
                print("    ⚠️ Item sem insumo nem subcomposição.")

        print("")

diagnosticar_composicoes() # This function can be called directly or integrated into a management command for easier execution.
# If you want to run this as a management command, you can create a command file in the management/commands directory.
