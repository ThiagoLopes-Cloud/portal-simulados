/** @type {import('tailwindcss').Config} */
export default {
  content: [
    './index.html',
    './src/**/*.{vue,js,ts,jsx,tsx}',
  ],
  theme: {
    extend: {
      colors: {
        // ── New unified tokens (sl-*)
        'sl-bg':       '#F8FAFC',
        'sl-surface':  '#FFFFFF',
        'sl-elevated': '#F1F5F9',
        'sl-primary':  '#2563EB',
        'sl-primary-hover': '#1D4ED8',
        'sl-purple':   '#7C3AED',
        'sl-green':    '#059669',
        'sl-red':      '#DC2626',
        'sl-amber':    '#D97706',
        'sl-text':     '#0F172A',
        'sl-text-2':   '#334155',
        'sl-muted':    '#64748B',
        'sl-subtle':   '#94A3B8',
        'sl-border':   '#E2E8F0',
        'sl-border-2': '#CBD5E1',
        'sl-dark':     '#0F172A',

        // ── Legacy compatibility (simus-*) — keep until pages are migrated
        'simus-bg':      '#08091A',
        'simus-surface': '#FFFFFF',
        'simus-primary': '#4F46E5',
        'simus-text':    '#0F172A',
        'simus-muted':   '#64748B',
        'simus-cyan':    '#00E5FF',
      },
      fontFamily: {
        display: ['Syne', 'sans-serif'],
        body:    ['DM Sans', 'sans-serif'],
        mono:    ['JetBrains Mono', 'monospace'],
      },
      borderRadius: {
        'sl':        '12px',
        'sl-lg':     '16px',
        'sl-xl':     '20px',
        'simus':     '16px',
        'simus-sm':  '12px',
      },
      boxShadow: {
        'sl-card':     '0 1px 3px rgba(0,0,0,0.06), 0 4px 16px rgba(0,0,0,0.04)',
        'sl-elevated': '0 4px 24px rgba(0,0,0,0.08)',
        'sl-primary':  '0 4px 14px rgba(37,99,235,0.35)',
        'simus-soft':  '0 8px 30px rgba(0,0,0,0.04)',
      },
    },
  },
  plugins: [],
}
