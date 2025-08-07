/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    './templates/**/*.html',
    './*/templates/**/*.html',
    './static/js/**/*.js',
  ],
  theme: {
    extend: {
      colors: {
        'primary-blue': '#1e40af',
        'light-blue': '#3b82f6',
        'dark-blue': '#1e3a8a',
      },
      animation: {
        'marquee': 'marquee 20s linear infinite',
      },
      keyframes: {
        marquee: {
          '0%': { transform: 'translateX(0%)' },
          '100%': { transform: 'translateX(-50%)' },
        }
      },
      fontFamily: {
        'poppins': ['Poppins', 'sans-serif'],
      }
    }
  },
  plugins: [],
}