/** @type {import('tailwindcss').Config} */
export default {
  content: [
    './index.html',
    './src/**/*.{vue,js,ts,jsx,tsx}',
  ],
  theme: {
    extend: {
      colors: {
        // Brand
        'orbit':         'var(--color-orbit)',
        'orbit-bright':  'var(--color-orbit-bright)',
        'orbit-dim':     'var(--color-orbit-dim)',
        'orbit-glow':    'var(--color-orbit-glow)',
        'pulsar':        'var(--color-pulsar)',
        'pulsar-bright': 'var(--color-pulsar-bright)',
        // Backgrounds
        'cosmos':  'var(--color-cosmos)',
        'nebula':  'var(--color-nebula)',
        'void':    'var(--color-void)',
        'horizon': 'var(--color-horizon)',
        'eclipse': 'var(--color-eclipse)',
        // Text
        'star':  'var(--color-star)',
        'comet': 'var(--color-comet)',
        'dust':  'var(--color-dust)',
        // Semantic
        'stellar': 'var(--color-stellar)',
        'stellar-dim': 'var(--color-stellar-dim)',
        'nova':    'var(--color-nova)',
        'nova-dim': 'var(--color-nova-dim)',
        'flare':   'var(--color-flare)',
        'flare-dim': 'var(--color-flare-dim)',
        'info':    'var(--color-info)',
        // Borders
        'border-default': 'var(--color-border)',
        'border-hover':   'var(--color-border-hover)',
      },
      fontFamily: {
        display: ['Syne', 'sans-serif'],
        body:    ['DM Sans', 'sans-serif'],
        mono:    ['JetBrains Mono', 'monospace'],
      },
      fontSize: {
        '2xs':  'var(--text-2xs)',
        'xs':   'var(--text-xs)',
        'sm':   'var(--text-sm)',
        'base': 'var(--text-base)',
        'lg':   'var(--text-lg)',
        'xl':   'var(--text-xl)',
        '2xl':  'var(--text-2xl)',
        '3xl':  'var(--text-3xl)',
        '4xl':  'var(--text-4xl)',
        '5xl':  'var(--text-5xl)',
      },
      borderRadius: {
        'xs':   'var(--radius-xs)',
        'sm':   'var(--radius-sm)',
        'md':   'var(--radius-md)',
        'lg':   'var(--radius-lg)',
        'xl':   'var(--radius-xl)',
        '2xl':  'var(--radius-2xl)',
        'full': 'var(--radius-full)',
      },
      boxShadow: {
        'xs':      'var(--shadow-xs)',
        'sm':      'var(--shadow-sm)',
        'md':      'var(--shadow-md)',
        'lg':      'var(--shadow-lg)',
        'xl':      'var(--shadow-xl)',
        'card':    'var(--shadow-card)',
        'orbit':   'var(--shadow-orbit)',
        'pulsar':  'var(--shadow-pulsar)',
        'stellar': 'var(--shadow-stellar)',
        'nova':    'var(--shadow-nova)',
        'focus':   'var(--shadow-focus)',
      },
      spacing: {
        '0-5': 'var(--space-0-5)',
        '1-5': 'var(--space-1-5)',
        '2-5': 'var(--space-2-5)',
        '3-5': 'var(--space-3-5)',
      },
    },
  },
  plugins: [],
}
