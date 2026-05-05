import js from "@eslint/js";
import globals from "globals";
import pluginVue from "eslint-plugin-vue";
import { defineConfig } from "eslint/config";

export default defineConfig([
  // 🚫 Ignorar arquivos que NÃO devem ser analisados
  {
    ignores: ["node_modules/**", "dist/**", "frontend/dist/**"],
  },

  // ✅ Config principal JS
  {
    files: ["**/*.{js,mjs,cjs,vue}"],
    plugins: { js },
    extends: ["js/recommended"],
    languageOptions: {
      globals: globals.browser,
    },
  },

  // ✅ Config do Vue
  pluginVue.configs["flat/essential"],
]);