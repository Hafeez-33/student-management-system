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
    <button
      type="button"
      :disabled="page <= 1"
      @click="$emit('change', page - 1)"
    >
      Previous
    </button>
    <span>Page {{ page }} of {{ pages }}</span>
    <button
      type="button"
      :disabled="page >= pages"
      @click="$emit('change', page + 1)"
    >
      Next
    </button>
  </nav>
</template>

<style scoped>
.pagination {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  margin-top: 1rem;
}

button:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}
</style>
