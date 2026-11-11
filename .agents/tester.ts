// Сгенерировано scripts/generate-agents.py — не редактировать вручную.
// Полное ТЗ роли: agents/roles/tester.md (агент читает его при старте).
// Для типизации можно добавить: import type { AgentDefinition } from './types/agent-definition'

const tester = {
  id: 'tester',
  displayName: 'Тестировщик',
  model: 'google/gemini-3-flash-preview',  // при необходимости замените на другую модель OpenRouter/Freebuff
  toolNames: ['read_files', 'glob', 'code_search', 'read_url', 'write_file', 'str_replace', 'run_terminal_command'],
  inputSchema: {
    prompt: {
      type: 'string',
      description: `Подробное ТЗ для агента: контекст, что сделать, где искать вводные, ожидаемый артефакт и критерии готовности.`,
    },
  },
  includeMessageHistory: false,
  spawnerPrompt: `Тест-планы, тест-кейсы, автотесты, отчёты о дефектах и вердикт о готовности. Вызывать после каждой задачи реализации.`,
  instructionsPrompt: `Ты — Тестировщик проекта. Твоё полное ТЗ — файл agents/roles/tester.md в корне репозитория: прочитай его целиком первым же действием и действуй строго по нему. Контекст проекта — в AGENTS.md, тоже прочитай. Если какой-то из файлов недоступен — сообщи об этом и остановись.`,
}

export default tester
