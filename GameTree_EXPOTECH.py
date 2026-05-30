import mysql.connector
from mysql.connector import Error
import os
import re

DB_CONFIG = {
    'host': 'localhost',
    'user': 'root',       
    'password': '1234', 
    'database': 'GameTree'
}

def conectar():
    """Estabelece a conexão com o banco de dados MySQL."""
    try:
        conn = mysql.connector.connect(**DB_CONFIG)
        return conn
    except Error as e:
        print(f"Erro ao conectar ao MySQL: {e}")
        return None

def criar_tabela():
    conn = conectar()
    if not conn:
        return False
    
    cursor = conn.cursor(dictionary=True)
    
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS usuarios (
            id_usuario INT AUTO_INCREMENT PRIMARY KEY,
            nome_usuario VARCHAR(100) NOT NULL UNIQUE,
            email VARCHAR(255) NOT NULL,
            senha VARCHAR(255) NOT NULL,
            nivel INT DEFAULT 1
        )
    """)
    
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS jogos (
            id_jogo INT AUTO_INCREMENT PRIMARY KEY,
            titulo VARCHAR(150) NOT NULL UNIQUE,
            descricao TEXT NOT NULL,
            link_steam VARCHAR(255) NOT NULL,
            ram_minima INT NOT NULL,
            armazenamento_minimo INT NOT NULL,
            cpu_minima VARCHAR(150) NOT NULL,
            gpu_minima VARCHAR(150) NOT NULL
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS comentarios (
            id_comentario INT AUTO_INCREMENT PRIMARY KEY,
            id_jogo INT NOT NULL,
            nome_usuario VARCHAR(100) NOT NULL,
            texto TEXT NOT NULL,
            estrelas INT NOT NULL,
            recomenda CHAR(1) NOT NULL,
            data_postagem DATETIME DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (id_jogo) REFERENCES jogos (id_jogo) ON DELETE CASCADE
        )
    """)
    conn.commit()


    cursor.execute("SELECT COUNT(*) as total FROM jogos")
    if cursor.fetchone()['total'] == 0:
        jogos_iniciais = [
            ("Minecraft", "Jogo de sobrevivência e construção com blocos.", "https://store.steampowered.com/app/1928420/Minecraft_Dungeons/", 4, 4, "Intel Core i3-3210 / AMD A8-7600", "Intel HD Graphics 4000 / AMD Radeon R5"),
            ("Counter-Strike 2", "Jogo de tiro tático em primeira pessoa baseado em objetivos.", "https://store.steampowered.com/app/730/CounterStrike_2/", 8, 85, "Intel Core i5 6600K / AMD Ryzen 5 1600", "NVIDIA GeForce GTX 1060 / AMD Radeon RX 580"),
            ("The Witcher 3", "RPG de ação de mundo aberto focado em caça a monstros.", "https://store.steampowered.com/app/292030/The_Witcher_3_Wild_Hunt/", 6, 50, "Intel Core i5-2500K / AMD Phenom II X4 940", "NVIDIA GTX 660 / AMD Radeon HD 7870"),
            ("Stardew Valley", "RPG de vida no campo onde você cuida da sua própria fazenda.", "https://store.steampowered.com/app/413150/Stardew_Valley/", 2, 1, "Intel 2Ghz", "Placa com 256MB de VRAM"),
            ("Cyberpunk 2077", "RPG de ação e aventura em mundo aberto em Night City.", "https://store.steampowered.com/app/1091500/Cyberpunk_2077/", 12, 70, "Intel Core i7-6700 / AMD Ryzen 5 1600", "NVIDIA GTX 1060 / AMD Radeon RX 580")
        ]
        cursor.executemany("""
            INSERT INTO jogos (titulo, descricao, link_steam, ram_minima, armazenamento_minimo, cpu_minima, gpu_minima)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
        """, jogos_iniciais)
        conn.commit()
        print("5 jogos iniciais foram cadastrados com sucesso no banco!")
    
    cursor.close()
    conn.close()
    return True

