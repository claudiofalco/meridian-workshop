<template>
  <div class="restocking">
    <div class="page-header">
      <h2>{{ t('restocking.title') }}</h2>
      <p>{{ t('restocking.description') }}</p>
    </div>

    <div class="budget-bar">
      <label class="budget-label">{{ t('restocking.budgetLabel') }}</label>
      <input
        v-model.number="budgetInput"
        type="number"
        min="0"
        step="1000"
        :placeholder="t('restocking.budgetPlaceholder')"
        class="budget-input"
      />
    </div>

    <div v-if="loading" class="loading">{{ t('common.loading') }}</div>
    <div v-else-if="error" class="error">{{ error }}</div>
    <div v-else>
      <div class="stats-grid">
        <div class="stat-card danger">
          <div class="stat-label">{{ t('restocking.itemsNeedingRestock') }}</div>
          <div class="stat-value">{{ recommendations.length }}</div>
        </div>
        <div class="stat-card success">
          <div class="stat-label">{{ t('restocking.withinBudget') }}</div>
          <div class="stat-value">{{ withinBudgetCount }}</div>
        </div>
        <div class="stat-card">
          <div class="stat-label">{{ t('restocking.totalCost') }}</div>
          <div class="stat-value">{{ formatCurrency(withinBudgetCost) }}</div>
        </div>
        <div class="stat-card" :class="budgetInput ? (budgetRemaining >= 0 ? 'success' : 'danger') : ''">
          <div class="stat-label">{{ t('restocking.budgetRemaining') }}</div>
          <div class="stat-value">{{ budgetInput ? formatCurrency(budgetRemaining) : '—' }}</div>
        </div>
      </div>

      <div class="card">
        <div class="card-header">
          <h3 class="card-title">{{ t('restocking.title') }} ({{ recommendations.length }})</h3>
        </div>

        <div v-if="recommendations.length === 0" class="empty-state">
          {{ t('restocking.noItems') }}
        </div>

        <div v-else class="table-container">
          <table class="restocking-table">
            <thead>
              <tr>
                <th>{{ t('restocking.table.sku') }}</th>
                <th>{{ t('restocking.table.product') }}</th>
                <th>{{ t('restocking.table.warehouse') }}</th>
                <th>{{ t('restocking.table.currentStock') }}</th>
                <th>{{ t('restocking.table.reorderPoint') }}</th>
                <th>{{ t('restocking.table.recommendedQty') }}</th>
                <th>{{ t('restocking.table.unitCost') }}</th>
                <th>{{ t('restocking.table.estimatedCost') }}</th>
                <th>{{ t('restocking.table.trend') }}</th>
                <th>{{ t('restocking.table.status') }}</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="rec in recommendations" :key="rec.sku + rec.warehouse" :class="{ 'row-urgent': rec.urgent }">
                <td><strong>{{ rec.sku }}</strong></td>
                <td>{{ translateProductName(rec.name) }}</td>
                <td>{{ rec.warehouse }}</td>
                <td>
                  <span :class="rec.quantity_on_hand === 0 ? 'badge danger' : 'badge warning'">
                    {{ rec.quantity_on_hand }}
                  </span>
                </td>
                <td>{{ rec.reorder_point }}</td>
                <td><strong>{{ rec.recommended_qty }}</strong></td>
                <td>{{ formatCurrency(rec.unit_cost) }}</td>
                <td><strong>{{ formatCurrency(rec.estimated_cost) }}</strong></td>
                <td>
                  <span :class="trendClass(rec.trend)">{{ t('trends.' + rec.trend) || rec.trend }}</span>
                </td>
                <td>
                  <span v-if="rec.urgent" class="badge danger">{{ t('restocking.urgent') }}</span>
                  <span v-else-if="rec.within_budget" class="badge success">{{ t('restocking.withinBudgetBadge') }}</span>
                  <span v-else class="badge warning">{{ t('restocking.overBudget') }}</span>
                </td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, computed, watch, onMounted } from 'vue'
import { api } from '../api'
import { useFilters } from '../composables/useFilters'
import { useI18n } from '../composables/useI18n'

