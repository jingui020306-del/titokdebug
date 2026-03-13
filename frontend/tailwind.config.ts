import type { Config } from "tailwindcss";

const config: Config = {
  content: ["./app/**/*.{js,ts,jsx,tsx}", "./components/**/*.{js,ts,jsx,tsx}"],
  theme: {
    extend: {
      colors: {
        base: "#090B12",
        panel: "#101524",
        line: "#252C3F",
        ink: "#E5E9F0",
        subInk: "#8B95A8",
        accent: "#6E7DFF"
      },
      boxShadow: {
        soft: "0 0 0 1px rgba(110,125,255,0.15), 0 16px 40px rgba(0,0,0,0.45)"
      }
    }
  },
  plugins: []
};

export default config;
