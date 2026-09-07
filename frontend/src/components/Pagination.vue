<script setup>
defineProps({
  page: {
    type: Number,
    required: true,
  },
  pages: {
    type: Number,
    required: true,
  },
  total: {
    type: Number,
    required: true,
  },
})

defineEmits(['change'])
</script>

<template>
  <nav v-if="total > 0 && pages > 1" class="pagination" aria-label="Pagination">
    <p class="meta">Showing page {{ page }} of {{ pages }} · {{ total }} total</p>
    <div class="controls">
      <button
        type="button"
        class="page-btn"
        :disabled="page <= 1"
        @click="$emit('change', page - 1)"
      >
        Previous
      </button>
      <span class="indicator" aria-current="page">Page {{ page }} of {{ pages }}</span>
      <button
        type="button"
        class="page-btn"
        :disabled="page >= pages"
        @click="$emit('change', page + 1)"
      >
        Next
      </button>
    </div>
  </nav>
</template>

<style scoped>
.pagination {
  display: flex;
  flex-wrap: wrap;
  align-items: center;
  justify-content: space-between;
  gap: 0.75rem 1rem;
  margin-top: 1rem;
  padding: 0.85rem 1rem;
  background: var(--surface-muted);
  border: 1px solid var(--border);
  border-radius: var(--radius-sm);
}

.meta {
  margin: 0;
  font-size: 0.875rem;
  color: var(--text-secondary);
}

.controls {
  display: flex;
  align-items: center;
  gap: 0.65rem;
}

.indicator {
  font-size: 0.875rem;
  font-weight: 600;
  color: var(--text-primary);
  min-width: 7rem;
  text-align: center;
}

.page-btn {
  padding: 0.5rem 0.9rem;
  border: 1px solid var(--border);
  border-radius: 8px;
  background: var(--surface);
  color: var(--text-primary);
  font-weight: 600;
  cursor: pointer;
  transition:
    background var(--transition),
    border-color var(--transition),
    color var(--transition),
    transform var(--transition);
}

.page-btn:hover:not(:disabled) {
  border-color: var(--primary);
  color: var(--primary);
  background: var(--primary-soft);
}

.page-btn:disabled {
  opacity: 0.45;
  cursor: not-allowed;
}

@media (max-width: 560px) {
  .pagination {
    flex-direction: column;
    align-items: stretch;
  }

  .controls {
    justify-content: space-between;
  }
}
</style>
