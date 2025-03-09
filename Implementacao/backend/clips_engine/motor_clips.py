import sys
sys.path.append('/home/eduardo/projetos/expert-system/backend/venv/lib/python3.8/site-packages/clipspy')

from clips import Environment

BASE_CONHECIMENTO_PATH = 'rules/base-conhecimento.clp'

def processar_contrato(dados_usuario):
    env = Environment()

    try:
        # Verificar se o caminho do arquivo de base de conhecimento está correto
        env.load(BASE_CONHECIMENTO_PATH)
    except Exception as e:
        raise Exception(f"Erro ao carregar a base de conhecimento: {str(e)}")

    # Iniciar o fato para o template contrato
    contrato_fato = "(contrato "

    # Adicionar todos os slots do contrato de uma vez
    for chave, valor in dados_usuario.items():
        contrato_fato += f"({chave} {valor}) "

    contrato_fato += ")"  # Fechar o fato

    # Inserir o fato no CLIPS
    env.assert_string(contrato_fato)

    # Rodar motor de inferência
    env.run()

    # Mostrar todos os fatos após execução (para depuração)
    print("\nFATOS APÓS EXECUCAO DO CLIPS:")
    for fato in env.facts():
        print(fato)

    # Recuperar o tipo de contrato (ex: comodato) a partir do fato (contrato-selecionado)
    contrato_tipo = None
    for fato in env.facts():
        if fato.template.name == "contrato-selecionado":
            contrato_tipo = fato[0]

    # Coletar os fatos gerados (clausula-incluida e clausula-itens)
    clausulas = interpretar_resultado_clips(env)

    # Mostrar todas as clausulas após execução (para depuração)
    print("\nCLAUSULAS INTERPRETADAS:")
    print(clausulas)  

    # Ajustar a estrutura do JSON
    resultado = {}
    
    if contrato_tipo:
        resultado["contrato"] = contrato_tipo

    # Organizar as cláusulas corretamente (nome e itens) garantindo que o "nome" venha primeiro

    resultado["clausulas"] = []
    if clausulas:
        resultado["clausulas"] = clausulas

    print("\nRESPOSTA JSON:")
    print(resultado)

    return {"dados-contrato": resultado}


def interpretar_resultado_clips(env):
    clausulas = {}

    # Buscar os fatos existentes após a execução
    for fato in env.facts():      
        if fato.template.name == "clausula-incluida":
            nome = fato[0]  # Acessar pelo índice, que é o nome da cláusula
            clausulas[nome] = []  # Inicializa a lista de itens para essa cláusula

        elif fato.template.name == "clausula-itens":
            nome = fato[0]  # Acessar pelo índice, que é o nome da cláusula
            itens = [fato[i] for i in range(1, len(fato))]  # Acessar os itens pelos índices
            if nome in clausulas:
                clausulas[nome].extend(itens)

    # Formatar a resposta de acordo com o esperado no JSON
    clausulas_json = []
    for nome, itens in clausulas.items():
        clausulas_json.append({
            "nome": nome,
            "itens": itens
        })

    return clausulas_json
