import random
import time
import pandas as pd

###Definindo as turmas e as matérias com suas respectivas cargas horárias
turmas= {
    "5A": {"Artes": 2, "Educação Física-Professor1": 3, "Inglês": 1, "Regente-Professor1": 7, "Regente-Professor2": 7},
    "5B": {"Artes": 2, "Educação Física-Professor2": 3, "Inglês": 1, "Regente-Professor1": 7, "Regente-Professor2": 7},
    "6A": {"Artes": 2, "Ciências-Professor1": 3, "Educação Física-Professor1": 2, "Ensino Religioso": 2, "Geografia": 1, "História": 2, "Inglês": 1, "Matemática-Professor1": 3, "Português-Professor1": 4},
    "6B": {"Artes": 2, "Ciências-Professor1": 3, "Educação Física-Professor1": 2, "Ensino Religioso": 2, "Geografia": 1, "História": 2, "Inglês": 1, "Matemática-Professor1": 3, "Português-Professor1": 4},
    "7A": {"Artes": 1, "Ciências-Professor1": 3, "Educação Física-Professor1": 2, "Ensino Religioso": 2, "Geografia": 2, "História": 1, "Inglês": 2, "Matemática-Professor1": 4, "Português-Professor1": 3},
    "7B": {"Artes": 1, "Ciências-Professor1": 3, "Educação Física-Professor1": 2, "Ensino Religioso": 2, "Geografia": 2, "História": 1, "Inglês": 2, "Matemática-Professor1": 4, "Português-Professor1": 3},
    "8A": {"Artes": 1, "Ciências-Professor2": 4, "Educação Física-Professor2": 2, "Ensino Religioso": 2, "Geografia": 2, "História": 2, "Inglês": 1, "Matemática-Professor2": 3, "Português-Professor2": 3},
    "8B": {"Artes": 1, "Ciências-Professor2": 4, "Educação Física-Professor2": 2, "Ensino Religioso": 2, "Geografia": 2, "História": 2, "Inglês": 1, "Matemática-Professor2": 3, "Português-Professor2": 3},
    "9A": {"Artes": 1, "Ciências-Professor2": 3, "Educação Física-Professor2": 2, "Ensino Religioso": 1, "Geografia": 2, "História": 2, "Inglês": 2, "Matemática-Professor2": 4, "Português-Professor2": 3},
    "9B": {"Artes": 1, "Ciências-Professor2": 3, "Educação Física-Professor2": 2, "Ensino Religioso": 1, "Geografia": 2, "História": 2, "Inglês": 2, "Matemática-Professor2": 4, "Português-Professor2": 3}
}

# turmas= turmaExterno.balanceamento_professores_materia()
print(f"turmas:  {turmas}")

def introduzir_diversidade_com_mutacao(populacao, proporcao=0.3):
    num_mutacoes = int(len(populacao) * proporcao)
    for i in range(num_mutacoes):
        populacao[i] = (mutacao(populacao[i][0]), avaliar_aptidao(populacao[i][0]))
    return populacao

def salvar_horarios_em_excel(horarios):
    """
    Salva os horários gerados em um arquivo Excel, incluindo a contagem de cada matéria na semana.
    """
    with pd.ExcelWriter(f"horarios_turmas_{time.time()}.xlsx") as writer:
        for turma, dias in horarios.items():
            # Transpor os dados: dias da semana como colunas
            df = pd.DataFrame(dias).T
            df.columns = ["Segunda-feira", "Terça-feira", "Quarta-feira", "Quinta-feira", "Sexta-feira"]
            df.index = ["1º Horário", "2º Horário", "3º Horário", "4º Horário"]
            
            # Contar a frequência de cada matéria na semana
            todas_materias = [materia for dia in dias for materia in dia]
            contagem_materias = pd.DataFrame(
                {"Matéria": list(set(todas_materias)), 
                 "Frequência": [todas_materias.count(materia) for materia in set(todas_materias)]}
            )
            
            # Escrever o DataFrame de horários em uma aba do Excel
            df.to_excel(writer, sheet_name=turma, startrow=0)
            
            # Escrever a contagem de matérias abaixo da tabela de horários
            contagem_materias.to_excel(writer, sheet_name=turma, startrow=len(df) + 3, index=False)
    
    print("Planilha Excel gerada com sucesso!")