def criar_conta(nome, email, senha):
    if not nome or not email or not senha:
        print("\nErro: Todos os campos devem ser preenchidos!")
        return False

    conn = conectar()
    if not conn: return False
    cursor = conn.cursor(dictionary=True)

    try:
        cursor.execute("""
            INSERT INTO usuarios (nome_usuario, email, senha) 
            VALUES (%s, %s, %s)
        """, (nome, email, senha))
            
        conn.commit()
        print(f"\nSucesso: Conta de '{nome}' criada!")
        return True

    except Error as e:
        if e.errno == 1062:
            print(f"\nErro: O nome de usuário '{nome}' já está em uso.")
        else:
            print(f"\nErro no banco de dados: {e}")
        return False
    finally:
        cursor.close()
        conn.close()

def fazer_login():
    print("\n--- LOGIN DE USUÁRIO ---")
    nome_informado = input("Nome de usuário: ").strip()
    senha_informada = input("Senha: ").strip()

    if not nome_informado or not senha_informada:
        print("Erro: Todos os campos devem ser preenchidos!")
        return False, ""

    conn = conectar()
    if not conn: return False, ""
    cursor = conn.cursor(dictionary=True)

    try:
        cursor.execute("SELECT senha FROM usuarios WHERE nome_usuario = %s", (nome_informado,))
        usuario = cursor.fetchone()

        if usuario is None:
            print("\nErro: Nome de usuário não encontrado!")
            return False, ""

        if usuario["senha"] == senha_informada:
            print(f"\nSucesso: Bem-vindo de volta, {nome_informado}!")
            return True, nome_informado
        else:
            print("\nErro: Senha incorreta!")
            return False, ""

    except Error as e:
        print(f"Erro no banco de dados ao fazer login: {e}")
        return False, ""
    finally:
        cursor.close()
        conn.close()

def editar_perfil():
    print("\n--- Edição de perfil ---")
    nome_login = str(input("Digite o seu nome de usuário atual: ")).strip()
    senha_informada = input("Digite sua senha atual: ")

    conn = conectar()
    if not conn: return False
    cursor = conn.cursor(dictionary=True)

    try:
        cursor.execute("SELECT id_usuario, senha, email FROM usuarios WHERE nome_usuario = %s", (nome_login,))
        usuario = cursor.fetchone()

        if usuario is None:
            print("\nErro: Nome de usuário não foi encontrado.")
            return False
        
        if senha_informada != usuario['senha']:
            print("\nErro: Senha informada incorreta!")
            return False
        
        id_user = usuario['id_usuario']
        print("\n--- Identificação Confirmada ---")
        print("1 - alterar o nome de usuário")
        print("2 - alterar o email")
        print("3 - alterar a senha")

        opcao = input("\nEscolha a opção desejada: ")

        if opcao == "1":
            global usuario_atual

            novo_nome = input("Digite o novo nome de usuário: ").strip()
            if not novo_nome:
                print("Erro: o nome de usuário não pode ser vazio!")
                return False
            
            try:
                cursor.execute("UPDATE usuarios SET nome_usuario = %s WHERE id_usuario = %s", (novo_nome, id_user))
                conn.commit()
                usuario_atual = novo_nome
                print(f"\nSucesso! O seu nome de usuário foi alterado para '{novo_nome}'.")

            except Error as e:
                if e.errno == 1062:
                    print(f"\nErro: O nome de usuário: {novo_nome} já está em uso.")
                else:
                    print(f"\nErro ao atualizar: {e}")
                return False
            
        elif opcao == "2":
            novo_email = input("Digite o novo endereço de E-mail: ").strip()
            if not novo_email:
                print("Erro: O email informado não entrou nos padrões.")
                return False
            
            cursor.execute("UPDATE usuarios SET email = %s WHERE id_usuario = %s", (novo_email, id_user))
            conn.commit()
            print("\nEmail updated com sucesso!")

        elif opcao == "3":
            nova_senha = input("Digite sua nova senha: ").strip()
            confirmar_senha = input("Digite sua nova senha novamente para confirmar: ").strip()

            if not nova_senha:
                print("Erro: A senha não pode ser vazia.")
                return False
            
            if nova_senha != confirmar_senha:
                print("Erro: As senhas não coincidem!")
                return False
            
            cursor.execute("UPDATE usuarios SET senha = %s WHERE id_usuario = %s", (nova_senha, id_user))
            conn.commit()
            print("\nSucesso, senha alterada!")

        elif opcao == "4":
            print("Operação cancelada!")
            return True
        else:
            print("Opção inválida!")
            return False
    except Error as e:
        print(f"Erro no banco de dados ao editar perfil: {e}")
        return False
    finally:
        cursor.close()
        conn.close()

