<template>
  <div class="app">
    <header class="top-nav">
      <div class="nav-container">
        <div class="logo">
          <h1>{{ t('nav.companyName') }}</h1>
          <span class="subtitle">{{ t('nav.subtitle') }}</span>
        </div>
        <nav class="nav-tabs">
          <router-link to="/" :class="{ active: $route.path === '/' }">
            {{ t('nav.overview') }}
          </router-link>
          <router-link to="/inventory" :class="{ active: $route.path === '/inventory' }">
            {{ t('nav.inventory') }}
          </router-link>
          <router-link to="/orders" :class="{ active: $route.path === '/orders' }">
            {{ t('nav.orders') }}
          </router-link>
          <router-link to="/spending" :class="{ active: $route.path === '/spending' }">
            {{ t('nav.finance') }}
          </router-link>
          <router-link to="/demand" :class="{ active: $route.path === '/demand' }">
            {{ t('nav.demandForecast') }}
          </router-link>
          <router-link to="/reports" :class="{ active: $route.path === '/reports' }">
            {{ t('nav.reports') }}
          </router-link>
          <router-link to="/restocking" :class="{ active: $route.path === '/restocking' }">
            {{ t('nav.restocking') }}
          </router-link>
        </nav>
        <button class="theme-toggle" @click="toggleTheme" :title="theme === 'dark' ? 'Switch to light mode' : 'Switch to dark mode'">
          <svg v-if="theme === 'dark'" xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="5"/><line x1="12" y1="1" x2="12" y2="3"/><line x1="12" y1="21" x2="12" y2="23"/><line x1="4.22" y1="4.22" x2="5.64" y2="5.64"/><line x1="18.36" y1="18.36" x2="19.78" y2="19.78"/><line x1="1" y1="12" x2="3" y2="12"/><line x1="21" y1="12" x2="23" y2="12"/><line x1="4.22" y1="19.78" x2="5.64" y2="18.36"/><line x1="18.36" y1="5.64" x2="19.78" y2="4.22"/></svg>
          <svg v-else xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M21 12.79A9 9 0 1 1 11.21 3 7 7 0 0 0 21 12.79z"/></svg>
        </button>
        <LanguageSwitcher />
        <ProfileMenu
          @show-profile-details="showProfileDetails = true"
          @show-tasks="showTasks = true"
        />
      </div>
    </header>
    <FilterBar />
    <main class="main-content">
      <router-view />
    </main>

    <ProfileDetailsModal
      :is-open="showProfileDetails"
      @close="showProfileDetails = false"
    />

    <TasksModal
      :is-open="showTasks"
      :tasks="tasks"
      @close="showTasks = false"
      @add-task="addTask"
      @delete-task="deleteTask"
      @toggle-task="toggleTask"
    />
  </div>
</template>

<script>
import { ref, onMounted, computed } from 'vue'
import { api } from './api'
import { useAuth } from './composables/useAuth'
import { useI18n } from './composables/useI18n'
import { useTheme } from './composables/useTheme'
import FilterBar from './components/FilterBar.vue'
import ProfileMenu from './components/ProfileMenu.vue'
import ProfileDetailsModal from './components/ProfileDetailsModal.vue'
import TasksModal from './components/TasksModal.vue'
import LanguageSwitcher from './components/LanguageSwitcher.vue'

export default {
  name: 'App',
  components: {
    FilterBar,
    ProfileMenu,
    ProfileDetailsModal,
    TasksModal,
    LanguageSwitcher
  },
  setup() {
    const { currentUser } = useAuth()
    const { t } = useI18n()
    const { theme, toggleTheme } = useTheme()
    const showProfileDetails = ref(false)
    const showTasks = ref(false)
    const apiTasks = ref([])

    // Merge mock tasks from currentUser with API tasks
    const tasks = computed(() => {
      return [...currentUser.value.tasks, ...apiTasks.value]
    })

    const loadTasks = async () => {
      try {
        apiTasks.value = await api.getTasks()
      } catch (err) {
        console.error('Failed to load tasks:', err)
      }
    }

    const addTask = async (taskData) => {
      try {
        const newTask = await api.createTask(taskData)
        // Add new task to the beginning of the array
        apiTasks.value.unshift(newTask)
      } catch (err) {
        console.error('Failed to add task:', err)
      }
    }

    const deleteTask = async (taskId) => {
      try {
        // Check if it's a mock task (from currentUser)
        const isMockTask = currentUser.value.tasks.some(t => t.id === taskId)

        if (isMockTask) {
          // Remove from mock tasks
          const index = currentUser.value.tasks.findIndex(t => t.id === taskId)
          if (index !== -1) {
            currentUser.value.tasks.splice(index, 1)
          }
        } else {
          // Remove from API tasks
          await api.deleteTask(taskId)
          apiTasks.value = apiTasks.value.filter(t => t.id !== taskId)
        }
      } catch (err) {
        console.error('Failed to delete task:', err)
      }
    }

    const toggleTask = async (taskId) => {
      try {
        // Check if it's a mock task (from currentUser)
        const mockTask = currentUser.value.tasks.find(t => t.id === taskId)

        if (mockTask) {
          // Toggle mock task status
          mockTask.status = mockTask.status === 'pending' ? 'completed' : 'pending'
        } else {
          // Toggle API task
          const updatedTask = await api.toggleTask(taskId)
          const index = apiTasks.value.findIndex(t => t.id === taskId)
          if (index !== -1) {
            apiTasks.value[index] = updatedTask
          }
        }
      } catch (err) {
        console.error('Failed to toggle task:', err)
      }
    }

    onMounted(loadTasks)

    return {
      t,
      theme,
      toggleTheme,
      showProfileDetails,
      showTasks,
      tasks,
      addTask,
      deleteTask,
      toggleTask
    }
  }
}
</script>

