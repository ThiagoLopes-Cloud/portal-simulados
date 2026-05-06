/** @type {import('tailwindcss').Config} */
export default {
  content: [
    './index.html',
    './src/**/*.{vue,js,ts,jsx,tsx}',
  ],
  theme: {
    extend: {
      colors: {
        'simus-bg':      '#F8FAFC',
        'simus-surface': '#FFFFFF',
        'simus-primary': '#4F46E5',
        'simus-text':    '#0F172A',
        'simus-muted':   '#64748B',
      },
      fontFamily: {
        display: ['Space Grotesk', 'sans-serif'],
        body:    ['Inter', 'sans-serif'],
      },
      borderRadius: {
        simus:    '16px',
        'simus-sm': '12px',
      },
      boxShadow: {
        'simus-soft': '0 8px 30px rgba(0, 0, 0, 0.04)',
      },
    },
  },
  plugins: [],
}