def inserir_jogos():
    print("\n--- Inserir jogos ---")
    titulo = input("Título do jogo: ").strip()
    if not titulo:
        print("Erro: O título do jogo não pode ser vazio.")
        return False
    descricao = input("Resumo/Sinópse do jogo: ").strip()
    link_loja = input("Link de compra: ").strip()

    try:
        ram_minima = int(input("Quantidade mínima de RAM (em GB - apenas os números): ").strip())
        armazenamento_minimo = int(input("Armazenamento mínimo necessário (em GB - apenas os números): ").strip())
    except ValueError:
        print("\nErro: RAM e Armazenamento precisam ser valores numéricos inteiros!")
        return False
    
    cpu_minima = input("Processador mínimo (CPU): ").strip()
    gpu_minima = input("Placa de vídeo mínima (GPU): ").strip()

    conn = conectar()
    if not conn: return False
    cursor = conn.cursor(dictionary=True)

    try:
        cursor.execute("""
            INSERT INTO jogos (titulo, descricao, link_steam, ram_minima, armazenamento_minimo, cpu_minima, gpu_minima)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
        """, (titulo, descricao, link_loja, ram_minima, armazenamento_minimo, cpu_minima, gpu_minima))
        
        conn.commit()
        print(f"\nSucesso: o jogo '{titulo}' foi cadastrado com sucesso!")
        return True
    except Error as e:
        if e.errno == 1062:
            print("Erro: Já existe um jogo cadastrado com esse nome")
        else:
            print(f"Erro no banco de dados ao cadastrar o jogo: {e}")
        return False
    finally:
        cursor.close()
        conn.close()

def listar_jogos():
    global usuario_atual
    conn = conectar()
    if not conn: return True
    cursor = conn.cursor(dictionary=True)
    
    cursor.execute("SELECT id_jogo, titulo FROM jogos")
    jogos = cursor.fetchall()
    
    if not jogos:
        print("Nenhum jogo encontrado no banco de dados.")
        cursor.close()
        conn.close()
        return True
        
    print("\n--- JOGOS DISPONÍVEIS ---\n")
    for jogo in jogos:
        print(f"{jogo['id_jogo']} - {jogo['titulo']}")
    print("\n0 - Voltar ao Menu")
    print("-------------------------")
    
    try:
        escolha = int(input("Escolha o número de um jogo para ver os detalhes: ").strip())
    except ValueError:
        print("Opção inválida!")
        cursor.close()
        conn.close()
        return True
        
    if escolha == 0:
        cursor.close()
        conn.close()
        return True

    cursor.execute("SELECT * FROM jogos WHERE id_jogo = %s", (escolha,))
    jogo_escolhido = cursor.fetchone()
    
    if jogo_escolhido:
        print(f"\n=== {jogo_escolhido['titulo'].upper()} ===")
        print(f"Descrição: {jogo_escolhido['descricao']}")
        print(f"Link para compra (Steam): {jogo_escolhido['link_steam']}")
        print(f"\n--- REQUISITOS MÍNIMOS ---")
        print(f"-> Processador (CPU): {jogo_escolhido['cpu_minima']}")
        print(f"-> Placa de Vídeo (GPU): {jogo_escolhido['gpu_minima']}")
        print(f"-> Memória RAM: {jogo_escolhido['ram_minima']}GB")
        print(f"-> Espaço: {jogo_escolhido['armazenamento_minimo']}GB")
        print("=============================")

        # Fecha o cursor atual antes de chamar funções que abrem outros cursores
        cursor.close()
        conn.close()

        exibir_comentarios(jogo_escolhido['id_jogo'])
        
        print("\n[1] Inserir Comentário neste jogo")
        print("[0] Voltar")
        
        acao = input("Escolha uma opção: ").strip()
        if acao == "1":
            print("\n-> Encaminhando para o sistema de comentários...")
            inserir_comentario(jogo_escolhido['id_jogo'], usuario_atual)
    else:
        print("Jogo não encontrado!")
        cursor.close()
        conn.close()

    return True