<style>
/* ── Design tokens ─────────────────────────────────────────── */
:root {
  --bg:              #f1f5f9;
  --surface:         #ffffff;
  --surface-hover:   #f8fafc;
  --border:          #e2e8f0;
  --border-light:    #f1f5f9;
  --text-primary:    #0f172a;
  --text-secondary:  #64748b;
  --text-tertiary:   #94a3b8;
  --accent:          #2563eb;
  --accent-light:    #60a5fa;
  --accent-hover:    #1d4ed8;
  --accent-bg:       #eff6ff;
  --accent-text:     #1e40af;
  --nav-bg:          #ffffff;
  --nav-border:      #e2e8f0;
  --success-bg:      #d1fae5;
  --success-text:    #065f46;
  --warning-bg:      #fef3c7;
  --warning-text:    #92400e;
  --warning-value:   #ea580c;
  --danger-bg:       #fef2f2;
  --danger-border:   #fecaca;
  --danger-text:     #991b1b;
  --danger-value:    #dc2626;
  --info-bg:         #dbeafe;
  --info-text:       #1e40af;
  --stable-bg:       #e0e7ff;
  --stable-text:     #3730a3;
  --shadow-sm:       0 1px 3px 0 rgba(0,0,0,0.05), 0 1px 2px -1px rgba(0,0,0,0.05);
  --shadow-md:       0 4px 12px rgba(0,0,0,0.07);
  --radius:          10px;
  --radius-sm:       6px;
}

[data-theme="dark"] {
  --bg:              #0f172a;
  --surface:         #1e293b;
  --surface-hover:   #273449;
  --border:          #334155;
  --border-light:    #2a3a4d;
  --text-primary:    #f1f5f9;
  --text-secondary:  #94a3b8;
  --text-tertiary:   #64748b;
  --accent:          #60a5fa;
  --accent-light:    #93c5fd;
  --accent-hover:    #93c5fd;
  --accent-bg:       #1e3a5f;
  --accent-text:     #93c5fd;
  --nav-bg:          #1e293b;
  --nav-border:      #334155;
  --success-bg:      #14412e;
  --success-text:    #4ade80;
  --warning-bg:      #3b2a0e;
  --warning-text:    #fbbf24;
  --warning-value:   #fb923c;
  --danger-bg:       #3b1515;
  --danger-border:   #7f1d1d;
  --danger-text:     #f87171;
  --danger-value:    #f87171;
  --info-bg:         #1e3a5f;
  --info-text:       #60a5fa;
  --stable-bg:       #1e1b4b;
  --stable-text:     #a5b4fc;
  --shadow-sm:       0 1px 3px 0 rgba(0,0,0,0.3);
  --shadow-md:       0 4px 12px rgba(0,0,0,0.4);
}

/* ── Reset ──────────────────────────────────────────────────── */
* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

body {
  font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
  background: var(--bg);
  color: var(--text-primary);
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  transition: background 0.2s ease, color 0.2s ease;
}

/* ── App shell ───────────────────────────────────────────────── */
.app {
  display: flex;
  flex-direction: column;
  min-height: 100vh;
}

/* ── Top nav ─────────────────────────────────────────────────── */
.top-nav {
  background: var(--nav-bg);
  border-bottom: 1px solid var(--nav-border);
  box-shadow: var(--shadow-sm);
  position: sticky;
  top: 0;
  z-index: 100;
  transition: background 0.2s ease, border-color 0.2s ease;
}

.nav-container {
  max-width: 1600px;
  margin: 0 auto;
  display: flex;
  align-items: center;
  padding: 0 2rem;
  height: 68px;
  gap: 0.5rem;
}

.nav-container > .nav-tabs {
  margin-left: auto;
  margin-right: 0.5rem;
}

