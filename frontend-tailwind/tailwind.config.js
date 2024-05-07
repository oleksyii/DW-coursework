/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{vue,js,ts,jsx,tsx}",
    "./node_modules/flowbite/**/*.js",
  ],
  theme: {
    extend: {
      colors: {
        "btn-primary": "#f5e79a",
        "my-gray": "#ebebeb",
        "my-green": "hsla(160, 100%, 37%, 1)",
        "my-green-hover": "hsla(160, 100%, 37%, 0.2)",
        "gray-superlight": "#adbcd1",
        "gray-light": "#496183",
        "gray-middle": "#405572",
        "gray-price": "#2e3d52",
        "gray-text": "#A1A5AA",
        "green-price": "#BEEE11",
        "blue-cart": "#67C1F5",
        "blue-tag": "rgba(135, 206, 247, 0.25)",
        "blue-tag-bright": "#6fc4f6",
        "black-review": "#16202D",
        "red-dislike": "#AB4D4D",
      },
    },
  },
  plugins: [require("flowbite/plugin")],
};
