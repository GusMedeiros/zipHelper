import os
import shutil


def log_exception(e):
    import traceback

    # Nome do arquivo onde o log será salvo
    nome_arquivo = 'log_de_exceptions.txt'

    # Abre o arquivo no modo de adicionar ('a') para adicionar informações ao final do arquivo
    with open(nome_arquivo, 'a') as arquivo:
        # Obtém o stack trace como uma string
        stack_trace = traceback.format_exc()

        # Escreve o stack trace no arquivo
        arquivo.write("Exceção:\n")
        arquivo.write(str(e) + '\n')
        arquivo.write("Traceback:\n")
        arquivo.write(stack_trace + '\n')
        arquivo.write("=" * 50 + '\n')


try:
    caminho = 'C:\\Program Files\\'
    print("Diretório atual: " + os.getcwd())
    print(f"Instalando o zipHelper em {caminho}")
    resposta = input(
        "Pressione 'S' para aceitar, 'N' para mudar o caminho, ou 'Q' para cancelar a instalação: ").lower()

    if resposta == "n":
        resposta = input("Insira o novo caminho ou 'Q' para cancelar a instalação: ").lower()
        if resposta == "q":
            exit()
        else:
            caminho = resposta
    elif resposta == "q":
        exit()

    if not os.path.exists(caminho):
        print(f"{caminho} não existe. Criando diretórios")
        os.makedirs(caminho)

    arquivo_origem = f"zipHelper"
    if not os.path.exists(arquivo_origem):
        print(f"zipHelper não encontrado em {os.getcwd()}")

    if os.path.exists(arquivo_origem):
        if os.path.exists(caminho+arquivo_origem):
            print("Instalação antiga detectada. Deletando")
            shutil.rmtree(caminho+arquivo_origem)
            print("Instalação antiga removida.")
        print(f"Copiando {os.getcwd()}{arquivo_origem} para {caminho}")
        shutil.move(arquivo_origem, caminho)
        print("Arquivo movido com sucesso!")
        import add_extract_option
        input("Insira qualquer coisa para continuar")
        add_extract_option.run(caminho+arquivo_origem+"\\zipHelper.exe", caminho+arquivo_origem+"\\xibo.ico")
    else:
        print(f"Erro: arquivo de origem '{arquivo_origem}' não encontrado.")
    input("Instalação finalizada. Aperte enter para sair")

except Exception as e:
    log_exception(e)
    input("Erro na instalação. O log do erro foi salvo na pasta.")