def gerar_horarios_turmas(carga_horaria):
    horario = [[None] * 4 for _ in range(5)]  # 5 dias, 4 períodos por dia
    materias = []

    # Cria uma lista de matérias com base na carga horária
    for materia, carga in carga_horaria.items():
        materias.extend([materia] * carga)

    random.shuffle(materias)  # Embaralha as matérias

    # Distribui as matérias
    for materia in materias:
        alocado = False
        while not alocado:
            dia = random.randint(0, 4)  # Escolhe um dia aleatório
            periodo = random.randint(0, 3)  # Escolhe um período aleatório
            if horario[dia][periodo] is None:  # Verifica se o horário está vazio
                horario[dia][periodo] = materia
                alocado = True

    return horario

# Gera os horários para todas as turmas
def gerar_horarios_todas_turmas():   
    def verificar_alocacao(horario, carga_horaria, turma):
        """Verifica se todas as matérias foram alocadas corretamente."""
        alocadas = [materia for dia in horario for materia in dia if materia]
        for materia, carga in carga_horaria.items():
            if alocadas.count(materia) != carga:
                print(f"Erro: A matéria {materia} não foi completamente alocada na turma {turma}.") 

    horarios_turmas = {}
    for turma, carga_horaria in turmas.items():
        horarios_turmas[turma] = gerar_horarios_turmas(carga_horaria)
    verificar_alocacao(horarios_turmas[turma], carga_horaria, turma)

    return horarios_turmas



def avaliar_aptidao(horarios):
    penalidades = 0
       
    # Dicionário para rastrear a carga horária de cada matéria em todas as turmas
    carga_horaria_geral = {}

    for turma, horario in horarios.items():
        # 1- Carga horária da matéria sendo cumprida por turmas
        carga_horaria_gerada = {}
        for dia in horario:
            for materia in dia:
                if materia:
                    carga_horaria_gerada[materia] = carga_horaria_gerada.get(materia, 0) + 1
        for materia, carga in turmas[turma].items():
            if carga_horaria_gerada.get(materia, 0) != carga:
                # penalidades += abs(carga_horaria_gerada.get(materia, 0) - carga) * 5  # Penalidade maior por erro de carga horária
                penalidades += 4  # Penalidade maior por erro de carga horária
        
        # 2- Verificar repetição de matérias no mesmo dia
        for dia_idx, dia in enumerate(horario):
            materias_no_dia = set()
            carga_horaria_dia = {}  # Contagem de aulas por matéria no dia          
            for periodo_idx, materia in enumerate(dia):              
                if materia:
                    # 3- Verificar repetição de matérias no mesmo dia
                    # Penalizar repetição de matérias no mesmo dia
                    if turma == "5A" and materia not in ["Regente-Professor1", "Regente-Professor2"] and materia in materias_no_dia:
                        penalidades += 1  # Penalidade para repetição de matérias no 5A (exceto regentes)
                    elif turma == "5B" and materia not in ["Regente-Professor1", "Regente-Professor2"] and materia in materias_no_dia:
                        penalidades += 1  # Penalidade para repetição de matérias no 5B (exceto regentes)
                    elif turma not in ["5A", "5B"] and materia in materias_no_dia:
                        penalidades += 1  # Penalidade para repetição de qualquer matéria nas outras turmas
                    materias_no_dia.add(materia)


                    
        
    # 3- Após processar todas as turmas, verificar excesso de carga horária por matéria no dia
    for turma, horario in horarios.items():
        for dia_idx, dia in enumerate(horario):
            for periodo_idx, materia in enumerate(dia):
                if materia:
                    # Atualizar a carga horária geral da matéria
                    if materia not in carga_horaria_geral:
                        carga_horaria_geral[materia] = {}
                    if dia_idx not in carga_horaria_geral[materia]:
                        carga_horaria_geral[materia][dia_idx] = 0
                    carga_horaria_geral[materia][dia_idx] += 1

    # 3.a- Verificar excesso de carga horária por matéria no dia
    for materia, dias in carga_horaria_geral.items():
        for dia, total_periodos in dias.items():
            if total_periodos > 4:  # Limite de 4 períodos por dia
                penalidades += (total_periodos - 4) * 5  # Penalidade para excesso de carga horária

    
    
    return penalidades


# Seleção por ranking
def selecao_por_ranking(populacao, num_individuos):
    # Ordenar a população pela aptidão (menor penalidade primeiro)
    populacao_ordenada = sorted(populacao, key=lambda x: x[1])
    
    # Criar uma lista de probabilidades inversamente proporcionais à posição no ranking
    ranking = list(range(1, len(populacao_ordenada) + 1))
    probabilidades = [1 / rank for rank in ranking]
    soma_probabilidades = sum(probabilidades)
    probabilidades_normalizadas = [p / soma_probabilidades for p in probabilidades]
    
    # Selecionar indivíduos com base nas probabilidades normalizadas
    selecionados = random.choices(
        populacao_ordenada, 
        weights=probabilidades_normalizadas, 
        k=num_individuos
    )
    
    # Retornar apenas os indivíduos selecionados (sem as penalidades)
    return [individuo[0] for individuo in selecionados]

