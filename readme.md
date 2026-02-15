# OneLive 2.1

**OneLive** — это «весёлый» Python-раннер: запускает `.py` файл, модуль (`-m`) или команду (`-c`), а при ошибках вызывает **оригинальный рикролл** через `curl ASCII.live/can-you-hear-me`.

## Что обновлено (2026)

- Современный CLI на `argparse`.
- Поддержка запуска файла, модуля и inline-команды.
- Передача аргументов в запускаемый код (`script_args`).
- Опция `--cwd` для запуска скрипта в нужной рабочей директории.
- Гибкая обработка ошибок и опциональный traceback.
- Сборка в standalone executable (`.exe`) через **PyInstaller**.
- Добавлены проверки в **GitHub Actions** (lint, unit-tests, build smoke test).

## Требования

- Python **3.12+**
- `curl` (для рикролл-режима)

## Быстрый старт

```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -U pip
pip install -r requirements-dev.txt
```

## Использование

Запуск файла:

```bash
python onelive.py script.py
```

Запуск файла + аргументы для скрипта:

```bash
python onelive.py script.py arg1 arg2
```

Запуск модуля:

```bash
python onelive.py -m http.server
```

Запуск inline-кода:

```bash
python onelive.py -c "print('Hello from OneLive')"
```

Запуск из другой директории:

```bash
python onelive.py app/main.py --cwd app
```

Отключить рикролл:

```bash
python onelive.py broken.py --no-rickroll
```

Показать traceback:

```bash
python onelive.py broken.py --traceback
```

## Сборка `.exe`

Через скрипт:

```bash
python scripts/build_exe.py --clean --name onelive
```

После сборки бинарник появится в `dist/`:

- Windows: `dist/onelive.exe`
- Linux/macOS: `dist/onelive`

## CI / GitHub Actions

Workflow: `.github/workflows/ci.yml`

Проверяет:

- `ruff check .`
- `unittest`
- smoke build через `scripts/build_exe.py`

## Проверки локально

```bash
python -m unittest discover -s tests -q
python -m ruff check .
```
