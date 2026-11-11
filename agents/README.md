# Агенты проекта

Команда ИИ-субагентов для проекта «AI-агент для бэк-офиса брокера» (разбор
расхождений после сверки сделок). Контекст проекта и правила — в корневом
[`AGENTS.md`](../AGENTS.md).

## Зачем такая структура

В проекте используется несколько ИИ-инструментов (OpenCode, Freebuff, Claude Code,
Qwen Code, Codex, Gemini CLI), у каждого — свой формат описания субагентов.
Чтобы промпт роли существовал в одном экземпляре, полное ТЗ лежит в
`agents/roles/<роль>.md`, а файлы для конкретных инструментов — тонкие обёртки,
которые генерирует скрипт `scripts/generate-agents.py`: субагент читает своё ТЗ
из файла роли при старте.

```
agents/roles/*.md      ← полный промпт роли — единственная копия (править здесь)
.opencode/agents/*.md  ← тонкие обёртки: права/модели для OpenCode V2
.codex/agents/*.toml   ← тонкие обёртки (TOML) для Codex
.claude/agents/*.md    ← тонкие обёртки для Claude Code
.qwen/agents/*.md      ← тонкие обёртки для Qwen Code
.agents/*.ts           ← тонкие обёртки (AgentDefinition) для Freebuff / Codebuff
```

## Роли

| Файл | ID | Суть |
| --- | --- | --- |
| `roles/director.md` | `director` | Оркестратор: план, делегирование, приёмка |
| `roles/researcher.md` | `researcher` | Веб-ресерч темы, отчёт с источниками |
| `roles/business-analyst.md` | `business-analyst` | Требования, user stories, глоссарий |
| `roles/architect.md` | `architect` | Архитектура, датамодель, контракты, ADR |
| `roles/developer.md` | `developer` | Реализация кода с тестами и линтерами |
| `roles/tester.md` | `tester` | Тест-планы, автотесты, отчёты о дефектах |

## Как менять роль

1. Текст роли — правь только `agents/roles/<роль>.md`; перегенерация не нужна.
2. Права/инструменты/модели роли — в `scripts/generate-agents.py`
   (секции `OPENCODE`, `CODEX`, `CLAUDE`, `QWEN`, `FREEBUFF`), затем
   `python3 scripts/generate-agents.py`.

Проверка актуальности (для CI): `python3 scripts/generate-agents.py --check`.

## Права ролей (кратко)

- `researcher` — только чтение и веб, файлы не меняет.
- `business-analyst`, `architect` — пишут только в `docs/**`.
- `developer`, `tester` — полный доступ к рабочей области, но без `git push`.
- `director` — может писать планы, запускать субагентов, но не выполняет
  shell-команды сам.
