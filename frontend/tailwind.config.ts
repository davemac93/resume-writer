import type { Config } from "tailwindcss";

const config: Config = {
  content: [
    "./src/pages/**/*.{js,ts,jsx,tsx,mdx}",
    "./src/components/**/*.{js,ts,jsx,tsx,mdx}",
    "./src/app/**/*.{js,ts,jsx,tsx,mdx}",
  ],
  theme: {
    extend: {
      colors: {
        background: "var(--background-start)",
        foreground: "var(--foreground)",
        card: {
          DEFAULT: "var(--card-bg)",
          foreground: "var(--foreground)",
        },
        primary: {
          DEFAULT: "var(--primary-blue)",
          foreground: "var(--foreground)",
        },
        secondary: {
          DEFAULT: "var(--text-muted)",
          foreground: "var(--foreground)",
        },
        destructive: {
          DEFAULT: "#ef4444",
          foreground: "var(--foreground)",
        },
        muted: {
          DEFAULT: "var(--text-muted)",
          foreground: "var(--foreground)",
        },
        accent: {
          DEFAULT: "var(--card-bg)",
          foreground: "var(--foreground)",
        },
        popover: {
          DEFAULT: "var(--card-bg)",
          foreground: "var(--foreground)",
        },
        border: "var(--border)",
        input: "var(--border)",
        ring: "var(--primary-blue)",
      },
      borderRadius: {
        lg: "var(--radius)",
        md: "calc(var(--radius) - 2px)",
        sm: "calc(var(--radius) - 4px)",
      },
      backdropBlur: {
        xs: '2px',
      },
      boxShadow: {
        xs: '0 1px 2px 0 rgb(0 0 0 / 0.05)',
      },
      ringWidth: {
        '3': '3px',
      },
    },
  },
  plugins: [],
};

export default config;
