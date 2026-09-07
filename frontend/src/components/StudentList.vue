<script setup>
import { onMounted, ref } from 'vue'
import { getStudents } from '../api/students'
import StatusFilter from './StatusFilter.vue'
import Pagination from './Pagination.vue'

const students = ref([])
const loading = ref(false)
const error = ref('')
const currentPage = ref(1)
const selectedStatus = ref('')
const perPage = ref(10)
const total = ref(0)
const totalPages = ref(0)

async function loadStudents() {
  loading.value = true
  error.value = ''

  try {
    const response = await getStudents({
      page: currentPage.value,
      per_page: perPage.value,
      enrollment_status: selectedStatus.value,
    })
    const data = response.data
    students.value = data.items || []
    currentPage.value = data.page
    perPage.value = data.per_page
    total.value = data.total
    totalPages.value = data.pages
  } catch {
    error.value = 'Unable to load students. Please try again.'
    students.value = []
    total.value = 0
    totalPages.value = 0
  } finally {
    loading.value = false
  }
}

function onStatusChange(status) {
  selectedStatus.value = status
  currentPage.value = 1
  loadStudents()
}

function onPageChange(page) {
  currentPage.value = page
  loadStudents()
}

function fullName(student) {
  return `${student.first_name} ${student.last_name}`
}

onMounted(loadStudents)
</script>

<template>
  <section class="list">
    <div class="toolbar">
      <StatusFilter :model-value="selectedStatus" @update:model-value="onStatusChange" />
    </div>

    <div v-if="loading" class="status">Loading students...</div>

    <div v-else-if="error" class="status status-error" role="alert">
      <p>{{ error }}</p>
      <button type="button" class="retry" @click="loadStudents">Retry</button>
    </div>

    <div v-else-if="students.length === 0" class="status">No students found.</div>

    <template v-else>
      <table class="table">
        <thead>
          <tr>
            <th>Name</th>
            <th>Email</th>
            <th>Date of Birth</th>
            <th>Enrollment Status</th>
            <th>Actions</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="student in students" :key="student.id">
            <td>{{ fullName(student) }}</td>
            <td>{{ student.email }}</td>
            <td>{{ student.date_of_birth }}</td>
            <td class="status-cell">{{ student.enrollment_status }}</td>
            <td class="actions">
              <span class="placeholder">Edit</span>
              <span class="placeholder">Delete</span>
            </td>
          </tr>
        </tbody>
      </table>
    </template>

    <Pagination
      v-if="!loading && !error"
      :page="currentPage"
      :pages="totalPages"
      :total="total"
      @change="onPageChange"
    />
  </section>
</template>

<style scoped>
.list {
  margin-top: 1.5rem;
}

.toolbar {
  margin-bottom: 1rem;
}

.status {
  padding: 1.25rem;
  background: #fff;
  border: 1px solid #e3e3e3;
  border-radius: 8px;
}

.status-error {
  color: #8a1f11;
  border-color: #f0c2bb;
  background: #fff6f5;
}

.retry {
  margin-top: 0.5rem;
  padding: 0.4rem 0.8rem;
  cursor: pointer;
}

.table {
  width: 100%;
  border-collapse: collapse;
  background: #fff;
  border: 1px solid #e3e3e3;
  border-radius: 8px;
  overflow: hidden;
}

th,
td {
  text-align: left;
  padding: 0.75rem 0.9rem;
  border-bottom: 1px solid #eee;
  font-size: 0.95rem;
}

th {
  background: #f0f2f5;
  font-weight: 600;
}

.status-cell {
  text-transform: capitalize;
}

.actions {
  display: flex;
  gap: 0.75rem;
  color: #888;
}

.placeholder {
  font-size: 0.85rem;
}
</style>