.logo {
  display: flex;
  align-items: baseline;
  gap: 0.75rem;
  flex-shrink: 0;
}

.logo h1 {
  font-size: 1.25rem;
  font-weight: 700;
  color: var(--text-primary);
  letter-spacing: -0.025em;
}

.subtitle {
  font-size: 0.8125rem;
  color: var(--text-secondary);
  font-weight: 400;
  padding-left: 0.75rem;
  border-left: 1px solid var(--border);
}

/* ── Nav tabs ────────────────────────────────────────────────── */
.nav-tabs {
  display: flex;
  gap: 0.125rem;
}

.nav-tabs a {
  padding: 0.5rem 1rem;
  color: var(--text-secondary);
  text-decoration: none;
  font-weight: 500;
  font-size: 0.9rem;
  border-radius: var(--radius-sm);
  transition: color 0.15s ease, background 0.15s ease;
  position: relative;
  white-space: nowrap;
}

.nav-tabs a:hover {
  color: var(--text-primary);
  background: var(--surface-hover);
}

.nav-tabs a.active {
  color: var(--accent);
  background: var(--accent-bg);
  font-weight: 600;
}

.nav-tabs a.active::after {
  content: '';
  position: absolute;
  bottom: -1px;
  left: 8px;
  right: 8px;
  height: 2px;
  background: var(--accent);
  border-radius: 2px 2px 0 0;
}

/* ── Theme toggle ────────────────────────────────────────────── */
.theme-toggle {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 36px;
  height: 36px;
  border: 1px solid var(--border);
  border-radius: var(--radius-sm);
  background: var(--surface);
  color: var(--text-secondary);
  cursor: pointer;
  flex-shrink: 0;
  transition: color 0.15s ease, background 0.15s ease, border-color 0.15s ease;
}

.theme-toggle:hover {
  color: var(--text-primary);
  background: var(--surface-hover);
  border-color: var(--text-tertiary);
}

/* ── Main content ────────────────────────────────────────────── */
.main-content {
  flex: 1;
  max-width: 1600px;
  width: 100%;
  margin: 0 auto;
  padding: 1.5rem 2rem;
}

/* ── Page header ─────────────────────────────────────────────── */
.page-header {
  margin-bottom: 1.5rem;
}

.page-header h2 {
  font-size: 1.75rem;
  font-weight: 700;
  color: var(--text-primary);
  margin-bottom: 0.3rem;
  letter-spacing: -0.025em;
}

.page-header p {
  color: var(--text-secondary);
  font-size: 0.9375rem;
}

/* ── Stat cards ──────────────────────────────────────────────── */
.stats-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(240px, 1fr));
  gap: 1.25rem;
  margin-bottom: 1.5rem;
}

.stat-card {
  background: var(--surface);
  padding: 1.375rem 1.5rem;
  border-radius: var(--radius);
  border: 1px solid var(--border);
  box-shadow: var(--shadow-sm);
  transition: border-color 0.15s ease, box-shadow 0.15s ease;
}

.stat-card:hover {
  border-color: var(--text-tertiary);
  box-shadow: var(--shadow-md);
}

.stat-label {
  color: var(--text-secondary);
  font-size: 0.8125rem;
  font-weight: 600;
  text-transform: uppercase;
  letter-spacing: 0.6px;
  margin-bottom: 0.625rem;
}

.stat-value {
  font-size: 2rem;
  font-weight: 700;
  color: var(--text-primary);
  letter-spacing: -0.03em;
  line-height: 1.1;
}

.stat-card.warning .stat-value { color: var(--warning-value); }
.stat-card.success .stat-value { color: var(--success-text); }
.stat-card.danger  .stat-value { color: var(--danger-value); }
.stat-card.info    .stat-value { color: var(--accent); }

/* ── Cards ───────────────────────────────────────────────────── */
.card {
  background: var(--surface);
  border-radius: var(--radius);
  padding: 1.375rem 1.5rem;
  border: 1px solid var(--border);
  margin-bottom: 1.25rem;
  box-shadow: var(--shadow-sm);
  transition: background 0.2s ease, border-color 0.2s ease;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1.125rem;
  padding-bottom: 0.875rem;
  border-bottom: 1px solid var(--border);
}

.card-title {
  font-size: 1.0625rem;
  font-weight: 700;
  color: var(--text-primary);
  letter-spacing: -0.015em;
}

/* ── Tables ──────────────────────────────────────────────────── */
.table-container {
  overflow-x: auto;
}

table {
  width: 100%;
  border-collapse: collapse;
}

thead {
  background: var(--surface-hover);
  border-top: 1px solid var(--border);
  border-bottom: 1px solid var(--border);
}

th {
  text-align: left;
  padding: 0.625rem 0.875rem;
  font-weight: 600;
  color: var(--text-secondary);
  font-size: 0.75rem;
  text-transform: uppercase;
  letter-spacing: 0.06em;
}