def inserir_comentario(id_jogo, nome_usuario):
    print("\n--- INSERIR NOVO COMENTÁRIO ---")
    texto = input("Digite o seu comentário sobre o jogo: ").strip()

    try:
        estrelas = int(input("Avaliação (de 1 a 5 estrelas): ").strip())
        if estrelas < 1 or estrelas > 5:
            print("Nota inválida! Escolha de 1 a 5.")
            return False
    except ValueError:
        print("Digite um número válido para as estrelas.")
        return False
    recomenda = input("Você recomendaria esse jogo? (S/N): ").strip().upper()
    if recomenda not in ["S", "N"]:
        print("Opção inválida! Escolha S para Sim ou N para Não.")
        return False

    if not texto:
        print("O comentário não pode ficar vazio!")
        return False

    conn = conectar()
    if not conn: return False
    cursor = conn.cursor(dictionary=True)
    
    cursor.execute("""
        INSERT INTO comentarios (id_jogo, nome_usuario, texto, estrelas, recomenda)
        VALUES (%s, %s, %s, %s, %s)
    """, (id_jogo, nome_usuario, texto, estrelas, recomenda))
    conn.commit()
    cursor.close()
    conn.close()

    print("\nSeu comentário foi publicado!")
    return True

def exibir_comentarios(id_jogo):
    conn = conectar()
    if not conn: return
    cursor = conn.cursor(dictionary=True)
    
    cursor.execute("SELECT nome_usuario, texto, estrelas, recomenda, data_postagem FROM comentarios WHERE id_jogo = %s ORDER BY data_postagem DESC", (id_jogo,))
    comentarios = cursor.fetchall()
    cursor.close()
    conn.close()

    print("\n--- AVALIAÇÕES DOS USUÁRIOS ---\n")
    if not comentarios:
        print("Nenhum comentário ainda. Seja o primeiro a avaliar!")
    for c in comentarios:
        recomenda_status = "👍 Recomendado" if c['recomenda'] == "S" else "👎 Não Recomendado"
        estrelas_visuais = "⭐" * c['estrelas']
        # Convertemos para string pois o MySQL retorna um objeto datetime nativo do Python
        data_str = c['data_postagem'].strftime('%Y-%m-%d %H:%M:%S') if c['data_postagem'] else "Sem data"
        print(f"[{data_str}] {c['nome_usuario']} - {estrelas_visuais} ({recomenda_status})")
        print(f"💬 \"{c['texto']}\"")
        print("-" * 30)

