<script setup>
defineProps({
  modelValue: {
    type: String,
    default: '',
  },
})

defineEmits(['update:modelValue'])
</script>

<template>
  <label class="filter">
    <span class="filter-label">Status</span>
    <select
      class="filter-select"
      :value="modelValue"
      @change="$emit('update:modelValue', $event.target.value)"
    >
      <option value="">All statuses</option>
      <option value="active">Active</option>
      <option value="graduated">Graduated</option>
      <option value="dropped">Dropped</option>
    </select>
  </label>
</template>

<style scoped>
.filter {
  display: inline-flex;
  flex-direction: column;
  gap: 0.35rem;
  min-width: 12rem;
}

.filter-label {
  font-size: 0.8rem;
  font-weight: 600;
  color: var(--text-secondary);
  letter-spacing: 0.02em;
  text-transform: uppercase;
}

.filter-select {
  appearance: none;
  width: 100%;
  padding: 0.65rem 2.25rem 0.65rem 0.85rem;
  border: 1px solid var(--border);
  border-radius: var(--radius-sm);
  background-color: var(--surface);
  background-image:
    linear-gradient(45deg, transparent 50%, var(--text-secondary) 50%),
    linear-gradient(135deg, var(--text-secondary) 50%, transparent 50%);
  background-position:
    calc(100% - 16px) calc(50% - 2px),
    calc(100% - 11px) calc(50% - 2px);
  background-size: 5px 5px, 5px 5px;
  background-repeat: no-repeat;
  color: var(--text-primary);
  cursor: pointer;
  transition: border-color var(--transition), box-shadow var(--transition);
}

.filter-select:hover {
  border-color: var(--border-strong);
}

.filter-select:focus {
  border-color: var(--primary);
}
</style>
