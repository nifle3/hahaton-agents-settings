// ESLint 9 (flat config) + typescript-eslint — линтер для TypeScript/JavaScript.
// Расширение .mjs выбрано, чтобы конфиг работал независимо от "type" в package.json.
// @ts-check
import eslint from "@eslint/js";
import tseslint from "typescript-eslint";

export default tseslint.config(
  {
    ignores: [
      "dist/**",
      "build/**",
      "coverage/**",
      "node_modules/**",
      "vendor/**",
      "**/*.gen.ts",
    ],
  },

  // Базовые правила для JS и TS
  eslint.configs.recommended,
  // Правила с учётом типов (type-aware linting — часть тайпчека)
  tseslint.configs.recommended,

  {
    languageOptions: {
      parserOptions: {
        projectService: true,
        tsconfigRootDir: import.meta.dirname,
      },
    },
    rules: {
      // Не ругаться на неиспользуемые аргументы, начинающиеся с "_"
      "@typescript-eslint/no-unused-vars": [
        "error",
        { argsIgnorePattern: "^_", varsIgnorePattern: "^_" },
      ],
      // Явные type-only импорты — помогает бандлерам
      "@typescript-eslint/consistent-type-imports": ["warn", { fixStyle: "inline-type-imports" }],
      // Нет/no-floating-promises требуют type-aware режима; включается по желанию:
      // "@typescript-eslint/no-floating-promises": "error",
    },
  },
);
