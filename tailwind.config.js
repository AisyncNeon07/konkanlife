/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    "./templates/**/*.html",
    "./*/templates/**/*.html",
    "./**/templates/**/*.html",
    "./static/js/**/*.js",
  ],
  corePlugins: {
    preflight: false,
  },
  theme: {
    extend: {
      colors: {
        ocean: {
          deep: "#0a3d62",
          navy: "#0f172a",
          card: "#ffffff",
          cardHover: "#f8fafc",
          mid: "#0284c7",
          light: "#0ea5e9",
          sky: "#38bdf8",
          mist: "#f0f9ff",
          surface: "#f8fafc",
        },
        sand: {
          warm: "#fef3c7",
          gold: "#d97706",
          coral: "#ea580c",
          subtle: "#fffbeb",
        },
        coastal: {
          emerald: "#059669",
          mint: "#10b981",
          subtle: "#ecfdf5",
        },
        surface: {
          light: "#ffffff",
          lightAlt: "#f8fafc",
          lightMuted: "#f1f5f9",
          border: "#e2e8f0",
        },
      },
      fontFamily: {
        sans: ["'Plus Jakarta Sans'", "system-ui", "-apple-system", "sans-serif"],
        display: ["'Plus Jakarta Sans'", "sans-serif"],
        editorial: ["'Playfair Display'", "Georgia", "serif"],
      },
      boxShadow: {
        editorial: "0 20px 40px -15px rgba(15, 23, 42, 0.08)",
        tactile: "0 10px 25px -5px rgba(2, 132, 199, 0.25)",
        card: "0 4px 20px -2px rgba(15, 23, 42, 0.05), 0 2px 6px -1px rgba(15, 23, 42, 0.02)",
        "card-hover": "0 20px 35px -10px rgba(15, 23, 42, 0.1), 0 4px 10px -2px rgba(15, 23, 42, 0.04)",
      },
      borderRadius: {
        "2xl": "1rem",
        "3xl": "1.5rem",
        "4xl": "2rem",
      },
    },
  },
  plugins: [],
};
