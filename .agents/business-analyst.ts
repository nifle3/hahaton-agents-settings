// Сгенерировано scripts/generate-agents.py — не редактировать вручную.
// Полное ТЗ роли: agents/roles/business-analyst.md (агент читает его при старте).
// Для типизации можно добавить: import type { AgentDefinition } from './types/agent-definition'

const business_analyst = {
  id: 'business-analyst',
  displayName: 'Бизнес-аналитик',
  model: 'google/gemini-3-flash-preview',  // при необходимости замените на другую модель OpenRouter/Freebuff
  toolNames: ['read_files', 'glob', 'code_search', 'web_search', 'read_url', 'write_file', 'str_replace'],
  inputSchema: {
    prompt: {
      type: 'string',
      description: `Подробное ТЗ для агента: контекст, что сделать, где искать вводные, ожидаемый артефакт и критерии готовности.`,
    },
  },
  includeMessageHistory: false,
  spawnerPrompt: `Формулирование требований, user stories, глоссария и процессов домена. Вызывать перед реализацией новой фичи.`,
  instructionsPrompt: `Ты — Бизнес-аналитик проекта. Твоё полное ТЗ — файл agents/roles/business-analyst.md в корне репозитория: прочитай его целиком первым же действием и действуй строго по нему. Контекст проекта — в AGENTS.md, тоже прочитай. Если какой-то из файлов недоступен — сообщи об этом и остановись.`,
}

export default business_analyst
