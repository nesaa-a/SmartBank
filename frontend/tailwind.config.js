/** @type {import('tailwindcss').Config} */
export default {
  content: ["./index.html", "./src/**/*.{ts,tsx}"],
  theme: {
    extend: {
      colors: {
        brand: {
          50:  "#eff6ff",
          100: "#dbeafe",
          400: "#60a5fa",
          500: "#3b82f6",
          600: "#2563eb",
          700: "#1d4ed8",
          900: "#1e3a8a",
        },
      },
      backgroundImage: {
        "gradient-brand": "linear-gradient(135deg, #3b82f6 0%, #6366f1 100%)",
        "gradient-card":  "linear-gradient(145deg, rgba(30,41,59,0.8) 0%, rgba(15,23,42,0.9) 100%)",
      },
      boxShadow: {
        "glow-blue":   "0 0 24px rgba(59,130,246,0.25)",
        "glow-indigo": "0 0 24px rgba(99,102,241,0.25)",
        "glow-green":  "0 0 24px rgba(16,185,129,0.25)",
        "glow-red":    "0 0 24px rgba(239,68,68,0.25)",
      },
      keyframes: {
        "fade-in": {
          "0%":   { opacity: "0", transform: "translateY(8px)" },
          "100%": { opacity: "1", transform: "translateY(0)" },
        },
        "slide-up": {
          "0%":   { opacity: "0", transform: "translateY(20px)" },
          "100%": { opacity: "1", transform: "translateY(0)" },
        },
        shimmer: {
          "0%":   { backgroundPosition: "-200% center" },
          "100%": { backgroundPosition: "200% center" },
        },
        "glow-pulse": {
          "0%, 100%": { opacity: "0.4" },
          "50%":      { opacity: "0.8" },
        },
        float: {
          "0%, 100%": { transform: "translateY(0px)" },
          "50%":      { transform: "translateY(-8px)" },
        },
        "scale-in": {
          "0%":   { opacity: "0", transform: "scale(0.95)" },
          "100%": { opacity: "1", transform: "scale(1)" },
        },
      },
      animation: {
        "fade-in":    "fade-in 0.4s ease-out",
        "slide-up":   "slide-up 0.5s ease-out",
        shimmer:      "shimmer 2.5s linear infinite",
        "glow-pulse": "glow-pulse 2s ease-in-out infinite",
        float:        "float 6s ease-in-out infinite",
        "scale-in":   "scale-in 0.3s ease-out",
      },
    },
  },
  plugins: [],
};
