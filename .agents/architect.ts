// Сгенерировано scripts/generate-agents.py — не редактировать вручную.
// Полное ТЗ роли: agents/roles/architect.md (агент читает его при старте).
// Для типизации можно добавить: import type { AgentDefinition } from './types/agent-definition'

const architect = {
  id: 'architect',
  displayName: 'Архитектор',
  model: 'google/gemini-3.1-pro-preview',  // при необходимости замените на другую модель OpenRouter/Freebuff
  toolNames: ['read_files', 'glob', 'code_search', 'web_search', 'read_url', 'write_file', 'str_replace'],
  inputSchema: {
    prompt: {
      type: 'string',
      description: `Подробное ТЗ для агента: контекст, что сделать, где искать вводные, ожидаемый артефакт и критерии готовности.`,
    },
  },
  includeMessageHistory: false,
  spawnerPrompt: `Проектирование архитектуры, датамодели и API-контрактов, написание ADR. Вызывать до начала реализации значимых фич.`,
  instructionsPrompt: `Ты — Архитектор проекта. Твоё полное ТЗ — файл agents/roles/architect.md в корне репозитория: прочитай его целиком первым же действием и действуй строго по нему. Контекст проекта — в AGENTS.md, тоже прочитай. Если какой-то из файлов недоступен — сообщи об этом и остановись.`,
}

export default architect
