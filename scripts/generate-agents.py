#!/usr/bin/env python3
"""Генерация тонких обёрток субагентов для разных ИИ-инструментов.

Единственная копия промпта каждой роли — agents/roles/<роль>.md.
Сгенерированные файлы содержат только настройки инструмента (права, модели,
списки инструментов) и отсылают субагента к файлу роли: он читает своё ТЗ
при старте (все роли имеют инструменты чтения файлов).

Выходные файлы:
  .opencode/agents/<id>.md  — OpenCode V2 (description, mode, permissions)
  .claude/agents/<id>.md    — Claude Code (name, description, tools, model)
  .qwen/agents/<id>.md      — Qwen Code (name, description, tools, approvalMode)
  .agents/<id>.ts           — Freebuff / Codebuff (AgentDefinition)
  .codex/agents/<id>.toml   — Codex (name, description, developer_instructions, sandbox_mode)

Запуск: python3 scripts/generate-agents.py [--check]
  --check — проверить, что сгенерированные файлы актуальны (для CI), ничего не писать.
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
ROLES_DIR = ROOT / "agents" / "roles"

ROLES = ["director", "researcher", "business-analyst", "architect", "developer", "tester"]

ROLE_TITLES = {
    "director": "Директор проекта",
    "researcher": "Ресерчер темы",
    "business-analyst": "Бизнес-аналитик",
    "architect": "Архитектор",
    "developer": "Программист",
    "tester": "Тестировщик",
}


def role_body(role_id: str) -> str:
    """Короткий промпт-обёртка: субагент читает полное ТЗ из файла роли."""
    title = ROLE_TITLES[role_id]
    return (
        f"Ты — {title} проекта. Твоё полное ТЗ — файл agents/roles/{role_id}.md "
        "в корне репозитория: прочитай его целиком первым же действием и действуй "
        "строго по нему. Контекст проекта — в AGENTS.md, тоже прочитай. "
        "Если какой-то из файлов недоступен — сообщи об этом и остановись."
    )


def oc_perm(action: str, resource: str, effect: str) -> str:
    return f"  - action: {action}\n    resource: \"{resource}\"\n    effect: {effect}"


# ---------------------------------------------------------------------------
# Описания для автоделегирования (видит модель, выбирающая субагента)
# ---------------------------------------------------------------------------

DESCRIPTIONS = {
    "director": (
        "Директор проекта: декомпозирует задачу, составляет план и оркестрирует "
        "работу остальных субагентов (researcher, business-analyst, architect, "
        "developer, tester), принимает результаты по критериям готовности. "
        "MUST BE USED as the lead/orchestrator for multi-step project work."
    ),
    "researcher": (
        "Ресерчер темы: исследует в вебе рынок, аналогов, технологии и регуляторику, "
        "готовит отчёт со ссылками на проверенные источники. "
        "Use PROACTIVELY for any research or competitive analysis question."
    ),
    "business-analyst": (
        "Бизнес-аналитик: формулирует требования, user stories с критериями "
        "приёмки Given/When/Then, глоссарий домена и описание процессов. "
        "MUST BE USED before implementing any new feature."
    ),
    "architect": (
        "Архитектор: проектирует компоненты, датамодель, API-контракты, пишет ADR "
        "и обосновывает trade-offs. "
        "MUST BE USED before starting implementation of significant features."
    ),
    "developer": (
        "Программист: реализует задачи по коду строго по архитектуре и conventions "
        "проекта, с тестами и прогоном линтеров перед сдачей."
    ),
    "tester": (
        "Тестировщик: составляет тест-планы и кейсы (включая граничные случаи "
        "домена сверки), пишет и запускает автотесты, готовит отчёты о дефектах "
        "и вердикт о готовности. Use after each implementation task."
    ),
}

# ---------------------------------------------------------------------------
# OpenCode V2: .opencode/agents/<id>.md
# ---------------------------------------------------------------------------

OPENCODE = {
    "director": {
        "mode": "all",
        "color": "#a855f7",
        "permissions": [
            oc_perm("edit", "*", "allow"),
            oc_perm("shell", "*", "deny"),
        ],
    },
    "researcher": {
        "mode": "subagent",
        "color": "#0ea5e9",
        "permissions": [
            oc_perm("edit", "*", "deny"),
            oc_perm("shell", "*", "deny"),
        ],
    },
    "business-analyst": {
        "mode": "subagent",
        "color": "#f59e0b",
        "permissions": [
            oc_perm("edit", "*", "deny"),
            oc_perm("edit", "docs/**", "allow"),
            oc_perm("shell", "*", "deny"),
        ],
    },
    "architect": {
        "mode": "subagent",
        "color": "#8b5cf6",
        "permissions": [
            oc_perm("edit", "*", "deny"),
            oc_perm("edit", "docs/**", "allow"),
            oc_perm("shell", "*", "deny"),
        ],
    },
    "developer": {
        "mode": "subagent",
        "color": "#22c55e",
        "permissions": [
            oc_perm("shell", "git push*", "deny"),
        ],
    },
    "tester": {
        "mode": "subagent",
        "color": "#ef4444",
        "permissions": [
            oc_perm("shell", "git push*", "deny"),
        ],
    },
}


def render_opencode(role_id: str) -> str:
    cfg = OPENCODE[role_id]
    lines = [
        "---",
        f"description: {DESCRIPTIONS[role_id]}",
        f"mode: {cfg['mode']}",
        f"color: \"{cfg['color']}\"",
    ]
    if cfg.get("permissions"):
        lines.append("permissions:")
        lines.extend(cfg["permissions"])
    lines.append("---")
    lines.append("")
    lines.append(role_body(role_id))
    return "\n".join(lines) + "\n"


# ---------------------------------------------------------------------------
# Claude Code: .claude/agents/<id>.md
# ---------------------------------------------------------------------------

CLAUDE = {
    "director": {
        "tools": ["Task", "Read", "Glob", "Grep", "WebSearch", "WebFetch", "Write", "Edit"],
    },
    "researcher": {
        "tools": ["Read", "Glob", "Grep", "WebSearch", "WebFetch"],
    },
    "business-analyst": {
        "tools": ["Read", "Glob", "Grep", "WebSearch", "WebFetch", "Write", "Edit"],
    },
    "architect": {
        "tools": ["Read", "Glob", "Grep", "WebSearch", "WebFetch", "Write", "Edit"],
    },
    "developer": {
        "tools": ["Read", "Edit", "Write", "Glob", "Grep", "Bash", "WebSearch", "WebFetch"],
    },
    "tester": {
        "tools": ["Read", "Edit", "Write", "Glob", "Grep", "Bash"],
    },
}


def render_claude(role_id: str) -> str:
    cfg = CLAUDE[role_id]
    lines = [
        "---",
        f"name: {role_id}",
        f"description: {DESCRIPTIONS[role_id]}",
        "tools: " + ", ".join(cfg["tools"]),
        "model: inherit",
        "---",
        "",
        role_body(role_id),
    ]
    return "\n".join(lines) + "\n"


# ---------------------------------------------------------------------------
# Qwen Code: .qwen/agents/<id>.md
# ---------------------------------------------------------------------------

QWEN = {
    "director": {
        "tools": ["read_file", "read_many_files", "grep_search", "glob",
                  "web_search", "web_fetch", "write_file", "edit"],
        "approvalMode": "default",
    },
    "researcher": {
        "tools": ["read_file", "read_many_files", "grep_search", "glob",
                  "web_search", "web_fetch"],
        "approvalMode": "plan",
    },
    "business-analyst": {
        "tools": ["read_file", "read_many_files", "grep_search", "glob",
                  "web_search", "web_fetch", "write_file", "edit"],
        "approvalMode": "auto-edit",
    },
    "architect": {
        "tools": ["read_file", "read_many_files", "grep_search", "glob",
                  "web_search", "web_fetch", "write_file", "edit"],
        "approvalMode": "auto-edit",
    },
    "developer": {
        "tools": None,  # наследует все инструменты родительской сессии
        "approvalMode": "auto-edit",
    },
    "tester": {
        "tools": ["read_file", "read_many_files", "grep_search", "glob",
                  "write_file", "edit", "run_shell_command"],
        "approvalMode": "auto-edit",
    },
}


def render_qwen(role_id: str) -> str:
    cfg = QWEN[role_id]
    lines = [
        "---",
        f"name: {role_id}",
        f"description: {DESCRIPTIONS[role_id]}",
        "model: inherit",
    ]
    if cfg["tools"]:
        lines.append("tools:")
        lines.extend(f"  - {t}" for t in cfg["tools"])
    lines.append(f"approvalMode: {cfg['approvalMode']}")
    lines.append("---")
    lines.append("")
    lines.append(role_body(role_id))
    return "\n".join(lines) + "\n"


# ---------------------------------------------------------------------------
# Freebuff / Codebuff: .agents/<id>.ts — AgentDefinition
# ---------------------------------------------------------------------------

FREEBUFF = {
    "director": {
        "model": "anthropic/claude-sonnet-4.6",
        "tools": ["read_files", "glob", "code_search", "web_search", "read_url",
                  "write_file", "spawn_agents"],
        "spawnable": ["researcher", "business-analyst", "architect", "developer", "tester"],
    },
    "researcher": {
        "model": "google/gemini-3-flash-preview",
        "tools": ["read_files", "glob", "code_search", "web_search", "read_url"],
        "spawnable": [],
    },
    "business-analyst": {
        "model": "google/gemini-3-flash-preview",
        "tools": ["read_files", "glob", "code_search", "web_search", "read_url",
                  "write_file", "str_replace"],
        "spawnable": [],
    },
    "architect": {
        "model": "google/gemini-3.1-pro-preview",
        "tools": ["read_files", "glob", "code_search", "web_search", "read_url",
                  "write_file", "str_replace"],
        "spawnable": [],
    },
    "developer": {
        "model": "anthropic/claude-sonnet-4.6",
        "tools": ["read_files", "glob", "code_search", "web_search", "read_url",
                  "write_file", "str_replace", "apply_patch", "run_terminal_command"],
        "spawnable": [],
    },
    "tester": {
        "model": "google/gemini-3-flash-preview",
        "tools": ["read_files", "glob", "code_search", "read_url",
                  "write_file", "str_replace", "run_terminal_command"],
        "spawnable": [],
    },
}

SPAWNER_PROMPTS = {
    "director": ("Директор проекта: декомпозирует задачу, оркестрирует остальных "
                 "субагентов и принимает результаты. Использовать как ведущего агента "
                 "для многоэтапной работы."),
    "researcher": "Исследование темы в вебе: рынок, аналоги, технологии, регуляторика. Делегировать любые ресерч-вопросы.",
    "business-analyst": "Формулирование требований, user stories, глоссария и процессов домена. Вызывать перед реализацией новой фичи.",
    "architect": "Проектирование архитектуры, датамодели и API-контрактов, написание ADR. Вызывать до начала реализации значимых фич.",
    "developer": "Реализация задач по коду по архитектуре и conventions проекта.",
    "tester": "Тест-планы, тест-кейсы, автотесты, отчёты о дефектах и вердикт о готовности. Вызывать после каждой задачи реализации.",
}


def ts_multiline(text: str) -> str:
    """Строка для TS-шаблонного литерала с экранированием."""
    escaped = text.replace("\\", "\\\\").replace("`", "\\`").replace("${", "\\${")
    return "`" + escaped + "`"


def render_freebuff(role_id: str) -> str:
    cfg = FREEBUFF[role_id]
    input_desc = "Подробное ТЗ для агента: контекст, что сделать, где искать вводные, ожидаемый артефакт и критерии готовности."
    tool_list = ", ".join(f"'{t}'" for t in cfg["tools"])
    var = role_id.replace("-", "_")
    lines = [
        "// Сгенерировано scripts/generate-agents.py — не редактировать вручную.",
        "// Полное ТЗ роли: agents/roles/" + role_id + ".md (агент читает его при старте).",
        "// Для типизации можно добавить: import type { AgentDefinition } from './types/agent-definition'",
        "",
        f"const {var} = {{",
        f"  id: '{role_id}',",
        f"  displayName: '{ROLE_TITLES[role_id]}',",
        f"  model: '{cfg['model']}',  // при необходимости замените на другую модель OpenRouter/Freebuff",
        f"  toolNames: [{tool_list}],",
    ]
    if cfg["spawnable"]:
        spawn_list = ", ".join(f"'{a}'" for a in cfg["spawnable"])
        lines.append(f"  spawnableAgents: [{spawn_list}],")
    lines.extend([
        "  inputSchema: {",
        "    prompt: {",
        "      type: 'string',",
        f"      description: {ts_multiline(input_desc)},",
        "    },",
        "  },",
        "  includeMessageHistory: false,",
        f"  spawnerPrompt: {ts_multiline(SPAWNER_PROMPTS[role_id])},",
        f"  instructionsPrompt: {ts_multiline(role_body(role_id))},",
        "}",
        "",
        f"export default {var}",
    ])
    return "\n".join(lines) + "\n"


# ---------------------------------------------------------------------------
# Codex: .codex/agents/<id>.toml
# ---------------------------------------------------------------------------

# sandbox_mode: read-only / workspace-write (в остальных настройках наследует
# родительскую сессию; модель и effort не задаём — наследуются).
CODEX_SANDBOX = {
    "director": "workspace-write",
    "researcher": "read-only",
    "business-analyst": "workspace-write",
    "architect": "workspace-write",
    "developer": "workspace-write",
    "tester": "workspace-write",
}


def toml_str(text: str) -> str:
    escaped = text.replace("\\", "\\\\").replace('"', '\\"')
    return f'"{escaped}"'


def render_codex(role_id: str) -> str:
    lines = [
        f'name = "{role_id}"',
        f"description = {toml_str(DESCRIPTIONS[role_id])}",
        f'sandbox_mode = "{CODEX_SANDBOX[role_id]}"',
        'developer_instructions = """',
        role_body(role_id),
        '"""',
    ]
    return "\n".join(lines) + "\n"


