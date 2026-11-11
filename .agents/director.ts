// Сгенерировано scripts/generate-agents.py — не редактировать вручную.
// Полное ТЗ роли: agents/roles/director.md (агент читает его при старте).
// Для типизации можно добавить: import type { AgentDefinition } from './types/agent-definition'

const director = {
  id: 'director',
  displayName: 'Директор проекта',
  model: 'anthropic/claude-sonnet-4.6',  // при необходимости замените на другую модель OpenRouter/Freebuff
  toolNames: ['read_files', 'glob', 'code_search', 'web_search', 'read_url', 'write_file', 'spawn_agents'],
  spawnableAgents: ['researcher', 'business-analyst', 'architect', 'developer', 'tester'],
  inputSchema: {
    prompt: {
      type: 'string',
      description: `Подробное ТЗ для агента: контекст, что сделать, где искать вводные, ожидаемый артефакт и критерии готовности.`,
    },
  },
  includeMessageHistory: false,
  spawnerPrompt: `Директор проекта: декомпозирует задачу, оркестрирует остальных субагентов и принимает результаты. Использовать как ведущего агента для многоэтапной работы.`,
  instructionsPrompt: `Ты — Директор проекта проекта. Твоё полное ТЗ — файл agents/roles/director.md в корне репозитория: прочитай его целиком первым же действием и действуй строго по нему. Контекст проекта — в AGENTS.md, тоже прочитай. Если какой-то из файлов недоступен — сообщи об этом и остановись.`,
}

export default director
