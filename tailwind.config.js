/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        "background":"#F9FAFB",
        "icon-fill": "#4B5563",
        "border": "#E5E7EB",
        "text-default": "#374151",
        "active-blue": "#1D4ED8",
        "active-tab": "#EFF6FF",
        "output": "#F3F4F6",
        "hint": "#FEFCE8",
        "hint-title": "#854D0E",
      },
      fontFamily: {
        'inter': ["Inter", "sans-serif"],
      },
      lineHeight: {
        "mobile": "22px",
        "desktop": "25px",
      }
    },
  },
  plugins: [],
}