def verificar_requisitos():
    print("\n=== VERIFICADOR DE REQUISITOS DO PC ===")
    print("Insira as especificações da sua máquina abaixo:\n")

    try:
        ram_usuario = int(input("Quantidade de RAM (em GB): ").strip())
    except ValueError:
        print("Valor inválido para RAM!")
        return True

    try:
        armazenamento_usuario = int(input("Armazenamento disponível (em GB): ").strip())
    except ValueError:
        print("Valor inválido para armazenamento!")
        return True

    cpu_usuario = input("Modelo da CPU (ex: Intel Core i5-8400): ").strip().lower()
    gpu_usuario = input("Modelo da GPU (ex: NVIDIA GTX 1060): ").strip().lower()

    if not cpu_usuario or not gpu_usuario:
        print("CPU e GPU não podem estar vazias!")
        return True

    def avaliar_hardware(ram, cpu, gpu):
        pontuacao = 0

        if ram >= 32: pontuacao += 3
        elif ram >= 16: pontuacao += 2
        elif ram >= 8: pontuacao += 1

        cpus_altas = ["i9", "i7-12", "i7-13", "i7-14", "ryzen 7 5", "ryzen 7 7", "ryzen 9"]
        cpus_medias = ["i7", "i5-10", "i5-11", "i5-12", "ryzen 5 3", "ryzen 5 5", "ryzen 7"]
        cpus_baixas = ["i5", "i3", "ryzen 5", "ryzen 3", "fx-", "a10", "celeron", "pentium"]

        if any(c in cpu for c in cpus_altas): pontuacao += 3
        elif any(c in cpu for c in cpus_medias): pontuacao += 2
        elif any(c in cpu for c in cpus_baixas): pontuacao += 1

        gpus_altas = ["rtx 4090", "rtx 4080", "rtx 4070", "rtx 4050", "rtx 3080", "rtx 3090", "rx 7900", "rx 6900", "rx 6800"]
        gpus_medias = ["rtx 3060", "rtx 2060", "rtx 2070", "rtx 2080", "gtx 1080", "rx 6700", "rx 5700", "rx 580"]
        gpus_baixas = ["gtx 1060", "gtx 1050", "gtx 970", "gtx 960", "rx 570", "rx 480", "gtx 750", "intel hd", "radeon hd"]

        if any(g in gpu for g in gpus_altas): pontuacao += 3
        elif any(g in gpu for g in gpus_medias): pontuacao += 2
        elif any(g in gpu for g in gpus_baixas): pontuacao += 1

        if pontuacao >= 8: return "ALTO DESEMPENHO"
        elif pontuacao >= 5: return "DESEMPENHO MÉDIO"
        elif pontuacao >= 2: return "DESEMPENHO BAIXO"
        else: return "MUITO FRACO"

    categoria = avaliar_hardware(ram_usuario, cpu_usuario, gpu_usuario)
    print(f"\n Avaliação da sua máquina: [{categoria}]")

    conn = conectar()
    if not conn: return True
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM jogos")
    todos_jogos = cursor.fetchall()
    cursor.close()
    conn.close()

    jogos_compativeis = []
    jogos_incompativeis = []

    def extrair_numero_cpu(cpu_str):
        cpu_str = cpu_str.lower()
        numeros = re.findall(r'\d+', cpu_str)
        return int(numeros[0]) if numeros else 0

    for jogo in todos_jogos:
        ram_ok = ram_usuario >= jogo["ram_minima"]
        armazenamento_ok = armazenamento_usuario >= jogo["armazenamento_minimo"]

        cpu_req = jogo["cpu_minima"].lower()
        gpu_req = jogo["gpu_minima"].lower()

        num_cpu_usuario = extrair_numero_cpu(cpu_usuario)
        num_cpu_req = extrair_numero_cpu(cpu_req)

        cpu_ok = num_cpu_usuario >= num_cpu_req

        num_gpu_usuario = int(re.search(r'\d{3,4}', gpu_usuario).group()) if re.search(r'\d{3,4}', gpu_usuario) else 0
        num_gpu_req = int(re.search(r'\d{3,4}', gpu_req).group()) if re.search(r'\d{3,4}', gpu_req) else 0

        gpu_ok = num_gpu_usuario >= num_gpu_req

        if ram_ok and armazenamento_ok and cpu_ok and gpu_ok:
            jogos_compativeis.append(jogo)
        else:
            motivos = []
            if not ram_ok:
                motivos.append(f"RAM insuficiente (precisa de {jogo['ram_minima']}GB, você tem {ram_usuario}GB)")
            if not armazenamento_ok:
                motivos.append(f"Armazenamento insuficiente (precisa de {jogo['armazenamento_minimo']}GB, você tem {armazenamento_usuario}GB)")
            if not cpu_ok:
                motivos.append(f"CPU abaixo do mínimo (requer: {jogo['cpu_minima']})")
            if not gpu_ok:
                motivos.append(f"GPU abaixo do mínimo (requer: {jogo['gpu_minima']})")
            jogos_incompativeis.append((jogo, motivos))

    print(f"\n Jogos que RODAM na sua máquina ({len(jogos_compativeis)}):")
    print("-" * 45)
    if jogos_compativeis:
        for j in jogos_compativeis:
            print(f"  ✔  {j['titulo']}")
    else:
        print("  Nenhum jogo compatível encontrado.")

    print(f"\n Jogos que NÃO rodam na sua máquina ({len(jogos_incompativeis)}):")
    print("-" * 45)
    if jogos_incompativeis:
        for j, motivos in jogos_incompativeis:
            print(f"  ✘  {j['titulo']}")
            for m in motivos:
                print(f"       → {m}")
    else:
        print("  Parabéns! Seu PC roda todos os jogos disponíveis.")

    print("\n" + "=" * 45)
    return True

