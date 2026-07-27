// vite.config.js
import { defineConfig } from "file:///D:/du%20an/educore/frontend/node_modules/vite/dist/node/index.js";
import vue from "file:///D:/du%20an/educore/frontend/node_modules/@vitejs/plugin-vue/dist/index.mjs";
import path from "path";
import { VitePWA } from "file:///D:/du%20an/educore/frontend/node_modules/vite-plugin-pwa/dist/index.js";
var __vite_injected_original_dirname = "D:\\du an\\educore\\frontend";
var vite_config_default = defineConfig(async ({ mode }) => {
  const isDev = mode === "development";
  const frappeui = await importFrappeUIPlugin(isDev);
  const config = {
    define: {
      __VUE_PROD_HYDRATION_MISMATCH_DETAILS__: "false"
    },
    plugins: [
      frappeui({
        frappeProxy: true,
        lucideIcons: true,
        jinjaBootData: true,
        buildConfig: {
          outDir: path.resolve(__vite_injected_original_dirname, "../lms/public/frontend"),
          indexHtmlPath: "../lms/www/_lms.html"
        }
      }),
      vue(),
      VitePWA({
        disable: process.env.DISABLE_PWA === "true",
        registerType: "autoUpdate",
        devOptions: {
          enabled: false
        },
        workbox: {
          cleanupOutdatedCaches: true,
          maximumFileSizeToCacheInBytes: 5 * 1024 * 1024,
          globPatterns: ["**/*.{js,ts,css,html,svg}"],
          runtimeCaching: [
            {
              urlPattern: ({ request }) => request.destination === "document",
              handler: "NetworkFirst",
              options: {
                cacheName: "html-cache"
              }
            }
          ]
        },
        manifest: false
      })
    ],
    server: {
      host: "0.0.0.0",
      // Accept connections from any network interface
      allowedHosts: true,
      // SCORM packages are served by Frappe's SCORMRenderer at /scorm/... .
      // frappeProxy only forwards ^/(desk|app|login|api|assets|files|private),
      // so without this the iframe's /scorm URL hits the SPA fallback and renders
      // blank. The `router` mirrors frappeProxy: Frappe resolves the site from the
      // Host header, so we must forward to http://<site>:8000 — a bare 127.0.0.1
      // target makes Frappe 404 with "127.0.0.1 does not exist". (Backend :8000.)
      proxy: {
        "/scorm": {
          target: "http://127.0.0.1:8000",
          router: (req) => `http://${req.headers.host.split(":")[0]}:8000`
        }
      }
    },
    resolve: {
      alias: {
        "@": path.resolve(__vite_injected_original_dirname, "src"),
        "../../../../sites/common_site_config.json": path.resolve(__vite_injected_original_dirname, "src/common_site_config_fallback.json")
      },
      // Force one copy of prosemirror; duplicate copies break tiptap's
      // instanceof checks and crash the list buttons.
      dedupe: [
        "prosemirror-model",
        "prosemirror-state",
        "prosemirror-view",
        "prosemirror-transform",
        "vue",
        "frappe-ui"
      ]
    },
    optimizeDeps: {
      include: [
        "feather-icons",
        "tailwind.config.js",
        "highlight.js",
        "plyr"
      ],
      exclude: mode === "production" ? [] : ["frappe-ui"]
    }
  };
  return config;
});
async function importFrappeUIPlugin(isDev) {
  if (isDev) {
    try {
      const module2 = await import("../frappe-ui/vite");
      return module2.default;
    } catch (error) {
      console.warn(
        "Local frappe-ui not found, falling back to npm package:",
        error.message
      );
    }
  }
  const module = await import("file:///D:/du%20an/educore/frontend/node_modules/frappe-ui/vite/index.js");
  return module.default;
}
export {
  vite_config_default as default
};
//# sourceMappingURL=data:application/json;base64,ewogICJ2ZXJzaW9uIjogMywKICAic291cmNlcyI6IFsidml0ZS5jb25maWcuanMiXSwKICAic291cmNlc0NvbnRlbnQiOiBbImNvbnN0IF9fdml0ZV9pbmplY3RlZF9vcmlnaW5hbF9kaXJuYW1lID0gXCJEOlxcXFxkdSBhblxcXFxlZHVjb3JlXFxcXGZyb250ZW5kXCI7Y29uc3QgX192aXRlX2luamVjdGVkX29yaWdpbmFsX2ZpbGVuYW1lID0gXCJEOlxcXFxkdSBhblxcXFxlZHVjb3JlXFxcXGZyb250ZW5kXFxcXHZpdGUuY29uZmlnLmpzXCI7Y29uc3QgX192aXRlX2luamVjdGVkX29yaWdpbmFsX2ltcG9ydF9tZXRhX3VybCA9IFwiZmlsZTovLy9EOi9kdSUyMGFuL2VkdWNvcmUvZnJvbnRlbmQvdml0ZS5jb25maWcuanNcIjtpbXBvcnQgeyBkZWZpbmVDb25maWcgfSBmcm9tICd2aXRlJ1xyXG5pbXBvcnQgdnVlIGZyb20gJ0B2aXRlanMvcGx1Z2luLXZ1ZSdcclxuaW1wb3J0IHBhdGggZnJvbSAncGF0aCdcclxuaW1wb3J0IHsgVml0ZVBXQSB9IGZyb20gJ3ZpdGUtcGx1Z2luLXB3YSdcclxuXHJcbmV4cG9ydCBkZWZhdWx0IGRlZmluZUNvbmZpZyhhc3luYyAoeyBtb2RlIH0pID0+IHtcclxuXHRjb25zdCBpc0RldiA9IG1vZGUgPT09ICdkZXZlbG9wbWVudCdcclxuXHRjb25zdCBmcmFwcGV1aSA9IGF3YWl0IGltcG9ydEZyYXBwZVVJUGx1Z2luKGlzRGV2KVxyXG5cclxuXHRjb25zdCBjb25maWcgPSB7XHJcblx0XHRkZWZpbmU6IHtcclxuXHRcdFx0X19WVUVfUFJPRF9IWURSQVRJT05fTUlTTUFUQ0hfREVUQUlMU19fOiAnZmFsc2UnLFxyXG5cdFx0fSxcclxuXHRcdHBsdWdpbnM6IFtcclxuXHRcdFx0ZnJhcHBldWkoe1xyXG5cdFx0XHRcdGZyYXBwZVByb3h5OiB0cnVlLFxyXG5cdFx0XHRcdGx1Y2lkZUljb25zOiB0cnVlLFxyXG5cdFx0XHRcdGppbmphQm9vdERhdGE6IHRydWUsXHJcblx0XHRcdFx0YnVpbGRDb25maWc6IHtcclxuXHRcdFx0XHRcdG91dERpcjogcGF0aC5yZXNvbHZlKF9fZGlybmFtZSwgJy4uL2xtcy9wdWJsaWMvZnJvbnRlbmQnKSxcclxuXHRcdFx0XHRcdGluZGV4SHRtbFBhdGg6ICcuLi9sbXMvd3d3L19sbXMuaHRtbCcsXHJcblx0XHRcdFx0fSxcclxuXHRcdFx0fSksXHJcblx0XHRcdHZ1ZSgpLFxyXG5cdFx0XHRWaXRlUFdBKHtcclxuXHRcdFx0XHRkaXNhYmxlOiBwcm9jZXNzLmVudi5ESVNBQkxFX1BXQSA9PT0gJ3RydWUnLFxyXG5cdFx0XHRcdHJlZ2lzdGVyVHlwZTogJ2F1dG9VcGRhdGUnLFxyXG5cdFx0XHRcdGRldk9wdGlvbnM6IHtcclxuXHRcdFx0XHRcdGVuYWJsZWQ6IGZhbHNlLFxyXG5cdFx0XHRcdH0sXHJcblx0XHRcdFx0d29ya2JveDoge1xyXG5cdFx0XHRcdFx0Y2xlYW51cE91dGRhdGVkQ2FjaGVzOiB0cnVlLFxyXG5cdFx0XHRcdFx0bWF4aW11bUZpbGVTaXplVG9DYWNoZUluQnl0ZXM6IDUgKiAxMDI0ICogMTAyNCxcclxuXHRcdFx0XHRcdGdsb2JQYXR0ZXJuczogWycqKi8qLntqcyx0cyxjc3MsaHRtbCxzdmd9J10sXHJcblx0XHRcdFx0XHRydW50aW1lQ2FjaGluZzogW1xyXG5cdFx0XHRcdFx0XHR7XHJcblx0XHRcdFx0XHRcdFx0dXJsUGF0dGVybjogKHsgcmVxdWVzdCB9KSA9PlxyXG5cdFx0XHRcdFx0XHRcdFx0cmVxdWVzdC5kZXN0aW5hdGlvbiA9PT0gJ2RvY3VtZW50JyxcclxuXHRcdFx0XHRcdFx0XHRoYW5kbGVyOiAnTmV0d29ya0ZpcnN0JyxcclxuXHRcdFx0XHRcdFx0XHRvcHRpb25zOiB7XHJcblx0XHRcdFx0XHRcdFx0XHRjYWNoZU5hbWU6ICdodG1sLWNhY2hlJyxcclxuXHRcdFx0XHRcdFx0XHR9LFxyXG5cdFx0XHRcdFx0XHR9LFxyXG5cdFx0XHRcdFx0XSxcclxuXHRcdFx0XHR9LFxyXG5cdFx0XHRcdG1hbmlmZXN0OiBmYWxzZSxcclxuXHRcdFx0fSksXHJcblx0XHRdLFxyXG5cdFx0c2VydmVyOiB7XHJcblx0XHRcdGhvc3Q6ICcwLjAuMC4wJywgLy8gQWNjZXB0IGNvbm5lY3Rpb25zIGZyb20gYW55IG5ldHdvcmsgaW50ZXJmYWNlXHJcblx0XHRcdGFsbG93ZWRIb3N0czogdHJ1ZSxcclxuXHRcdFx0Ly8gU0NPUk0gcGFja2FnZXMgYXJlIHNlcnZlZCBieSBGcmFwcGUncyBTQ09STVJlbmRlcmVyIGF0IC9zY29ybS8uLi4gLlxyXG5cdFx0XHQvLyBmcmFwcGVQcm94eSBvbmx5IGZvcndhcmRzIF4vKGRlc2t8YXBwfGxvZ2lufGFwaXxhc3NldHN8ZmlsZXN8cHJpdmF0ZSksXHJcblx0XHRcdC8vIHNvIHdpdGhvdXQgdGhpcyB0aGUgaWZyYW1lJ3MgL3Njb3JtIFVSTCBoaXRzIHRoZSBTUEEgZmFsbGJhY2sgYW5kIHJlbmRlcnNcclxuXHRcdFx0Ly8gYmxhbmsuIFRoZSBgcm91dGVyYCBtaXJyb3JzIGZyYXBwZVByb3h5OiBGcmFwcGUgcmVzb2x2ZXMgdGhlIHNpdGUgZnJvbSB0aGVcclxuXHRcdFx0Ly8gSG9zdCBoZWFkZXIsIHNvIHdlIG11c3QgZm9yd2FyZCB0byBodHRwOi8vPHNpdGU+OjgwMDAgXHUyMDE0IGEgYmFyZSAxMjcuMC4wLjFcclxuXHRcdFx0Ly8gdGFyZ2V0IG1ha2VzIEZyYXBwZSA0MDQgd2l0aCBcIjEyNy4wLjAuMSBkb2VzIG5vdCBleGlzdFwiLiAoQmFja2VuZCA6ODAwMC4pXHJcblx0XHRcdHByb3h5OiB7XHJcblx0XHRcdFx0Jy9zY29ybSc6IHtcclxuXHRcdFx0XHRcdHRhcmdldDogJ2h0dHA6Ly8xMjcuMC4wLjE6ODAwMCcsXHJcblx0XHRcdFx0XHRyb3V0ZXI6IChyZXEpID0+XHJcblx0XHRcdFx0XHRcdGBodHRwOi8vJHtyZXEuaGVhZGVycy5ob3N0LnNwbGl0KCc6JylbMF19OjgwMDBgLFxyXG5cdFx0XHRcdH0sXHJcblx0XHRcdH0sXHJcblx0XHR9LFxyXG5cdFx0cmVzb2x2ZToge1xyXG5cdFx0XHRhbGlhczoge1xyXG5cdFx0XHRcdCdAJzogcGF0aC5yZXNvbHZlKF9fZGlybmFtZSwgJ3NyYycpLFxyXG5cdFx0XHRcdCcuLi8uLi8uLi8uLi9zaXRlcy9jb21tb25fc2l0ZV9jb25maWcuanNvbic6IHBhdGgucmVzb2x2ZShfX2Rpcm5hbWUsICdzcmMvY29tbW9uX3NpdGVfY29uZmlnX2ZhbGxiYWNrLmpzb24nKSxcclxuXHRcdFx0fSxcclxuXHRcdFx0Ly8gRm9yY2Ugb25lIGNvcHkgb2YgcHJvc2VtaXJyb3I7IGR1cGxpY2F0ZSBjb3BpZXMgYnJlYWsgdGlwdGFwJ3NcclxuXHRcdFx0Ly8gaW5zdGFuY2VvZiBjaGVja3MgYW5kIGNyYXNoIHRoZSBsaXN0IGJ1dHRvbnMuXHJcblx0XHRcdGRlZHVwZTogW1xyXG5cdFx0XHRcdCdwcm9zZW1pcnJvci1tb2RlbCcsXHJcblx0XHRcdFx0J3Byb3NlbWlycm9yLXN0YXRlJyxcclxuXHRcdFx0XHQncHJvc2VtaXJyb3ItdmlldycsXHJcblx0XHRcdFx0J3Byb3NlbWlycm9yLXRyYW5zZm9ybScsXHJcblx0XHRcdFx0J3Z1ZScsXHJcblx0XHRcdFx0J2ZyYXBwZS11aScsXHJcblx0XHRcdF0sXHJcblx0XHR9LFxyXG5cdFx0b3B0aW1pemVEZXBzOiB7XHJcblx0XHRcdGluY2x1ZGU6IFtcclxuXHRcdFx0XHQnZmVhdGhlci1pY29ucycsXHJcblx0XHRcdFx0J3RhaWx3aW5kLmNvbmZpZy5qcycsXHJcblx0XHRcdFx0J2hpZ2hsaWdodC5qcycsXHJcblx0XHRcdFx0J3BseXInLFxyXG5cdFx0XHRdLFxyXG5cdFx0XHRleGNsdWRlOiBtb2RlID09PSAncHJvZHVjdGlvbicgPyBbXSA6IFsnZnJhcHBlLXVpJ10sXHJcblx0XHR9LFxyXG5cdH1cclxuXHRyZXR1cm4gY29uZmlnXHJcbn0pXHJcblxyXG5hc3luYyBmdW5jdGlvbiBpbXBvcnRGcmFwcGVVSVBsdWdpbihpc0Rldikge1xyXG5cdGlmIChpc0Rldikge1xyXG5cdFx0dHJ5IHtcclxuXHRcdFx0Y29uc3QgbW9kdWxlID0gYXdhaXQgaW1wb3J0KCcuLi9mcmFwcGUtdWkvdml0ZScpXHJcblx0XHRcdHJldHVybiBtb2R1bGUuZGVmYXVsdFxyXG5cdFx0fSBjYXRjaCAoZXJyb3IpIHtcclxuXHRcdFx0Y29uc29sZS53YXJuKFxyXG5cdFx0XHRcdCdMb2NhbCBmcmFwcGUtdWkgbm90IGZvdW5kLCBmYWxsaW5nIGJhY2sgdG8gbnBtIHBhY2thZ2U6JyxcclxuXHRcdFx0XHRlcnJvci5tZXNzYWdlXHJcblx0XHRcdClcclxuXHRcdH1cclxuXHR9XHJcblx0Ly8gRmFsbCBiYWNrIHRvIG5wbSBwYWNrYWdlIGlmIGxvY2FsIGltcG9ydCBmYWlsc1xyXG5cdGNvbnN0IG1vZHVsZSA9IGF3YWl0IGltcG9ydCgnZnJhcHBlLXVpL3ZpdGUnKVxyXG5cdHJldHVybiBtb2R1bGUuZGVmYXVsdFxyXG59XHJcbiJdLAogICJtYXBwaW5ncyI6ICI7QUFBdVEsU0FBUyxvQkFBb0I7QUFDcFMsT0FBTyxTQUFTO0FBQ2hCLE9BQU8sVUFBVTtBQUNqQixTQUFTLGVBQWU7QUFIeEIsSUFBTSxtQ0FBbUM7QUFLekMsSUFBTyxzQkFBUSxhQUFhLE9BQU8sRUFBRSxLQUFLLE1BQU07QUFDL0MsUUFBTSxRQUFRLFNBQVM7QUFDdkIsUUFBTSxXQUFXLE1BQU0scUJBQXFCLEtBQUs7QUFFakQsUUFBTSxTQUFTO0FBQUEsSUFDZCxRQUFRO0FBQUEsTUFDUCx5Q0FBeUM7QUFBQSxJQUMxQztBQUFBLElBQ0EsU0FBUztBQUFBLE1BQ1IsU0FBUztBQUFBLFFBQ1IsYUFBYTtBQUFBLFFBQ2IsYUFBYTtBQUFBLFFBQ2IsZUFBZTtBQUFBLFFBQ2YsYUFBYTtBQUFBLFVBQ1osUUFBUSxLQUFLLFFBQVEsa0NBQVcsd0JBQXdCO0FBQUEsVUFDeEQsZUFBZTtBQUFBLFFBQ2hCO0FBQUEsTUFDRCxDQUFDO0FBQUEsTUFDRCxJQUFJO0FBQUEsTUFDSixRQUFRO0FBQUEsUUFDUCxTQUFTLFFBQVEsSUFBSSxnQkFBZ0I7QUFBQSxRQUNyQyxjQUFjO0FBQUEsUUFDZCxZQUFZO0FBQUEsVUFDWCxTQUFTO0FBQUEsUUFDVjtBQUFBLFFBQ0EsU0FBUztBQUFBLFVBQ1IsdUJBQXVCO0FBQUEsVUFDdkIsK0JBQStCLElBQUksT0FBTztBQUFBLFVBQzFDLGNBQWMsQ0FBQywyQkFBMkI7QUFBQSxVQUMxQyxnQkFBZ0I7QUFBQSxZQUNmO0FBQUEsY0FDQyxZQUFZLENBQUMsRUFBRSxRQUFRLE1BQ3RCLFFBQVEsZ0JBQWdCO0FBQUEsY0FDekIsU0FBUztBQUFBLGNBQ1QsU0FBUztBQUFBLGdCQUNSLFdBQVc7QUFBQSxjQUNaO0FBQUEsWUFDRDtBQUFBLFVBQ0Q7QUFBQSxRQUNEO0FBQUEsUUFDQSxVQUFVO0FBQUEsTUFDWCxDQUFDO0FBQUEsSUFDRjtBQUFBLElBQ0EsUUFBUTtBQUFBLE1BQ1AsTUFBTTtBQUFBO0FBQUEsTUFDTixjQUFjO0FBQUE7QUFBQTtBQUFBO0FBQUE7QUFBQTtBQUFBO0FBQUEsTUFPZCxPQUFPO0FBQUEsUUFDTixVQUFVO0FBQUEsVUFDVCxRQUFRO0FBQUEsVUFDUixRQUFRLENBQUMsUUFDUixVQUFVLElBQUksUUFBUSxLQUFLLE1BQU0sR0FBRyxFQUFFLENBQUMsQ0FBQztBQUFBLFFBQzFDO0FBQUEsTUFDRDtBQUFBLElBQ0Q7QUFBQSxJQUNBLFNBQVM7QUFBQSxNQUNSLE9BQU87QUFBQSxRQUNOLEtBQUssS0FBSyxRQUFRLGtDQUFXLEtBQUs7QUFBQSxRQUNsQyw2Q0FBNkMsS0FBSyxRQUFRLGtDQUFXLHNDQUFzQztBQUFBLE1BQzVHO0FBQUE7QUFBQTtBQUFBLE1BR0EsUUFBUTtBQUFBLFFBQ1A7QUFBQSxRQUNBO0FBQUEsUUFDQTtBQUFBLFFBQ0E7QUFBQSxRQUNBO0FBQUEsUUFDQTtBQUFBLE1BQ0Q7QUFBQSxJQUNEO0FBQUEsSUFDQSxjQUFjO0FBQUEsTUFDYixTQUFTO0FBQUEsUUFDUjtBQUFBLFFBQ0E7QUFBQSxRQUNBO0FBQUEsUUFDQTtBQUFBLE1BQ0Q7QUFBQSxNQUNBLFNBQVMsU0FBUyxlQUFlLENBQUMsSUFBSSxDQUFDLFdBQVc7QUFBQSxJQUNuRDtBQUFBLEVBQ0Q7QUFDQSxTQUFPO0FBQ1IsQ0FBQztBQUVELGVBQWUscUJBQXFCLE9BQU87QUFDMUMsTUFBSSxPQUFPO0FBQ1YsUUFBSTtBQUNILFlBQU1BLFVBQVMsTUFBTSxPQUFPLG1CQUFtQjtBQUMvQyxhQUFPQSxRQUFPO0FBQUEsSUFDZixTQUFTLE9BQU87QUFDZixjQUFRO0FBQUEsUUFDUDtBQUFBLFFBQ0EsTUFBTTtBQUFBLE1BQ1A7QUFBQSxJQUNEO0FBQUEsRUFDRDtBQUVBLFFBQU0sU0FBUyxNQUFNLE9BQU8sMEVBQWdCO0FBQzVDLFNBQU8sT0FBTztBQUNmOyIsCiAgIm5hbWVzIjogWyJtb2R1bGUiXQp9Cg==