TARGETS = [
    (ROOT / ".opencode" / "agents", render_opencode, "md"),
    (ROOT / ".claude" / "agents", render_claude, "md"),
    (ROOT / ".qwen" / "agents", render_qwen, "md"),
    (ROOT / ".agents", render_freebuff, "ts"),
    (ROOT / ".codex" / "agents", render_codex, "toml"),
]


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true",
                        help="только проверить актуальность, не записывать")
    args = parser.parse_args()

    missing_roles = [r for r in ROLES if not (ROLES_DIR / f"{r}.md").exists()]
    if missing_roles:
        print("Нет файлов ролей: " + ", ".join(missing_roles), file=sys.stderr)
        return 1

    stale: list[Path] = []
    for directory, render, ext in TARGETS:
        for role_id in ROLES:
            target = directory / f"{role_id}.{ext}"
            content = render(role_id)
            if args.check:
                if not target.exists() or target.read_text(encoding="utf-8") != content:
                    stale.append(target)
            else:
                target.parent.mkdir(parents=True, exist_ok=True)
                target.write_text(content, encoding="utf-8")
                print(f"written: {target.relative_to(ROOT)}")

    if args.check:
        if stale:
            for path in stale:
                print(f"stale: {path.relative_to(ROOT)}", file=sys.stderr)
            print("Запустите: python3 scripts/generate-agents.py", file=sys.stderr)
            return 1
        print("OK: все сгенерированные файлы актуальны")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