def gerenciar_banco():
    while True:
        print("\n--- Menu: Gerenciamento dos Dados ---")
        print("1 - Remover usuário por ID")
        print("2 - Remover comentário pelo ID")
        print("3 - Remover jogo pelo ID")
        print("4 - Inserir novo jogo")
        print("0 - Voltar ao menu principal")

        opcao = input("\nEscolha a opção desejada: ").strip()

        if opcao == "0":
            print("Voltando ao menu principal...")
            break

        conn = conectar()
        if not conn: continue
        cursor = conn.cursor(dictionary=True)

        try:
            if opcao == "1":
                cursor.execute("SELECT id_usuario, nome_usuario, email FROM usuarios")
                usuarios = cursor.fetchall()
                
                if not usuarios:
                    print("\nNenhum usuário cadastrado no sistema.")
                    cursor.close()
                    conn.close()
                    continue
                
                print("\n--- USUÁRIOS CADASTRADOS ---")
                for u in usuarios:
                    print(f"ID: {u['id_usuario']} | Nome: {u['nome_usuario']} | E-mail: {u['email']}")
                
                try:
                    id_alvo = int(input("\nDigite o ID do usuário que deseja deletar: ").strip())
                except ValueError:
                    print("Erro: O ID precisa ser um número!")
                    cursor.close()
                    conn.close()
                    continue
                
                cursor.execute("DELETE FROM usuarios WHERE id_usuario = %s", (id_alvo,))
                conn.commit()
                
                if cursor.rowcount > 0:
                    print(f"\nSucesso: Usuário com ID {id_alvo} foi removido.")
                else:
                    print(f"\nAviso: Nenhum usuário encontrado com o ID {id_alvo}.")

            elif opcao == "2":
                cursor.execute("""
                    SELECT DISTINCT j.id_jogo, j.titulo 
                    FROM jogos j
                    INNER JOIN comentarios c ON j.id_jogo = c.id_jogo
                """)
                jogos_com_comentarios = cursor.fetchall()
                
                if not jogos_com_comentarios:
                    print("\nNenhum comentário cadastrado no sistema para ser removido.")
                    cursor.close()
                    conn.close()
                    continue
                
                print("\n--- JOGOS QUE POSSUEM COMENTÁRIOS ---")
                for j in jogos_com_comentarios:
                    print(f"ID: {j['id_jogo']} | Jogo: {j['titulo']}")
                
                try:
                    id_jogo_escolhido = int(input("\nDigite o ID do jogo para ver os comentários: ").strip())
                except ValueError:
                    print("Erro: O ID precisa ser um número!")
                    cursor.close()
                    conn.close()
                    continue
                    
                cursor.execute("""
                    SELECT id_comentario, nome_usuario, texto, estrelas 
                    FROM comentarios 
                    WHERE id_jogo = %s
                """, (id_jogo_escolhido,))
                comentarios = cursor.fetchall()
                
                if not comentarios:
                    print("\nEste jogo não possui comentários.")
                    cursor.close()
                    conn.close()
                    continue
                
                print("\n--- COMENTÁRIOS DESTE JOGO ---")
                for c in comentarios:
                    print(f"ID Comentário: {c['id_comentario']} | Usuário: {c['nome_usuario']} | Nota: {'⭐' * c['estrelas']}")
                    print(f"💬 \"{c['texto']}\"")
                    print("-" * 40)
                
                try:
                    id_comentario_deletar = int(input("Digite o ID do COMENTÁRIO que deseja apagar: ").strip())
                except ValueError:
                    print("Erro: O ID precisa ser um número!")
                    cursor.close()
                    conn.close()
                    continue
                
                cursor.execute("DELETE FROM comentarios WHERE id_comentario = %s AND id_jogo = %s", (id_comentario_deletar, id_jogo_escolhido))
                conn.commit()
                
                if cursor.rowcount > 0:
                    print(f"\nSucesso: O comentário ID {id_comentario_deletar} foi removido!")
                else:
                    print(f"\nAviso: Não foi encontrado o comentário {id_comentario_deletar} para este jogo.")

            elif opcao == "3":
                cursor.execute("SELECT id_jogo, titulo FROM jogos")
                jogos = cursor.fetchall()
                
                if not jogos:
                    print("\nNenhum jogo cadastrado no sistema.")
                    cursor.close()
                    conn.close()
                    continue
                
                print("\n--- JOGOS CADASTRADOS ---")
                for j in jogos:
                    print(f"ID: {j['id_jogo']} | Título: {j['titulo']}")
                
                try:
                    id_alvo = int(input("\nDigite o ID do jogo que deseja deletar: ").strip())
                except ValueError:
                    print("Erro: O ID precisa ser um número.")
                    cursor.close()
                    conn.close()
                    continue
                
                cursor.execute("DELETE FROM jogos WHERE id_jogo = %s", (id_alvo,))
                conn.commit()
                
                if cursor.rowcount > 0:
                    print(f"\nSucesso: Jogo com ID {id_alvo} foi removido.")
                else:
                    print(f"\nAviso: Nenhum jogo encontrado com o ID {id_alvo}.")
            
            elif opcao == "4":
                cursor.close()
                conn.close()
                inserir_jogos()
                continue
            else:
                print("\nOpção inválida! Digite apenas números")

        except Error as e:
            print(f"\nErro no banco de dados: {e}")
        finally:
            if conn.is_connected():
                cursor.close()
                conn.close()

