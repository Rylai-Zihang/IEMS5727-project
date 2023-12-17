/** @type {import('tailwindcss').Config} */
export default {
  content: ["./index.html", "./src/**/*.{vue,js,ts,jsx,tsx}"],
  theme: {
    extend: {
      fontSize: {
        custom: "36px",
      },
      height: {
        custom: "calc(100vh - 120px)",
      },
    },
  },
  plugins: [],
};