# # # Cruzamento de dois pontos
def cruzamento(pai1, pai2):
    filho = {}
    for turma in pai1:
        horario_filho = []
        for dia1, dia2 in zip(pai1[turma], pai2[turma]):
            horario_filho.append([random.choice([a, b]) for a, b in zip(dia1, dia2)])
        filho[turma] = horario_filho
    return filho

# Aumentando a probabilidade de mutação
def mutacao(horarios):
    turma_mutada = random.choice(list(horarios.keys()))
    dia1, dia2 = random.sample(range(5), 2)  # Escolhe dois dias aleatórios
    periodo1, periodo2 = random.sample(range(4), 2)  # Escolhe dois períodos aleatórios
    # Troca as matérias entre os dois períodos
    horarios[turma_mutada][dia1][periodo1], horarios[turma_mutada][dia2][periodo2] = \
        horarios[turma_mutada][dia2][periodo2], horarios[turma_mutada][dia1][periodo1]
    return horarios

# Algoritmo Genético para gerar o horário
def algoritmo_genetico():
    # Parâmetros do algoritmo genético
    num_geracoes = 1000
    num_individuos = 300
    probabilidade_mutacao = 0.1
    taxa_elitismo = 0.3

    # Geração de população inicial
    print("começou gerar horario turmas")
    populacao = [(gerar_horarios_todas_turmas(), 0) for _ in range(num_individuos)]  # Aumenta a população inicial
    print("finalizou gerar horario turmas")

    # Avaliar aptidão de cada indivíduo na população
    populacao = [(horarios, avaliar_aptidao(horarios)) for horarios, _ in populacao]

    # Inicializar a variável de melhor penalidade
    melhor_penalidade_anterior = float('inf')
    estagnacao = 0  # Inicializar antes do loop

    for geracao in range(num_geracoes):
        # # # Ajustar a taxa de mutação dinamicamente
        if estagnacao >= 10:
            probabilidade_mutacao = min(1.0, probabilidade_mutacao + 0.1)
        else:
            probabilidade_mutacao = 0.1

        # Seleção dos pais
        # pais = selecao_por_torneio(populacao, num_individuos, tamanho_torneio=5)
        pais = selecao_por_ranking(populacao, num_individuos)

        # Cruzamento dos pais para gerar filhos
        filhos = []
        for i in range(0, len(pais) - 1, 2):
            filho = cruzamento(pais[i], pais[i + 1])
            filhos.append(filho)

        if len(pais) % 2 != 0:
            filhos.append(pais[-1])

        # Mutação dos filhos
        for filho in filhos:
            if random.random() < probabilidade_mutacao:
                mutacao(filho)

        # Avaliação de aptidão dos filhos
        filhos = [(filho, avaliar_aptidao(filho)) for filho in filhos]

        # # Preservar a elite
        elite = populacao[:int(len(populacao) * taxa_elitismo)]
        populacao = elite + filhos

        ####Introduzir diversidade se necessário
        if estagnacao >= 10:
            print("Reiniciando parte da população com maior diversidade...")
            populacao = introduzir_diversidade_com_mutacao(populacao, proporcao=0.1)
            estagnacao = 0

        # Melhor indivíduo da geração
        melhor_individuo = min(populacao, key=lambda x: x[1])
        print(f"Geração {geracao + 1}: Penalidade = {melhor_individuo[1]}")

        # Verificar estagnação
        if melhor_individuo[1] < melhor_penalidade_anterior:
            melhor_penalidade_anterior = melhor_individuo[1]
            estagnacao = 0
        else:
            estagnacao += 1

        if melhor_individuo[1] == 0:
            print(f"Melhor horário encontrado na geração {geracao + 1}:")
            salvar_horarios_em_excel(melhor_individuo[0])
            break


# Executar o algoritmo genético
start_time = time.time()
start_time_formatted = time.strftime("%H:%M:%S", time.localtime(start_time))
print(f"Tempo total inicial: {start_time_formatted}")
algoritmo_genetico()
end_time = time.time()
end_time_formatted = time.strftime("%H:%M:%S", time.localtime(end_time))
print(f"Tempo total final: {end_time_formatted}")