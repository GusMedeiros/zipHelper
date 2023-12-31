import threading
import time
import zipfile
import os
import sys

import RARHelper


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


class ZipHelper:
    total = 1
    progresso = 1
    zip_name = 1
    terminou = False
    arquivo_atual = None

    @classmethod
    def display_progress_bar(cls):
        bar_length = 28
        progress_ratio = cls.progresso / cls.total
        filled_length = int(bar_length * progress_ratio)

        bar = '\033[32m█\033[0m' * filled_length + '-' * (bar_length - filled_length)

        print(f'|{bar}| {progress_ratio * 100:.1f}%')

    @classmethod
    def calc_decompressed_size(cls, zip_file_path):
        with zipfile.ZipFile(zip_file_path, 'r') as zip_ref:
            for file_info in zip_ref.infolist():
                cls.total += file_info.file_size

    @classmethod
    def print_ui(cls):
        while not cls.terminou:
            os.system('cls')
            print(f"Descompactando {cls.zip_name}")
            print(f"Arquivo atual: {cls.arquivo_atual}")
            print(f"Progresso: {cls.progresso / 1024 / 1024:.1f}/{cls.total / 1024 / 1024:.1f}MB")
            cls.display_progress_bar()
            time.sleep(0.2)
        os.system('cls')
        os.system('cls')
        print(f"Progresso: {cls.progresso / 1024 / 1024:.1f}/{cls.total / 1024 / 1024:.1f}MB")
        cls.display_progress_bar()
        print("\033[32mExtração finalizada. Saindo\033[0m")
        time.sleep(1)

    @staticmethod
    def cria_diretorios(path):
        if not path.endswith('/') and not path.endswith('\\'):
            path = os.path.dirname(path)
        try:
            os.makedirs(path)
        finally:
            return

    @classmethod
    def extract_in_chunks(cls, path, destination, chunk_size_bytes: int):
        try:
            cls.calc_decompressed_size(path)
            with zipfile.ZipFile(path, 'r') as zip_ref:
                cls.zip_name = zip_ref.filename
                info_list = zip_ref.infolist()
                for info in info_list:
                    if info.filename.endswith("/"):
                        continue
                    cls.arquivo_atual = info.filename
                    with zip_ref.open(info.filename) as file:
                        cur_file_path = os.path.join(destination, file.name)
                        # primeiro garante que diretorio existe
                        cls.cria_diretorios(cur_file_path)
                        # depois, se arquivo já existe e foi totalmente extraído, não precisa extrair dnv
                        if os.path.exists(cur_file_path) and info.file_size == os.path.getsize(cur_file_path):
                            cls.progresso += info.file_size
                            continue
                        # do contrário, extraimos no destino
                        with open(os.path.join(destination, file.name.replace("/", "\\")), 'wb') as target:
                            if target is None:
                                break
                            while True:
                                chunk = file.read(chunk_size_bytes)
                                if not chunk:
                                    break
                                target.write(chunk)
                                cls.progresso += len(chunk)
                cls.terminou = True
        except Exception as e:
            log_exception(e)


gb = 1024 * 1024 * 1
input_file_path = sys.argv[1]
destination_path, n = os.path.splitext(input_file_path)
os.makedirs(destination_path, exist_ok=True)
if input_file_path.endswith(".rar"):
    from RARHelper import RARHelper
    extract_thread = threading.Thread(target=RARHelper.extract_in_chunks, args=(input_file_path, destination_path, gb))
    print_ui_thread = threading.Thread(target=RARHelper.print_ui)

    extract_thread.start()
    print_ui_thread.start()

    extract_thread.join()
    print_ui_thread.join()

elif input_file_path.endswith(".zip"):
    extract_thread = threading.Thread(target=ZipHelper.extract_in_chunks, args=(input_file_path, destination_path, gb))
    print_ui_thread = threading.Thread(target=ZipHelper.print_ui)
    extract_thread.start()
    print_ui_thread.start()
    extract_thread.join()
    print_ui_thread.join()
else:
    input("Arquivo não suportado. Aperte enter para sair")