def exibir_menu():
    print("\n==== MENU ====")
    print("1 - Criar Conta")
    print("2 - Fazer Login")
    print("3 - Editar Conta")
    print("4 - Listar os jogos")
    print("5 - Analisar o Pc")
    print("0 - Sair")
    print()
    print("====== Menu ADMS ======")
    print("6 - Abrir Menu Banco de Dados")
    print("7 - Criar tabelas")

# Execução inicial para garantir que as tabelas existam
criar_tabela()

conta_criada = False
usuario_atual = ""

while True:
    exibir_menu()
    print()
    opcao = input("Escolha uma opcao: ").strip()
    print()

    if opcao == "1":
        padrao = r"^[\w\.-]+@[\w\.-]+\.\w+$"
        print("\n--- CADASTRO DE NOVA CONTA ---")
        nome_digitado = input("Nome de usuário: ").strip()
        email_digitado = input("E-mail: ").strip()

        if not re.match(padrao, email_digitado):
            print("\nEmail inválido, tente novamente!\n")
            continue

        senha_digitada = input("Senha: ").strip()
        sucesso = criar_conta(nome_digitado, email_digitado, senha_digitada)

        if sucesso:
            conta_criada = True
            usuario_atual = nome_digitado

    elif opcao == "2":
        if conta_criada:
            print(f"Você já está logado como '{usuario_atual}'!")
        else:
            sucesso, nome_logado = fazer_login()
            if sucesso:
                conta_criada = True
                usuario_atual = nome_logado

    elif opcao == "3":
        if not conta_criada:
            print("Acesso negado, crie uma conta primeiro para continuar!")
        else:
            editar_perfil()

    elif opcao == "4":
        if not conta_criada:
            print('Acesso negado, por favor, crie uma conta para prosseguir!')
        else:
            listar_jogos()

    elif opcao == "5":
        if not conta_criada:
            print('Acesso negado, por favor, crie uma conta para prosseguir!')
        else:
            verificar_requisitos()

    elif opcao == "6":
        gerenciar_banco()

    elif opcao == "7":
        criar_tabela()
        print("Tabelas criadas com sucesso!")
        
    elif opcao == "0":
        print('Saindo...')
        break
    else:
        print('Opção inválida!')