export default {
  name: 'Restocking',
  setup() {
    const { t, currentCurrency, translateProductName } = useI18n()
    const { selectedLocation, selectedCategory, getCurrentFilters } = useFilters()

    const loading = ref(true)
    const error = ref(null)
    const recommendations = ref([])
    const budgetInput = ref(null)

    let debounceTimer = null

    const withinBudgetCount = computed(() =>
      recommendations.value.filter(r => r.within_budget).length
    )

    const withinBudgetCost = computed(() =>
      recommendations.value.filter(r => r.within_budget).reduce((sum, r) => sum + r.estimated_cost, 0)
    )

    const budgetRemaining = computed(() =>
      budgetInput.value !== null && budgetInput.value !== ''
        ? budgetInput.value - withinBudgetCost.value
        : null
    )

    const loadData = async () => {
      try {
        loading.value = true
        error.value = null
        const filters = getCurrentFilters()
        const budget = budgetInput.value !== null && budgetInput.value !== '' ? budgetInput.value : null
        recommendations.value = await api.getRestockingRecommendations(filters, budget)
      } catch (err) {
        error.value = 'Failed to load recommendations: ' + err.message
      } finally {
        loading.value = false
      }
    }

    const debouncedLoad = () => {
      clearTimeout(debounceTimer)
      debounceTimer = setTimeout(loadData, 500)
    }

    const formatCurrency = (num) =>
      Number(num).toLocaleString(currentCurrency.value === 'JPY' ? 'ja-JP' : 'en-US', {
        style: 'currency',
        currency: currentCurrency.value === 'JPY' ? 'JPY' : 'USD'
      })

    const trendClass = (trend) => {
      if (trend === 'increasing') return 'trend-up'
      if (trend === 'decreasing') return 'trend-down'
      return 'trend-stable'
    }

    watch([selectedLocation, selectedCategory], loadData)
    watch(budgetInput, debouncedLoad)
    onMounted(loadData)

    return {
      t, translateProductName,
      loading, error, recommendations, budgetInput,
      withinBudgetCount, withinBudgetCost, budgetRemaining,
      formatCurrency, trendClass
    }
  }
}
</script>

<style scoped>
.restocking {
  padding: 0;
}

.budget-bar {
  display: flex;
  align-items: center;
  gap: 1rem;
  background: white;
  border-radius: 12px;
  padding: 1rem 1.5rem;
  margin-bottom: 1.5rem;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
}

.budget-label {
  font-size: 0.875rem;
  font-weight: 600;
  color: #64748b;
  white-space: nowrap;
}

.budget-input {
  width: 200px;
  padding: 0.5rem 0.75rem;
  border: 1px solid #e2e8f0;
  border-radius: 8px;
  font-size: 0.875rem;
  color: #0f172a;
  outline: none;
  transition: border-color 0.2s;
}

.budget-input:focus {
  border-color: #3b82f6;
}

.stats-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 1rem;
  margin-bottom: 1.5rem;
}

.stat-card {
  background: white;
  border-radius: 12px;
  padding: 1.25rem 1.5rem;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
  border-left: 4px solid #e2e8f0;
}

.stat-card.danger { border-left-color: #ef4444; }
.stat-card.success { border-left-color: #22c55e; }
.stat-card.warning { border-left-color: #f59e0b; }

.stat-label {
  font-size: 0.8rem;
  color: #64748b;
  margin-bottom: 0.4rem;
  font-weight: 500;
}

.stat-value {
  font-size: 1.75rem;
  font-weight: 700;
  color: #0f172a;
}

.card {
  background: white;
  border-radius: 12px;
  padding: 1.5rem;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
}

.card-header {
  margin-bottom: 1.25rem;
}

.card-title {
  font-size: 1.125rem;
  font-weight: 600;
  color: #0f172a;
  margin: 0;
}

.table-container {
  overflow-x: auto;
}

.restocking-table {
  width: 100%;
  border-collapse: collapse;
  font-size: 0.875rem;
}

.restocking-table th {
  background: #f8fafc;
  padding: 0.65rem 0.75rem;
  text-align: left;
  font-weight: 600;
  color: #64748b;
  border-bottom: 2px solid #e2e8f0;
  white-space: nowrap;
}

.restocking-table td {
  padding: 0.65rem 0.75rem;
  border-bottom: 1px solid #f1f5f9;
  vertical-align: middle;
}

.restocking-table tr:hover td {
  background: #f8fafc;
}

.row-urgent td {
  background: #fff7ed;
}

.row-urgent:hover td {
  background: #ffedd5;
}

.badge {
  display: inline-block;
  padding: 0.2rem 0.6rem;
  border-radius: 9999px;
  font-size: 0.75rem;
  font-weight: 600;
}

.badge.success { background: #dcfce7; color: #166534; }
.badge.warning { background: #fef3c7; color: #92400e; }
.badge.danger  { background: #fee2e2; color: #991b1b; }

.trend-up     { color: #16a34a; font-weight: 600; }
.trend-down   { color: #dc2626; font-weight: 600; }
.trend-stable { color: #64748b; }

.empty-state {
  text-align: center;
  padding: 3rem;
  color: #64748b;
  font-size: 0.95rem;
}

.loading {
  text-align: center;
  padding: 3rem;
  color: #64748b;
}

.error {
  background: #fee2e2;
  color: #991b1b;
  padding: 1rem;
  border-radius: 8px;
}
</style>
