<script setup>
import { onMounted, ref } from 'vue'
import { deleteStudent, getStudents } from '../api/students'
import StatusFilter from './StatusFilter.vue'
import Pagination from './Pagination.vue'
import StudentForm from './StudentForm.vue'

const students = ref([])
const loading = ref(false)
const error = ref('')
const currentPage = ref(1)
const selectedStatus = ref('')
const perPage = ref(10)
const total = ref(0)
const totalPages = ref(0)
const showForm = ref(false)
const editingStudent = ref(null)
const deletingId = ref(null)
const actionError = ref('')

async function loadStudents() {
  loading.value = true
  error.value = ''
  actionError.value = ''

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

function openCreate() {
  editingStudent.value = null
  showForm.value = true
}

function openEdit(student) {
  editingStudent.value = { ...student }
  showForm.value = true
}

function closeForm() {
  showForm.value = false
  editingStudent.value = null
}

async function onSaved() {
  closeForm()
  await loadStudents()
}

async function onDelete(student) {
  if (deletingId.value) {
    return
  }

  const confirmed = window.confirm(
    'Are you sure you want to delete this student?',
  )
  if (!confirmed) {
    return
  }

  deletingId.value = student.id
  actionError.value = ''

  try {
    const lastOnPage = students.value.length === 1
    await deleteStudent(student.id)
    if (lastOnPage && currentPage.value > 1) {
      currentPage.value -= 1
    }
    await loadStudents()
  } catch (err) {
    const status = err.response && err.response.status
    if (status === 404) {
      actionError.value = 'Student no longer exists.'
    } else {
      actionError.value = 'Unable to delete student. Please try again.'
    }
  } finally {
    deletingId.value = null
  }
}

function fullName(student) {
  return `${student.first_name} ${student.last_name}`
}

function initials(student) {
  const first = (student.first_name || '').trim().charAt(0)
  const last = (student.last_name || '').trim().charAt(0)
  return `${first}${last}`.toUpperCase() || '?'
}

function statusLabel(status) {
  if (!status) return ''
  return status.charAt(0).toUpperCase() + status.slice(1)
}

function emptyMessage() {
  if (selectedStatus.value) {
    return `No ${selectedStatus.value} students match this filter.`
  }
  return 'Try changing the filter or add a new student.'
}

onMounted(loadStudents)
</script>

<template>
  <section class="list">
    <StudentForm
      v-if="showForm"
      :key="editingStudent ? editingStudent.id : 'create'"
      :student="editingStudent"
      @saved="onSaved"
      @cancel="closeForm"
    />

    <template v-else>
      <header class="page-header">
        <div class="page-header-text">
          <p class="eyebrow">Dashboard</p>
          <h1>Student Management System</h1>
          <p class="subtitle">
            Manage student records and enrollment information.
          </p>
        </div>
        <button type="button" class="btn-primary" @click="openCreate">
          <span class="btn-plus" aria-hidden="true">+</span>
          Add Student
        </button>
      </header>

      <div class="controls-card">
        <div class="controls-left">
          <h2 class="section-title">Students</h2>
          <p v-if="!loading && !error" class="section-meta">
            {{ total }} {{ total === 1 ? 'record' : 'records' }} found
          </p>
        </div>
        <StatusFilter
          :model-value="selectedStatus"
          @update:model-value="onStatusChange"
        />
      </div>

      <div v-if="actionError" class="alert alert-error" role="alert">
        <span class="alert-icon" aria-hidden="true">!</span>
        <div>
          <strong>Delete failed</strong>
          <p>{{ actionError }}</p>
        </div>
      </div>

      <div v-if="loading" class="state-card">
        <div class="spinner" aria-hidden="true" />
        <p>Loading students...</p>
      </div>

      <div v-else-if="error" class="alert alert-error" role="alert">
        <span class="alert-icon" aria-hidden="true">!</span>
        <div class="alert-body">
          <strong>Unable to load students</strong>
          <p>{{ error }}</p>
          <button type="button" class="btn-secondary" @click="loadStudents">
            Retry
          </button>
        </div>
      </div>

      <div v-else-if="students.length === 0" class="state-card empty">
        <div class="empty-icon" aria-hidden="true">
          <svg viewBox="0 0 48 48" width="48" height="48" fill="none">
            <rect x="8" y="12" width="32" height="24" rx="4" stroke="currentColor" stroke-width="2" />
            <path d="M16 20h16M16 26h10" stroke="currentColor" stroke-width="2" stroke-linecap="round" />
          </svg>
        </div>
        <h3>No students found</h3>
        <p>{{ emptyMessage() }}</p>
        <button type="button" class="btn-primary" @click="openCreate">
          Add Student
        </button>
      </div>

      <template v-else>
        <div class="table-card">
          <div class="table-scroll">
            <table class="table">
              <thead>
                <tr>
                  <th>Student</th>
                  <th>Email</th>
                  <th>Date of Birth</th>
                  <th>Enrollment Status</th>
                  <th>Actions</th>
                </tr>
              </thead>
              <tbody>
                <tr v-for="student in students" :key="student.id">
                  <td>
                    <div class="student-cell">
                      <span class="avatar" aria-hidden="true">{{ initials(student) }}</span>
                      <span class="student-name">{{ fullName(student) }}</span>
                    </div>
                  </td>
                  <td class="email">{{ student.email }}</td>
                  <td class="dob">{{ student.date_of_birth }}</td>
                  <td>
                    <span
                      class="badge"
                      :class="`badge-${student.enrollment_status}`"
                    >
                      {{ statusLabel(student.enrollment_status) }}
                    </span>
                  </td>
                  <td>
                    <div class="actions">
                      <button
                        type="button"
                        class="btn-action edit"
                        @click="openEdit(student)"
                      >
                        Edit
                      </button>
                      <button
                        type="button"
                        class="btn-action delete"
                        :disabled="deletingId !== null"
                        @click="onDelete(student)"
                      >
                        {{ deletingId === student.id ? 'Deleting...' : 'Delete' }}
                      </button>
                    </div>
                  </td>
                </tr>
              </tbody>
            </table>
          </div>
        </div>
      </template>

      <Pagination
        v-if="!loading && !error"
        :page="currentPage"
        :pages="totalPages"
        :total="total"
        @change="onPageChange"
      />
    </template>
  </section>
</template>

<style scoped>
.page-header {
  display: flex;
  align-items: flex-start;
  justify-content: space-between;
  gap: 1.25rem;
  margin-bottom: 1.5rem;
  color: #fff;
}

.eyebrow {
  margin: 0 0 0.35rem;
  font-size: 0.75rem;
  font-weight: 700;
  letter-spacing: 0.08em;
  text-transform: uppercase;
  opacity: 0.85;
}

.page-header h1 {
  margin: 0;
  font-size: clamp(1.6rem, 3vw, 2rem);
  font-weight: 750;
  letter-spacing: -0.02em;
  line-height: 1.2;
}

.subtitle {
  margin: 0.45rem 0 0;
  max-width: 34rem;
  color: rgba(255, 255, 255, 0.85);
  font-size: 0.98rem;
  line-height: 1.45;
}

.btn-primary {
  display: inline-flex;
  align-items: center;
  gap: 0.4rem;
  flex-shrink: 0;
  padding: 0.7rem 1.15rem;
  border: none;
  border-radius: 10px;
  background: linear-gradient(135deg, #06b6d4 0%, #6366f1 55%, #7c3aed 100%);
  color: #fff;
  font-weight: 700;
  cursor: pointer;
  box-shadow: 0 8px 20px rgba(79, 70, 229, 0.28);
  transition: transform var(--transition), box-shadow var(--transition), filter var(--transition);
}

.btn-primary:hover {
  transform: translateY(-1px);
  filter: brightness(1.05);
  box-shadow: 0 10px 24px rgba(79, 70, 229, 0.35);
}

.btn-primary:active {
  transform: translateY(0);
}

.btn-plus {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  width: 1.25rem;
  height: 1.25rem;
  border-radius: 999px;
  background: rgba(255, 255, 255, 0.2);
  font-size: 1rem;
  line-height: 1;
}

.controls-card {
  display: flex;
  flex-wrap: wrap;
  align-items: flex-end;
  justify-content: space-between;
  gap: 1rem;
  margin-bottom: 1rem;
  padding: 1.1rem 1.2rem;
  background: var(--surface);
  border: 1px solid var(--border);
  border-radius: var(--radius);
  box-shadow: var(--shadow-sm);
}

.section-title {
  margin: 0;
  font-size: 1.1rem;
  font-weight: 700;
}

.section-meta {
  margin: 0.2rem 0 0;
  font-size: 0.875rem;
  color: var(--text-secondary);
}

.table-card {
  background: var(--surface);
  border: 1px solid var(--border);
  border-radius: var(--radius);
  box-shadow: var(--shadow-md);
  overflow: hidden;
}

.table-scroll {
  overflow-x: auto;
}

.table {
  width: 100%;
  border-collapse: collapse;
  min-width: 640px;
}

th,
td {
  text-align: left;
  padding: 0.9rem 1rem;
  border-bottom: 1px solid var(--border);
  vertical-align: middle;
}

th {
  background: var(--surface-muted);
  font-size: 0.75rem;
  font-weight: 700;
  letter-spacing: 0.04em;
  text-transform: uppercase;
  color: var(--text-secondary);
}

tbody tr {
  transition: background var(--transition);
}

tbody tr:hover {
  background: #f8fafc;
}

tbody tr:last-child td {
  border-bottom: none;
}

.student-cell {
  display: flex;
  align-items: center;
  gap: 0.75rem;
}

.avatar {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  width: 2.25rem;
  height: 2.25rem;
  border-radius: 999px;
  background: linear-gradient(135deg, #6366f1, #06b6d4);
  color: #fff;
  font-size: 0.75rem;
  font-weight: 700;
  flex-shrink: 0;
}

.student-name {
  font-weight: 650;
  color: var(--text-primary);
}

.email {
  color: var(--text-secondary);
  font-size: 0.92rem;
}

.dob {
  font-variant-numeric: tabular-nums;
  color: var(--text-primary);
  font-size: 0.92rem;
}

.badge {
  display: inline-flex;
  align-items: center;
  padding: 0.28rem 0.7rem;
  border-radius: 999px;
  font-size: 0.78rem;
  font-weight: 700;
  letter-spacing: 0.01em;
}

.badge-active {
  background: var(--success-soft);
  color: var(--success);
}

.badge-graduated {
  background: var(--primary-soft);
  color: var(--primary-dark);
}

.badge-dropped {
  background: var(--warning-soft);
  color: var(--warning);
}

.actions {
  display: flex;
  flex-wrap: wrap;
  gap: 0.5rem;
}

.btn-action {
  padding: 0.4rem 0.75rem;
  border-radius: 8px;
  border: 1px solid transparent;
  font-size: 0.85rem;
  font-weight: 650;
  cursor: pointer;
  transition:
    background var(--transition),
    border-color var(--transition),
    color var(--transition);
}

.btn-action.edit {
  background: var(--primary-soft);
  color: var(--primary-dark);
  border-color: #c7d2fe;
}

.btn-action.edit:hover {
  background: #e0e7ff;
}

.btn-action.delete {
  background: var(--danger-soft);
  color: var(--danger);
  border-color: #fecaca;
}

.btn-action.delete:hover:not(:disabled) {
  background: #fee2e2;
}

.btn-action:disabled {
  opacity: 0.55;
  cursor: not-allowed;
}

.state-card {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  gap: 0.75rem;
  min-height: 14rem;
  padding: 2rem 1.25rem;
  text-align: center;
  background: var(--surface);
  border: 1px solid var(--border);
  border-radius: var(--radius);
  box-shadow: var(--shadow-sm);
  color: var(--text-secondary);
}

.state-card h3 {
  margin: 0;
  color: var(--text-primary);
  font-size: 1.15rem;
}

.state-card p {
  margin: 0;
  max-width: 24rem;
}

.state-card.empty .empty-icon {
  color: var(--primary);
  opacity: 0.75;
}

.spinner {
  width: 2rem;
  height: 2rem;
  border: 3px solid var(--border);
  border-top-color: var(--primary);
  border-radius: 50%;
  animation: spin 0.7s linear infinite;
}

@keyframes spin {
  to {
    transform: rotate(360deg);
  }
}

.alert {
  display: flex;
  gap: 0.85rem;
  align-items: flex-start;
  margin-bottom: 1rem;
  padding: 1rem 1.1rem;
  border-radius: var(--radius-sm);
  border: 1px solid transparent;
}

.alert-error {
  background: var(--danger-soft);
  border-color: #fecaca;
  color: #7f1d1d;
}

.alert-icon {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  width: 1.5rem;
  height: 1.5rem;
  border-radius: 999px;
  background: var(--danger);
  color: #fff;
  font-weight: 800;
  flex-shrink: 0;
}

.alert p {
  margin: 0.25rem 0 0;
}

.alert-body .btn-secondary {
  margin-top: 0.75rem;
}

.btn-secondary {
  padding: 0.5rem 0.9rem;
  border: 1px solid var(--border-strong);
  border-radius: 8px;
  background: var(--surface);
  color: var(--text-primary);
  font-weight: 650;
  cursor: pointer;
  transition: background var(--transition), border-color var(--transition);
}

.btn-secondary:hover {
  background: var(--surface-muted);
  border-color: var(--primary);
  color: var(--primary-dark);
}

@media (max-width: 720px) {
  .page-header {
    flex-direction: column;
  }

  .btn-primary {
    width: 100%;
    justify-content: center;
  }

  .controls-card {
    align-items: stretch;
  }
}
</style>
