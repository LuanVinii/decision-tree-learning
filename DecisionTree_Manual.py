import pandas as pd
import math

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

def ganho(data_frame, atributo, nome_classe, nivel=0):
    entropia_total = entropia(data_frame[nome_classe])
    valores_unicos = data_frame[atributo].unique()

    print(f"\nAtributo: {atributo}")
    print(f"  - Entropia do conjunto atual ({nome_classe}): {round(entropia_total, 4)}")

    entropia_condicional = 0
    for valor in valores_unicos:
        subset = data_frame[data_frame[atributo] == valor]
        proporcao = len(subset) / len(data_frame)
        entropia_subset = entropia(subset[nome_classe])
        classe_counts = subset[nome_classe].value_counts().to_dict()

        # exibe a composição da classe (Sim/Não)
        composicao = ", ".join([f"{k}: {v}" for k, v in classe_counts.items()])
        print(f"    • {valor}: entropia = {round(entropia_subset, 4)}, proporção = {round(proporcao, 4)} [{composicao}]")

        entropia_condicional += proporcao * entropia_subset

    ganho_info = entropia_total - entropia_condicional
    print(f"  → Ganho de Informação: {round(ganho_info, 4)}")

    return ganho_info

def melhor_atributo(data_frame, atributos, nome_classe, nivel=0):
    print(f"\n{'  ' * nivel}Nível {nivel + 1} - Calculando Entropias e Ganhos por Atributo:")
    ganhos = {} #dicionário para guardar o ganho de cada atributo

    for atributo in atributos:
        # calcula o ganho de cada atributo em relação à classe
        ganho_atual = ganho(data_frame, atributo, nome_classe, nivel)
        ganhos[atributo] = ganho_atual

        #retorna o nome do atributo com maior ganho e o dicionário de ganhos
    melhor = max(ganhos, key=ganhos.get)

    print(f"\n{'  ' * nivel}Melhor Atributo neste nível: {melhor} (Ganho: {round(ganhos[melhor], 4)})")
    return melhor, ganhos

def criar_faixas(df, coluna, nome_coluna_nova, num_faixas = 3):
    minimo = df[coluna].min()
    maximo = df[coluna].max()
    intervalo = (maximo - minimo) // num_faixas + 1

    def faixa(valor):
        inicio = minimo + (valor - minimo) // intervalo * intervalo
        fim = inicio + intervalo - 1
        return f"{inicio}-{fim}"
    df[nome_coluna_nova] = df[coluna].apply(faixa)
    return df

def construir_arvore(data_frame, atributos, nome_classe, nivel=0):
    # Converte a coluna da classe para lista para poder trabalhar com os valores
    classes = data_frame[nome_classe].tolist()

    # Condição de parada 1: se todos os exemplos são da mesma classe, retorna essa classe
    if all(c == classes[0] for c in classes):
        return classes[0]

    # Condição de parada 2: se não há mais atributos para dividir, retorna a classe mais frequente
    if not atributos:
        return max(set(classes), key=classes.count)

    # Encontra o melhor atributo para fazer a divisão usando o critério de ganho de informação
    melhor, _ = melhor_atributo(data_frame, atributos, nome_classe, nivel)  # Passa o nivel aqui

    # Cria a estrutura do nó da árvore com o melhor atributo encontrado
    arvore = {melhor: {}}

    # Para cada valor único do atributo selecionado, divide os dados e faz a chamada recursiva
    for valor, grupo in data_frame.groupby(melhor):
        # Remove o atributo atual da lista de atributos disponíveis para os próximos níveis
        novos_atributos = [att for att in atributos if att != melhor]

        # Chamada recursiva para construir a subárvore, incrementando o nível
        arvore[f"{melhor} = {valor}"] = construir_arvore(grupo, novos_atributos, nome_classe, nivel+1)  # Incrementa o nivel aqui

    return arvore

def print_arvore(arvore, prefixo=""):
    if isinstance(arvore, dict):
        chaves = list(arvore.keys())
        for i, chave in enumerate(chaves):
            ultimo = i == len(chaves) - 1
            conector = "└── " if ultimo else "├── "
            print(prefixo + conector + str(chave))
            novo_prefixo = prefixo + ("    " if ultimo else "│   ")
            print_arvore(arvore[chave], novo_prefixo)
    else:
        print(prefixo + "└── " + str(arvore))

# Converte idade e renda em faixas para facilitar a divisão dos nós
df = criar_faixas(df, 'Idade', 'Faixa de Idade')
df = criar_faixas(df, 'Renda (R$)', 'Faixa de Renda')

atributos = ['Gênero', 'Escolaridade', 'Estado Civil', 'Forma de Pagamento', 'Faixa de Idade', 'Faixa de Renda']
arvore_resultado = construir_arvore(df, atributos, 'Comprou', 0)

print("\nÁrvore de Decisão:")
print_arvore(arvore_resultado)