/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        finora: {
          50: '#f5f7ff',
          100: '#ebf0fe',
          200: '#dce4fe',
          300: '#c3d1fc',
          400: '#a3b6fa',
          500: '#8396f6',
          600: '#6772ef',
          700: '#5359e1',
          800: '#4349b6',
          900: '#394091',
          950: '#232655',
        }
      }
    },
  },
  plugins: [],
}
