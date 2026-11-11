// Сгенерировано scripts/generate-agents.py — не редактировать вручную.
// Полное ТЗ роли: agents/roles/developer.md (агент читает его при старте).
// Для типизации можно добавить: import type { AgentDefinition } from './types/agent-definition'

const developer = {
  id: 'developer',
  displayName: 'Программист',
  model: 'anthropic/claude-sonnet-4.6',  // при необходимости замените на другую модель OpenRouter/Freebuff
  toolNames: ['read_files', 'glob', 'code_search', 'web_search', 'read_url', 'write_file', 'str_replace', 'apply_patch', 'run_terminal_command'],
  inputSchema: {
    prompt: {
      type: 'string',
      description: `Подробное ТЗ для агента: контекст, что сделать, где искать вводные, ожидаемый артефакт и критерии готовности.`,
    },
  },
  includeMessageHistory: false,
  spawnerPrompt: `Реализация задач по коду по архитектуре и conventions проекта.`,
  instructionsPrompt: `Ты — Программист проекта. Твоё полное ТЗ — файл agents/roles/developer.md в корне репозитория: прочитай его целиком первым же действием и действуй строго по нему. Контекст проекта — в AGENTS.md, тоже прочитай. Если какой-то из файлов недоступен — сообщи об этом и остановись.`,
}

export default developer
