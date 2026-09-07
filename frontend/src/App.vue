<script setup>
import StudentList from './components/StudentList.vue'
</script>

<template>
  <div class="shell">
    <div class="shell-bg" aria-hidden="true" />
    <main class="app">
      <StudentList />
    </main>
  </div>
</template>

<style>
:root {
  --primary: #4f46e5;
  --primary-dark: #3730a3;
  --primary-soft: #eef2ff;
  --accent: #06b6d4;
  --accent-soft: #ecfeff;
  --violet: #7c3aed;
  --success: #059669;
  --success-soft: #ecfdf5;
  --warning: #d97706;
  --warning-soft: #fffbeb;
  --danger: #dc2626;
  --danger-soft: #fef2f2;
  --surface: #ffffff;
  --surface-muted: #f8fafc;
  --border: #e2e8f0;
  --border-strong: #cbd5e1;
  --text-primary: #0f172a;
  --text-secondary: #64748b;
  --text-muted: #94a3b8;
  --shadow-sm: 0 1px 2px rgba(15, 23, 42, 0.05);
  --shadow-md: 0 8px 24px rgba(15, 23, 42, 0.08);
  --radius: 14px;
  --radius-sm: 10px;
  --focus: 0 0 0 3px rgba(79, 70, 229, 0.25);
  --font: 'Segoe UI', system-ui, -apple-system, BlinkMacSystemFont, sans-serif;
  --transition: 160ms ease;
}

*,
*::before,
*::after {
  box-sizing: border-box;
}

html,
body {
  margin: 0;
  min-height: 100%;
}

body {
  font-family: var(--font);
  color: var(--text-primary);
  background: var(--surface-muted);
  -webkit-font-smoothing: antialiased;
}

button,
input,
select {
  font: inherit;
}

button:focus-visible,
input:focus-visible,
select:focus-visible {
  outline: none;
  box-shadow: var(--focus);
}

.shell {
  position: relative;
  min-height: 100vh;
}

.shell-bg {
  position: absolute;
  inset: 0 0 auto 0;
  height: 220px;
  background:
    radial-gradient(ellipse 80% 120% at 10% -20%, rgba(6, 182, 212, 0.18), transparent 55%),
    radial-gradient(ellipse 70% 100% at 90% -10%, rgba(124, 58, 237, 0.16), transparent 50%),
    linear-gradient(135deg, #312e81 0%, #4338ca 45%, #4f46e5 100%);
  z-index: 0;
}

.app {
  position: relative;
  z-index: 1;
  max-width: 68rem;
  margin: 0 auto;
  padding: 2rem 1.25rem 3rem;
}

@media (max-width: 640px) {
  .app {
    padding: 1.25rem 1rem 2.5rem;
  }

  .shell-bg {
    height: 180px;
  }
}
</style>
