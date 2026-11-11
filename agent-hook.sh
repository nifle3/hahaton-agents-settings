#!/usr/bin/env bash
#
# agent-hook.sh — общий хук-хаб для агентных CLI (Claude Code, Codex, Qwen Code, OpenCode).
#
# Вся логика «после правки файла агентом» живёт здесь и не дублируется
# в конфигах инструментов: они лишь вызывают этот скрипт.
#
# Режимы запуска:
#   1) agent-hook.sh < JSON          — режим хука: JSON события на stdin
#      (формат Claude Code / Codex / Qwen: tool_input.file_path или file_path).
#   2) agent-hook.sh format <файл>   — режим форматтера OpenCode: путь файла в аргументе.
#
# Зависимость: jq (только для режима 1; при отсутствии — хук молча пропускается).
# Инструменты (gofmt, ruff, prettier) подбираются по расширению файла;
# отсутствующий инструмент пропускается с предупреждением в stderr.

set -u

MODE="${1:-}"

# --- Определяем файл --------------------------------------------------------

if [ "$MODE" = "format" ]; then
    # Режим 2: форматтер OpenCode (agent-hook.sh format "$FILE")
    FILE="${2:-}"
else
    # Режим 1: читаем JSON события со stdin
    if ! command -v jq >/dev/null 2>&1; then
        echo "agent-hook.sh: jq не найден, хук пропущен" >&2
        exit 0
    fi
    INPUT="$(cat)"
    FILE="$(printf '%s' "$INPUT" | jq -r '.tool_input.file_path // .file_path // empty' 2>/dev/null || true)"
fi

if [ -z "$FILE" ] || [ ! -f "$FILE" ]; then
    exit 0
fi

# --- Корень проекта ---------------------------------------------------------

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$ROOT" || exit 0

EXT="${FILE##*.}"

warn() { echo "agent-hook.sh: $1" >&2; }

run_tool() {
    if command -v "$1" >/dev/null 2>&1; then
        "$@" || true   # ошибки инструмента не блокируют хук
    else
        warn "$1 не найден, пропуск"
    fi
}

# --- Диспетчеризация по расширению ------------------------------------------

case "$EXT" in
    go)
        run_tool gofmt -w "$FILE"
        ;;
    py|pyi)
        run_tool ruff format "$FILE"
        run_tool ruff check --fix "$FILE"
        ;;
    ts|tsx|mts|cts|js|jsx|mjs|cjs)
        # prettier берём локальный (node_modules), затем глобальный
        if [ -x "node_modules/.bin/prettier" ]; then
            node_modules/.bin/prettier --write "$FILE" || true
        elif command -v prettier >/dev/null 2>&1; then
            prettier --write "$FILE" || true
        else
            warn "prettier не найден, пропуск"
        fi
        ;;
    json)
        # Форматируем только JSON в проектных каталогах, не трогаем конфиги инструментов
        case "$FILE" in
            *node_modules*|*vendor*) exit 0 ;;
            *) ;;
        esac
        if [ -x "node_modules/.bin/prettier" ]; then
            node_modules/.bin/prettier --write "$FILE" || true
        elif command -v prettier >/dev/null 2>&1; then
            prettier --write "$FILE" || true
        fi
        ;;
    *)
        # Неподдерживаемое расширение — ничего не делаем
        exit 0
        ;;
esac

# Хук «после правки» не возвращает вердиктов: всегда успех.
exit 0
