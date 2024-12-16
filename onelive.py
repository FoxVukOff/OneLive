import subprocess
import sys

def run_code_with_error_handling(file_path):
    try:
        # Открытие и выполнение файла .py
        with open(file_path, 'r') as file:
            code = file.read()
        exec(code)
    except SyntaxError as e:
        # При синтаксической ошибке выполняем команду curl
        print(f"Ошибка синтаксиса: {e}")
        print("Открываю командную строку...")
        subprocess.run(["curl", "ASCII.live/can-you-hear-me"])
    except NameError as e:
        # Если вызывается несуществующая функция или переменная
        print(f"Ошибка: {e}")
        print("Открываю командную строку...")
        subprocess.run(["curl", "ASCII.live/can-you-hear-me"])
    except Exception as e:
        # Обработка других ошибок
        print(f"Произошла ошибка: {e}")
        subprocess.run(["curl", "ASCII.live/can-you-hear-me"])

if __name__ == "__main__":
    # Проверка, что путь к файлу передан
    if len(sys.argv) != 2:
        print("Использование: python onelive.py <путь к файлу .py>")
    else:
        file_path = sys.argv[1]
        run_code_with_error_handling(file_path)
