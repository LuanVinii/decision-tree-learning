import pandas as pd
import math

def entropia(classe):
    total = len(classe)
    contagem = {}

    # laço para contar quantas vezes cada classe se repete
    for valor in classe:
        if valor not in contagem:
            contagem[valor] = 0
        contagem[valor] += 1

    valor_entropia = 0

    # laço para somar a entropia total com base na proporção de cada classe
    for qtd in contagem.values():
        proporcao = qtd / total
        # formula da entropia
        valor_entropia -= proporcao * math.log2(proporcao)

    return valor_entropia

def ganho(data_frame, atributo, nome_classe):
    total = len(data_frame)

    # calcula a entropia da coluna de classe
    entropia_total = entropia(data_frame[nome_classe])

    entropia_condicional = 0

    # laço para calcular a entropia dos grupos (atributo e cada classe pertencente a ele)
    for valor, grupo in data_frame.groupby(atributo):
        proporcao = len(grupo) / total # proporção do grupo em relação ao total de registros

        classe_grupo = list(grupo[nome_classe])

        # calcula a entropia do grupo e soma ponderado pela proporção
        entropia_condicional += proporcao * entropia(classe_grupo)

        # retorna o valor do ganho de informação
    return entropia_total - entropia_condicional

def melhor_atributo(data_frame, atributos, nome_classe):
    ganhos = {} #dicionário para guardar o ganho de cada atributo

    for atributo in atributos:
        # calcula o ganho de cada atributo em relação à classe
        ganho_atual = ganho(data_frame, atributo, nome_classe)
        ganhos[atributo] = ganho_atual

        #retorna o nome do atributo com maior ganho e o dicionário de ganhos
    melhor = max(ganhos, key=ganhos.get)
    return melhor, ganhos


dados = {
    'Gênero': ['F', 'M', 'F', 'F', 'M', 'M', 'F', 'F', 'M', 'M'],
    'Idade': [22, 35, 47, 52, 46, 51, 23, 40, 36, 44],
    'Escolaridade': ['Superior', 'Médio', 'Médio Incompleto', 'Superior', 'Médio', 'Superior', 'Médio', 'Médio', 'Superior', 'Médio Incompleto'],
    'Estado Civil': ['Casado', 'Casado', 'Casado', 'Solteiro', 'Casado', 'Divorciado', 'Solteiro', 'Divorciado', 'Divorciado', 'Solteiro'],
    'Renda (R$)': [2500, 4000, 1200, 3200, 2700, 5000, 2300, 3800, 3100, 1500],
    'Forma de Pagamento': ['Cartão de Crédito', 'Boleto', 'Cartão de Débito', 'Boleto', 'Cartão de Crédito', 'PIX', 'PIX', 'Cartão de Crédito', 'Cartão de Débito', 'PIX'],
    'Comprou': ['Não', 'Sim', 'Não', 'Sim', 'Sim', 'Sim', 'Não', 'Sim', 'Sim', 'Não']
}


df = pd.DataFrame(dados)
print(df)