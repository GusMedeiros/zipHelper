import threading
import time
import rarfile
import os


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


class RARHelper:
    total = 1
    progresso = 1
    rar_name = 1
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
    def calc_decompressed_size(cls, rar_file_path):
        with rarfile.RarFile(rar_file_path, 'r') as rar_ref:
            for file_info in rar_ref.infolist():
                cls.total += file_info.file_size

    @classmethod
    def print_ui(cls):
        while not cls.terminou:
            os.system('cls')
            print(f"Descompactando {cls.rar_name}")
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
        rarfile.UNRAR_TOOL = "C:\\Program Files\\WinRAR\\UnRAR.exe"
        try:
            cls.calc_decompressed_size(path)
            with rarfile.RarFile(path, 'r') as rar_ref:
                cls.rar_name = rar_ref.filename
                info_list = rar_ref.infolist()
                for info in info_list:
                    if info.filename.endswith("/"):
                        continue
                    cls.arquivo_atual = info.filename
                    with rar_ref.open(info.filename) as file:
                        cur_file_path = os.path.join(destination, info.filename)
                        # Ensure directory exists first
                        cls.cria_diretorios(cur_file_path)
                        # If the file exists and has been completely extracted, skip extraction
                        if os.path.exists(cur_file_path) and info.file_size == os.path.getsize(cur_file_path):
                            cls.progresso += info.file_size
                            continue
                        # Otherwise, extract to the destination
                        with open(cur_file_path, 'wb') as target:
                            file = rar_ref.open(info.filename)
                            if file is None or file.closed:
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