/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
    'node_modules/flowbite-react/**/*.{js,jsx,ts,tsx}'
  ],
  theme: {
    extend: {
      colors: {
        white: '#ffffff',
      }
    },
  },
  plugins: [
    require('flowbite/plugin')
  ],
  darkMode: 'light',
}
