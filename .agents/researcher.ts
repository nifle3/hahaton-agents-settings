// Сгенерировано scripts/generate-agents.py — не редактировать вручную.
// Полное ТЗ роли: agents/roles/researcher.md (агент читает его при старте).
// Для типизации можно добавить: import type { AgentDefinition } from './types/agent-definition'

const researcher = {
  id: 'researcher',
  displayName: 'Ресерчер темы',
  model: 'google/gemini-3-flash-preview',  // при необходимости замените на другую модель OpenRouter/Freebuff
  toolNames: ['read_files', 'glob', 'code_search', 'web_search', 'read_url'],
  inputSchema: {
    prompt: {
      type: 'string',
      description: `Подробное ТЗ для агента: контекст, что сделать, где искать вводные, ожидаемый артефакт и критерии готовности.`,
    },
  },
  includeMessageHistory: false,
  spawnerPrompt: `Исследование темы в вебе: рынок, аналоги, технологии, регуляторика. Делегировать любые ресерч-вопросы.`,
  instructionsPrompt: `Ты — Ресерчер темы проекта. Твоё полное ТЗ — файл agents/roles/researcher.md в корне репозитория: прочитай его целиком первым же действием и действуй строго по нему. Контекст проекта — в AGENTS.md, тоже прочитай. Если какой-то из файлов недоступен — сообщи об этом и остановись.`,
}

export default researcher
