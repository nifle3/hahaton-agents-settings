# Настройки проекта: окружение, линтеры, тайпчекеры, агентные хуки

Этот репозиторий — стартовый набор настроек, который копируется в новый проект.
Агентные роли и обёртки (`.opencode/`, `.agents/`, `agents/`, `scripts/` и др.)
описаны в [AGENTS.md](AGENTS.md) и здесь не дублируются.

## Состав

| Файл | Назначение |
| --- | --- |
| `.golangci.yml` | golangci-lint v2: линтер + typecheck + vet для Go |
| `pyproject.toml` | ruff (линтер + форматтер) и mypy (тайпчекер) для Python |
| `eslint.config.mjs` | ESLint 9 flat config + typescript-eslint |
| `.prettierrc.json` | Prettier — форматтер TS/JS |
| `tsconfig.json` | строгий тайпчек TypeScript (`tsc --noEmit`) |
| `Makefile` | цели `lint`, `fmt`, `typecheck`, `setup`, `precommit-install` |
| `.pre-commit-config.yaml` | хуки перед коммитом (ruff, golangci-lint, eslint, prettier, mypy) |
| `agent-hook.sh` | общий хаб агентных хуков (см. ниже) |
| `opencode.jsonc`, `.claude/settings.json`, `.codex/hooks.json`, `.qwen/settings.json` | тонкие адаптеры хуков под каждый инструмент |

## Установка инструментов

```sh
make setup                 # всё сразу (Go/Python/Node должны быть установлены)
```

Или по отдельности:

- **Go**: `go install github.com/golangci/golangci-lint/v2/cmd/golangci-lint@latest`
- **Python**: `pip install ruff mypy pre-commit`
- **TypeScript**: `npm install --save-dev eslint @eslint/js typescript-eslint prettier "typescript@~5.9.0"`
  (typescript-eslint 8.x пока поддерживает TypeScript до 6.1, поэтому версию фиксируем)

Pre-commit: `make precommit-install` (затем хуки запускаются при каждом коммите).

## Повседневные команды

```sh
make lint        # golangci-lint + ruff + eslint
make fmt         # gofmt + ruff format/fix + prettier
make typecheck   # mypy + tsc --noEmit
make precommit   # прогон pre-commit по всем файлам
```

## Хуки агентов: одна логика, четыре адаптера

Вся логика «что делать с файлом после правки агентом» живёт в одном месте —
`agent-hook.sh` (хаб). Конфиги инструментов содержат только вызов хаба, без
дублирования правил:

```
agent-hook.sh  ← единственная реализация (формат + фикс-линт по расширению)
   ├─ .claude/settings.json    → PostToolUse (Edit|Write), JSON на stdin
   ├─ .codex/hooks.json        → PostToolUse, JSON на stdin
   ├─ .qwen/settings.json      → PostToolUse (write_file|replace|edit), JSON на stdin
   └─ opencode.jsonc           → formatter-хук: agent-hook.sh format $FILE
```

Хаб по расширению файла запускает: `.go` → `gofmt -w`; `.py` → `ruff format`
+ `ruff check --fix`; `.ts/.tsx/.js` → `prettier --write`. Отсутствующий
инструмент пропускается с предупреждением; хук никогда не блокирует правку.

Требование хаба: `jq` (только для режима с JSON на stdin).

### Замечания по инструментам

- **Claude Code**: при первом запуске подтвердите доверие к `.claude/settings.json`.
- **Codex**: проектные хуки требуют подтверждения доверия при первом запуске;
  matcher — надмножество имён инструментов правки (`edit|write|patch|...`),
  сработает только по расширению файла в JSON события.
- **Qwen Code**: проектные хуки читаются из `.qwen/settings.json`; при первом
  запуске подтвердите конфигурацию хуков.
- **OpenCode**: хуки другого типа (formatter после write/edit + permissions);
  логика всё равно идёт через `agent-hook.sh format $FILE`. Также включены
  permission-правила (запрос подтверждения на `git push*`, запрет правок
  `.env*`, `vendor/`, `node_modules/`).
- **Freebuff**: полноценной hook-системы нет (проверено по исходникам SDK —
  `AgentDefinition` не содержит хук-колбэков). Вариант: добавить в роль
  разработчика (`agents/roles/developer.md`) указание запускать после правок
  `./agent-hook.sh format <файл>` или `make fmt` через терминальный инструмент.

## Копирование в новый проект

Скопируйте все файлы из таблицы «Состав» в корень проекта. Затем:

1. при необходимости впишите имя вашего Python-пакета в
   `pyproject.toml` → `[tool.ruff.lint.isort]` → `known-first-party`;
2. добавьте свои зависимости в `package.json` / `go.mod` (хаб находит
   prettier через `node_modules/.bin/`);
3. выполните `make setup && make precommit-install`.
