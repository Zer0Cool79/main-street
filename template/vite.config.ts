import { defineConfig } from "vite";
import { siteConfig } from "./plugins/site-config";

const root = import.meta.dirname;

export default defineConfig({
  plugins: [siteConfig()],
  build: {
    outDir: "dist",
    rollupOptions: {
      input: {
        main: `${root}/index.html`,
        notFound: `${root}/404.html`,
        privacy: `${root}/privacy-policy/index.html`,
        terms: `${root}/terms-of-service/index.html`,
      },
    },
  },
});
