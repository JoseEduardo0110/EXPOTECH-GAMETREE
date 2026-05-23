import sqlite3
import os
import re

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(SCRIPT_DIR, "GameTree.db")

def conectar():
        conn = sqlite3.connect(DB_PATH)
        conn.row_factory = sqlite3.Row
        return conn

def criar_tabela():
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("""
            CREATE TABLE IF NOT EXISTS usuarios (
            id_usuario INTEGER PRIMARY KEY AUTOINCREMENT,
            nome_usuario TEXT NOT NULL UNIQUE,
            email TEXT NOT NULL,
            senha TEXT NOT NULL,
            nivel INTEGER DEFAULT 1
    )
""")
    
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS jogos (
            id_jogo INTEGER PRIMARY KEY AUTOINCREMENT,
            titulo TEXT NOT NULL UNIQUE,
            descricao TEXT NOT NULL,
            link_steam TEXT NOT NULL,
            ram_minima INTEGER NOT NULL,
            armazenamento_minimo INTEGER NOT NULL,
            cpu_minima TEXT NOT NULL,
            gpu_minima TEXT NOT NULL
        )
    """)
    conn.commit()

    cursor.execute("SELECT COUNT(*) FROM jogos")
    if cursor.fetchone()[0] == 0:
        jogos_iniciais = [
            ("Minecraft", "Jogo de sobrevivência e construção com blocos em um mundo infinito.", "https://store.steampowered.com/app/1928420/Minecraft_Dungeons/", 4, 4),
            ("Counter-Strike 2", "Jogo de tiro tático em primeira pessoa baseado em objetivos.", "https://store.steampowered.com/app/730/CounterStrike_2/", 8, 85),
            ("The Witcher 3", "RPG de ação de mundo aberto focado em narrativa e caça a monstros.", "https://store.steampowered.com/app/292030/The_Witcher_3_Wild_Hunt/", 6, 50),
            ("Stardew Valley", "RPG de vida no campo onde você herda a antiga fazenda do seu avô.", "https://store.steampowered.com/app/413150/Stardew_Valley/", 2, 1),
            ("Cyberpunk 2077", "RPG de ação e aventura em mundo aberto ambientado em Night City.", "https://store.steampowered.com/app/1091500/Cyberpunk_2077/", 12, 70)
        ]
        cursor.executemany("""
            INSERT INTO jogos (titulo, descricao, link_steam, ram_minima, armazenamento_minimo)
            VALUES (?, ?, ?, ?, ?)
        """, jogos_iniciais)
        conn.commit()
        print("5 jogos iniciais foram cadastrados com sucesso no banco!")
    conn.close()
    return True

def criar_conta(nome, email, senha):
    if not nome or not email or not senha:
        print()
        print("Erro: Todos os campos devem ser preenchidos!")
        return False

    conn = conectar()
    cursor = conn.cursor()

    try:
        cursor.execute("""
            INSERT INTO usuarios (nome_usuario, email, senha) 
            VALUES (?, ?, ?)
        """, (nome, email, senha))
            
        conn.commit()
        print()
        print(f"Sucesso: Conta de '{nome}' criada!")
        return True

    except sqlite3.IntegrityError:
        print()
        print(f"Erro: O nome de usuário '{nome}' já está em uso.")
        return False

    finally:
        conn.close()

def listar_jogos():
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("SELECT id_jogo, titulo FROM jogos")
    jogos = cursor.fetchall()
    conn.close()
    
    if not jogos:
        print("Nenhum jogo encontrado no banco de dados.")
        return True
        
    print("\n--- JOGOS DISPONÍVEIS ---")
    for jogo in jogos:
        print(f"{jogo['id_jogo']} - {jogo['titulo']}")
    print("0 - Voltar ao Menu")
    print("-------------------------")
    
    try:
        escolha = int(input("Escolha o número de um jogo para ver os detalhes: ").strip())
    except ValueError:
        print("Opção inválida!")
        return True
        
    if escolha == 0:
        return True

    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM jogos WHERE id_jogo = ?", (escolha,))
    jogo_escolhido = cursor.fetchone()
    conn.close()
    
    if jogo_escolhido:
        print(f"\n=== {jogo_escolhido['titulo'].upper()} ===")
        print(f"Descrição: {jogo_escolhido['descricao']}")
        print(f"Link para compra (Steam): {jogo_escolhido['link_steam']}")
        print(f"\n--- REQUISITOS MÍNIMOS ---")
        print(f"-> Processador (CPU): {jogo_escolhido['cpu_minima']}")
        print(f"-> Placa de Vídeo (GPU): {jogo_escolhido['gpu_mínima']}")
        print(f"-> Memória RAM: {jogo_escolhido['ram_minima']}GB")
        print(f"-> Espaço: {jogo_escolhido['armazenamento_minimo']}GB")
        print("=============================")
        
        print("\n[1] Inserir Comentário neste jogo")
        print("[0] Voltar")
        
        acao = input("Escolha uma opção: ").strip()
        if acao == "1":
            print("\n-> Encaminhando para o sistema de comentários... (Opção ainda não desenvolvida)")
    else:
        print("Jogo não encontrado!")

    return True

def inserir_comentário():
        conn = conectar()
        cursor = conn.cursor()
        
        #espaço para comentar
        #avaliação por estrelas logo após o comentário ser feito e a opção ("Você recomendaria esse jogo?")
        #pôr horário que foi postado o comentário
        #exibir quem foi que fez o comentário
        #opção para por like nos comentários
        #espaço para por respostas no comentário exibido
        #(OPCIONAL)exibir usuário que fez aquela postagem
        #(VERIFICAR) # com base na categoria do jogo ex: #horror, ...
        return True

def verificar_requisitos():
        #Espaço para inserir os componentes da máquina
        #verificação se os componentes são de boa ou má qualidade
        #verificar quais jogos dá para rodar na máquina com base nos componentes inseridos


        return True

def limpar_tudo():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    cursor.execute("DELETE FROM usuarios")
    print("Banco de dados limpo com sucesso!")

    conn.commit()
    conn.close()
    

def exibir_menu():
    print("==== MENU ====")
    print("1 - Criar Conta")
    print("2 - Listar os jogos")
    print("3 - Inserir Comentário")
    print("4 - Analisar o Pc")
    print("0 - Sair")
    print()
    print("====== Menu ADMS ======")
    print("5 - Limpar o banco de dados")
    print("6 - adicionar jogos")
    

conn = conectar()
criar_tabela()

conta_criada = False

while True:
    exibir_menu()
    print()
    opcao = input("Escolha uma opcao: ").strip()
    print()

    if opcao == "1":
        padrao = r"^[\w\.-]+@[\w\.-]+\.\w+$"

        print("--- CADASTRO DE NOVA CONTA ---")
        
        nome_digitado = input("Nome de usuário: ").strip()
        email_digitado = input("E-mail: ").strip()
        if not re.match(padrao, email_digitado):
            print()
            print("Email inválido, tente novamente!")
            print()
            continue
        senha_digitada = input("Senha: ").strip()
                
        sucesso = criar_conta(nome_digitado, email_digitado, senha_digitada)

        if sucesso:
            conta_criada = True

    elif opcao == "5":
        confirmacao = input("Tem certeza que deseja limpar o banco de dados inteiro? (Y/N): ").strip().upper()

        if confirmacao == "Y":
            limpar_tudo()
            conta_criada = False
        else:
            print("Operação cancelada. Os dados continuam lá!")

    elif opcao in ["3", "4"]:
        if not conta_criada:
            print('Acesso negado, por favor, crie uma conta para prosseguir!')

        else:
            print('Opção ainda não desenvolvida!')
            print()
        
    elif opcao == "0":
        print('Saindo...')
        break
    else:
            print('Opção ainda não desenvolvida!')