#!/usr/bin/env python3
"""OneLive — playful Python runner with improved diagnostics and fallback actions."""

from __future__ import annotations

import argparse
import os
import pathlib
import runpy
import subprocess
import sys
import traceback
from dataclasses import dataclass
from typing import Iterable

RICKROLL_URL = "ASCII.live/can-you-hear-me"


@dataclass(slots=True)
class Config:
    """Runtime settings for OneLive."""

    no_rickroll: bool = False
    timeout: int = 15
    show_traceback: bool = False
    cwd: str | None = None


def trigger_rickroll(config: Config) -> int:
    """Run curl animation command and return process exit code."""
    if config.no_rickroll:
        return 0

    print(f"[OneLive] Запускаю: curl {RICKROLL_URL}")
    try:
        process = subprocess.run(
            ["curl", RICKROLL_URL],
            check=False,
            timeout=config.timeout,
        )
        return process.returncode
    except FileNotFoundError:
        print("[OneLive] Команда curl не найдена. Установите curl или используйте --no-rickroll.")
        return 127
    except subprocess.TimeoutExpired:
        print(f"[OneLive] curl превысил лимит {config.timeout} сек.")
        return 124


def execute_source(source: str, origin: str, config: Config, script_argv: list[str] | None = None) -> int:
    """Execute user Python source and handle exceptions."""
    namespace = {"__name__": "__main__", "__file__": origin}
    old_argv = sys.argv[:]
    old_cwd = pathlib.Path.cwd()

    sys.argv = [origin, *(script_argv or [])]
    if config.cwd:
        os.chdir(config.cwd)

    try:
        compiled = compile(source, origin, "exec")
        exec(compiled, namespace)
        return 0
    except (SyntaxError, NameError, ImportError, ZeroDivisionError, ValueError) as exc:
        print(f"[OneLive] Перехвачена ошибка: {exc.__class__.__name__}: {exc}")
        if config.show_traceback:
            traceback.print_exc()
        trigger_rickroll(config)
        return 1
    except Exception as exc:  # noqa: BLE001
        print(f"[OneLive] Неожиданная ошибка: {exc.__class__.__name__}: {exc}")
        if config.show_traceback:
            traceback.print_exc()
        trigger_rickroll(config)
        return 1
    finally:
        sys.argv = old_argv
        if config.cwd:
            os.chdir(old_cwd)


def run_file(path: pathlib.Path, config: Config, script_argv: list[str] | None = None) -> int:
    """Execute Python file by path."""
    if not path.exists():
        print(f"[OneLive] Файл не найден: {path}")
        return 2

    source = path.read_text(encoding="utf-8")
    return execute_source(source=source, origin=str(path), config=config, script_argv=script_argv)


def run_module(module_name: str, config: Config, script_argv: list[str] | None = None) -> int:
    """Execute module with runpy and process errors uniformly."""
    old_argv = sys.argv[:]
    old_cwd = pathlib.Path.cwd()

    sys.argv = [module_name, *(script_argv or [])]
    if config.cwd:
        os.chdir(config.cwd)

    try:
        runpy.run_module(module_name, run_name="__main__")
        return 0
    except Exception as exc:  # noqa: BLE001
        print(f"[OneLive] Ошибка модуля {module_name}: {exc.__class__.__name__}: {exc}")
        if config.show_traceback:
            traceback.print_exc()
        trigger_rickroll(config)
        return 1
    finally:
        sys.argv = old_argv
        if config.cwd:
            os.chdir(old_cwd)


def parse_args(argv: Iterable[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        prog="onelive",
        description="Запускает Python-скрипт/модуль и при ошибках может вызвать ASCII рикролл.",
    )
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("file", nargs="?", help="Путь к .py файлу.")
    mode.add_argument("-m", "--module", help="Имя Python-модуля для запуска.")
    mode.add_argument("-c", "--command", help="Python-код в виде строки для выполнения.")
    parser.add_argument(
        "--no-rickroll",
        action="store_true",
        help="Отключить вызов curl на ошибке.",
    )
    parser.add_argument(
        "--timeout",
        type=int,
        default=15,
        help="Таймаут для curl в секундах (по умолчанию: 15).",
    )
    parser.add_argument(
        "--traceback",
        action="store_true",
        help="Показывать полный traceback при ошибках.",
    )
    parser.add_argument("--cwd", help="Рабочая директория для запуска кода.")
    parser.add_argument("script_args", nargs="*", help="Аргументы, передаваемые выполняемому коду.")
    parser.add_argument("--version", action="version", version="OneLive 2.1.0")
    return parser.parse_args(list(argv))


def main(argv: Iterable[str] | None = None) -> int:
    args = parse_args(argv if argv is not None else sys.argv[1:])
    config = Config(
        no_rickroll=args.no_rickroll,
        timeout=max(1, args.timeout),
        show_traceback=args.traceback,
        cwd=args.cwd,
    )

    if args.command:
        return execute_source(source=args.command, origin="<command>", config=config, script_argv=args.script_args)

    if args.module:
        return run_module(args.module, config, script_argv=args.script_args)

    assert args.file is not None
    return run_file(pathlib.Path(args.file), config=config, script_argv=args.script_args)


if __name__ == "__main__":
    raise SystemExit(main())
