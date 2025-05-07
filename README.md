# B4GE - Calculadora de Energia Embutida e Emissões de CO₂eq

Este projeto é uma aplicação web baseada na planilha "SA_Calculadora de Energia Embutida e Emissões de CO2eq - B4Ge".  
Desenvolvido com **Python + Django**, tem como objetivo calcular a energia embutida e as emissões de carbono de obras civis.

## Funcionalidades:
- Cadastro de obras e insumos
- Banco de materiais com dados ambientais
- Cálculo automático de energia embutida (MJ) e CO₂eq (kg)
- Geração de relatórios (em breve)

## Como rodar o projeto

```bash
# Clone o repositório
git clone https://github.com/agneloobruno/projeto_b4ge.git
cd projeto_b4ge

# Crie e ative o ambiente virtual
python -m venv venv
venv\\Scripts\\activate  # no Windows

# Instale as dependências
pip install -r requirements.txt

# Execute o servidor
python manage.py runserver