td {
  padding: 0.625rem 0.875rem;
  border-top: 1px solid var(--border-light);
  color: var(--text-primary);
  font-size: 0.875rem;
}

tbody tr {
  transition: background-color 0.1s ease;
}

tbody tr:hover {
  background: var(--surface-hover);
}

/* ── Badges ──────────────────────────────────────────────────── */
.badge {
  display: inline-block;
  padding: 0.25rem 0.625rem;
  border-radius: var(--radius-sm);
  font-size: 0.7rem;
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: 0.05em;
}

.badge.success,
.badge.increasing { background: var(--success-bg); color: var(--success-text); }

.badge.warning    { background: var(--warning-bg); color: var(--warning-text); }

.badge.danger,
.badge.decreasing,
.badge.high       { background: var(--danger-bg);  color: var(--danger-text); }

.badge.info,
.badge.low        { background: var(--info-bg);    color: var(--info-text); }

.badge.stable     { background: var(--stable-bg);  color: var(--stable-text); }

.badge.medium     { background: var(--warning-bg); color: var(--warning-text); }

/* ── Utility ─────────────────────────────────────────────────── */
.loading {
  text-align: center;
  padding: 3rem;
  color: var(--text-secondary);
  font-size: 0.9375rem;
}

.error {
  background: var(--danger-bg);
  border: 1px solid var(--danger-border);
  color: var(--danger-text);
  padding: 1rem 1.25rem;
  border-radius: 8px;
  margin: 1rem 0;
  font-size: 0.9375rem;
}

/* ── Dark mode overrides for scoped component styles ─────────── */
/* html[data-theme="dark"] has specificity (0,2,1), beating Vue's
   scoped attribute selectors at (0,2,0), so no !important needed */
html[data-theme="dark"] .card,
html[data-theme="dark"] .stat-card,
html[data-theme="dark"] .kpi-card,
html[data-theme="dark"] .kpi-card-grid,
html[data-theme="dark"] .metric-card,
html[data-theme="dark"] .modal-content,
html[data-theme="dark"] .filter-bar,
html[data-theme="dark"] .filter-group select,
html[data-theme="dark"] .filter-group input,
html[data-theme="dark"] .budget-input,
html[data-theme="dark"] .tasks-modal,
html[data-theme="dark"] .profile-modal {
  background: var(--surface);
  border-color: var(--border);
  color: var(--text-primary);
}

html[data-theme="dark"] .filter-bar {
  background: var(--surface);
  border-bottom-color: var(--border);
}

html[data-theme="dark"] select,
html[data-theme="dark"] input[type="text"],
html[data-theme="dark"] input[type="number"],
html[data-theme="dark"] input[type="search"] {
  background: var(--surface-hover);
  color: var(--text-primary);
  border-color: var(--border);
}

html[data-theme="dark"] th,
html[data-theme="dark"] thead {
  background: var(--surface-hover);
  color: var(--text-secondary);
  border-color: var(--border);
}

html[data-theme="dark"] td {
  color: var(--text-primary);
  border-color: var(--border-light);
}

html[data-theme="dark"] tbody tr:hover,
html[data-theme="dark"] tr:hover {
  background: var(--surface-hover);
}

html[data-theme="dark"] .card-header,
html[data-theme="dark"] .card-title,
html[data-theme="dark"] h2,
html[data-theme="dark"] h3 {
  color: var(--text-primary);
  border-color: var(--border);
}

html[data-theme="dark"] .stat-label,
html[data-theme="dark"] .stat-subtitle,
html[data-theme="dark"] .label,
html[data-theme="dark"] label {
  color: var(--text-secondary);
}

html[data-theme="dark"] .stat-value {
  color: var(--text-primary);
}

html[data-theme="dark"] p,
html[data-theme="dark"] .description,
html[data-theme="dark"] .subtitle-text {
  color: var(--text-secondary);
}

html[data-theme="dark"] .modal-overlay {
  background: rgba(0, 0, 0, 0.7);
}

html[data-theme="dark"] .chart-bg,
html[data-theme="dark"] .chart-area {
  background: var(--surface);
}

html[data-theme="dark"] .legend-item,
html[data-theme="dark"] .chart-label {
  color: var(--text-secondary);
}

html[data-theme="dark"] .search-input,
html[data-theme="dark"] .task-input {
  background: var(--surface-hover);
  border-color: var(--border);
  color: var(--text-primary);
}

html[data-theme="dark"] .profile-menu-dropdown {
  background: var(--surface);
  border-color: var(--border);
  box-shadow: var(--shadow-md);
}

html[data-theme="dark"] .menu-item:hover {
  background: var(--surface-hover);
}

html[data-theme="dark"] .empty-state {
  color: var(--text-secondary);
}
</style>
