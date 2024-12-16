# OneLive

**OneLive** — это рикрольный Python интерпретатор, если находит ошибки синтаксиса в коде то он запускает команду `curl` с рикроллом. Используется для развлечения.

### Описание

Этот компилятор работает как стандартный интерпретатор Python, но с добавлением фичи для обработки синтаксических ошибок и ошибок при вызове неопределенных функций. Вместо обычных сообщений об ошибке, он запускает команду, которая вызывает рикролл через `curl`!

### Как использовать

1. Убедитесь, что у вас установлен Python 3.x.
2. Скачайте или клонируйте репозиторий:
   ```bash
   git clone https://github.com/FoxVukoff/OneLive.git