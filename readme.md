# OneLive 2.0

**OneLive** — это «весёлый» Python-раннер: запускает `.py` файл, модуль (`-m`) или команду (`-c`), а при ошибках может автоматически вызывать `curl` с ASCII-анимацией.

## Что обновлено (2026)

- Современный CLI на `argparse`.
- Поддержка запуска файла, модуля и inline-команды.
- Гибкая обработка ошибок и опциональный traceback.
- Настраиваемый URL для fallback-команды.
- Улучшенная сборка в standalone executable (`.exe`) через **PyInstaller**.
- Добавлены dev-инструменты: `pytest`, `ruff`.

## Требования

- Python **3.12+**
- `curl` (если используете рикролл-режим)

## Быстрый старт

```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -U pip
pip install -r requirements-dev.txt
```

Запуск файла:

```bash
python onelive.py script.py
```

Запуск модуля:

```bash
python onelive.py -m http.server
```

Запуск inline-кода:

```bash
python onelive.py -c "print('Hello from OneLive')"
```

Отключить curl fallback:

```bash
python onelive.py broken.py --no-rickroll
```

Показать traceback:

```bash
python onelive.py broken.py --traceback
```

## Сборка `.exe`

### Вариант 1: через скрипт

```bash
python scripts/build_exe.py --clean --name onelive
```

После сборки бинарник появится в `dist/`:

- Windows: `dist/onelive.exe`
- Linux/macOS: `dist/onelive`

### Вариант 2: вручную через PyInstaller

```bash
python -m PyInstaller --onefile --console --name onelive onelive.py
```

## Проверки качества

```bash
python -m pytest
python -m ruff check .
```

## Примечания

- Если `curl` не установлен, OneLive покажет предупреждение и завершит fallback без падения приложения.
- Сборка должна выполняться на целевой ОС (для `.exe` — на Windows).
