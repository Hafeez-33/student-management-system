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
    Status
    <select
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
  align-items: center;
  gap: 0.5rem;
  font-size: 0.95rem;
}

select {
  padding: 0.35rem 0.5rem;
}
</style>
