/** @type {import('tailwindcss').Config} */
// Tailwind CSS v4 — tokens de tema definidos via @theme no CSS (src/assets/main.css)
// Este arquivo é mantido para plugins e configurações futuras.
export default {
  content: [
    './index.html',
    './src/**/*.{vue,js,ts,jsx,tsx}',
  ],
  theme: {
    extend: {
      colors: {
        'simus-bg':      '#0B0D17',
        'simus-surface': '#1A1D27',
        'simus-cyan':    '#00E5FF',
        'simus-purple':  '#8A2BE2',
      },
      fontFamily: {
        display: ['Space Grotesk', 'sans-serif'],
        body:    ['Inter', 'sans-serif'],
      },
      borderRadius: {
        simus: '16px',
      },
    },
  },
  plugins: [],
}
