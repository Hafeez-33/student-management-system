<script setup>
import { computed, reactive, ref, watch } from 'vue'
import { createStudent, updateStudent } from '../api/students'

const EMAIL_RE = /^[^@\s]+@[^@\s]+\.[^@\s]+$/
const STATUSES = ['active', 'graduated', 'dropped']

const props = defineProps({
  student: {
    type: Object,
    default: null,
  },
})

const emit = defineEmits(['saved', 'cancel'])

const isEdit = computed(() => Boolean(props.student && props.student.id))

const form = reactive(emptyForm())
const fieldErrors = reactive(emptyErrors())
const formError = ref('')
const submitting = ref(false)

function emptyForm() {
  return {
    first_name: '',
    last_name: '',
    email: '',
    date_of_birth: '',
    enrollment_status: 'active',
  }
}

function emptyErrors() {
  return {
    first_name: '',
    last_name: '',
    email: '',
    date_of_birth: '',
    enrollment_status: '',
  }
}

function todayLocalIso() {
  const now = new Date()
  const year = now.getFullYear()
  const month = String(now.getMonth() + 1).padStart(2, '0')
  const day = String(now.getDate()).padStart(2, '0')
  return `${year}-${month}-${day}`
}

function fillForm(student) {
  Object.assign(form, emptyForm())
  Object.assign(fieldErrors, emptyErrors())
  formError.value = ''
  submitting.value = false

  if (!student) {
    return
  }

  form.first_name = student.first_name || ''
  form.last_name = student.last_name || ''
  form.email = student.email || ''
  form.date_of_birth = student.date_of_birth || ''
  form.enrollment_status = student.enrollment_status || 'active'
}

watch(
  () => props.student,
  (student) => fillForm(student),
  { immediate: true },
)

function validate() {
  Object.assign(fieldErrors, emptyErrors())

  const first = form.first_name.trim()
  const last = form.last_name.trim()
  const email = form.email.trim().toLowerCase()
  const dob = form.date_of_birth.trim()
  const status = form.enrollment_status

  if (!first) {
    fieldErrors.first_name = 'First name is required'
  }
  if (!last) {
    fieldErrors.last_name = 'Last name is required'
  }
  if (!email) {
    fieldErrors.email = 'Email is required'
  } else if (!EMAIL_RE.test(email)) {
    fieldErrors.email = 'Enter a valid email address'
  }
  if (!dob) {
    fieldErrors.date_of_birth = 'Date of birth is required'
  } else if (Number.isNaN(Date.parse(`${dob}T00:00:00`))) {
    fieldErrors.date_of_birth = 'Enter a valid date'
  } else if (dob > todayLocalIso()) {
    fieldErrors.date_of_birth = 'Date of birth cannot be in the future'
  }
  if (!status || !STATUSES.includes(status)) {
    fieldErrors.enrollment_status = 'Select an enrollment status'
  }

  return !Object.values(fieldErrors).some(Boolean)
}

function payload() {
  return {
    first_name: form.first_name.trim(),
    last_name: form.last_name.trim(),
    email: form.email.trim().toLowerCase(),
    date_of_birth: form.date_of_birth.trim(),
    enrollment_status: form.enrollment_status,
  }
}

function applyServerErrors(error) {
  const response = error.response
  if (!response) {
    formError.value = 'Unable to save student. Please try again.'
    return
  }

  const data = response.data || {}
  const details = data.details || {}

  if (response.status === 409) {
    fieldErrors.email = 'A student with this email already exists.'
    formError.value = data.error || 'Conflict'
    return
  }

  if (response.status === 400 && details) {
    for (const field of Object.keys(fieldErrors)) {
      if (details[field]) {
        fieldErrors[field] = details[field]
      }
    }
    formError.value = data.error || 'Validation failed'
    return
  }

  formError.value = data.error || 'Unable to save student. Please try again.'
}

async function onSubmit() {
  if (submitting.value) {
    return
  }

  formError.value = ''
  if (!validate()) {
    return
  }

  submitting.value = true
  try {
    if (isEdit.value) {
      await updateStudent(props.student.id, payload())
    } else {
      await createStudent(payload())
    }
    emit('saved')
  } catch (error) {
    applyServerErrors(error)
  } finally {
    submitting.value = false
  }
}

function onCancel() {
  fillForm(null)
  emit('cancel')
}
</script>

<template>
  <div class="form-shell">
    <form class="form-card" @submit.prevent="onSubmit" novalidate>
      <header class="form-header">
        <p class="eyebrow">{{ isEdit ? 'Update record' : 'New record' }}</p>
        <h2>{{ isEdit ? 'Edit Student' : 'Add Student' }}</h2>
        <p class="form-subtitle">
          {{ isEdit
            ? 'Update the student details below and save your changes.'
            : 'Fill in the details below to create a new student.' }}
        </p>
      </header>

      <div v-if="formError" class="form-alert" role="alert">
        <span class="alert-mark" aria-hidden="true">!</span>
        <span>{{ formError }}</span>
      </div>

      <div class="grid">
        <label class="field" :class="{ invalid: fieldErrors.first_name }">
          <span class="label">First name <span class="req">*</span></span>
          <input
            v-model="form.first_name"
            type="text"
            autocomplete="given-name"
            :aria-invalid="Boolean(fieldErrors.first_name)"
          />
          <span v-if="fieldErrors.first_name" class="field-error">{{ fieldErrors.first_name }}</span>
        </label>

        <label class="field" :class="{ invalid: fieldErrors.last_name }">
          <span class="label">Last name <span class="req">*</span></span>
          <input
            v-model="form.last_name"
            type="text"
            autocomplete="family-name"
            :aria-invalid="Boolean(fieldErrors.last_name)"
          />
          <span v-if="fieldErrors.last_name" class="field-error">{{ fieldErrors.last_name }}</span>
        </label>

        <label class="field" :class="{ invalid: fieldErrors.email }">
          <span class="label">Email <span class="req">*</span></span>
          <input
            v-model="form.email"
            type="email"
            autocomplete="email"
            :aria-invalid="Boolean(fieldErrors.email)"
          />
          <span v-if="fieldErrors.email" class="field-error">{{ fieldErrors.email }}</span>
        </label>

        <label class="field" :class="{ invalid: fieldErrors.date_of_birth }">
          <span class="label">Date of birth <span class="req">*</span></span>
          <input
            v-model="form.date_of_birth"
            type="date"
            :max="todayLocalIso()"
            :aria-invalid="Boolean(fieldErrors.date_of_birth)"
          />
          <span v-if="fieldErrors.date_of_birth" class="field-error">{{ fieldErrors.date_of_birth }}</span>
        </label>

        <label class="field field-full" :class="{ invalid: fieldErrors.enrollment_status }">
          <span class="label">Enrollment status <span class="req">*</span></span>
          <select
            v-model="form.enrollment_status"
            :aria-invalid="Boolean(fieldErrors.enrollment_status)"
          >
            <option value="active">Active</option>
            <option value="graduated">Graduated</option>
            <option value="dropped">Dropped</option>
          </select>
          <span v-if="fieldErrors.enrollment_status" class="field-error">{{ fieldErrors.enrollment_status }}</span>
        </label>
      </div>

      <div class="form-actions">
        <button type="button" class="btn-cancel" :disabled="submitting" @click="onCancel">
          Cancel
        </button>
        <button type="submit" class="btn-submit" :disabled="submitting">
          {{ submitting ? (isEdit ? 'Updating...' : 'Creating...') : (isEdit ? 'Save changes' : 'Create student') }}
        </button>
      </div>
    </form>
  </div>
</template>

<style scoped>
.form-shell {
  display: flex;
  justify-content: center;
  padding: 0.5rem 0 1rem;
}

.form-card {
  width: 100%;
  max-width: 40rem;
  padding: 1.5rem 1.5rem 1.35rem;
  background: var(--surface);
  border: 1px solid var(--border);
  border-radius: var(--radius);
  box-shadow: var(--shadow-md);
}

.form-header {
  margin-bottom: 1.25rem;
  padding-bottom: 1rem;
  border-bottom: 1px solid var(--border);
}

.eyebrow {
  margin: 0 0 0.3rem;
  font-size: 0.72rem;
  font-weight: 700;
  letter-spacing: 0.08em;
  text-transform: uppercase;
  color: var(--primary);
}

.form-header h2 {
  margin: 0;
  font-size: 1.45rem;
  letter-spacing: -0.02em;
}

.form-subtitle {
  margin: 0.4rem 0 0;
  color: var(--text-secondary);
  font-size: 0.92rem;
  line-height: 1.4;
}

.form-alert {
  display: flex;
  align-items: flex-start;
  gap: 0.65rem;
  margin-bottom: 1rem;
  padding: 0.8rem 0.9rem;
  border-radius: var(--radius-sm);
  background: var(--danger-soft);
  border: 1px solid #fecaca;
  color: #7f1d1d;
  font-size: 0.9rem;
}

.alert-mark {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  width: 1.25rem;
  height: 1.25rem;
  border-radius: 999px;
  background: var(--danger);
  color: #fff;
  font-size: 0.75rem;
  font-weight: 800;
  flex-shrink: 0;
}

.grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 1rem;
}

.field {
  display: flex;
  flex-direction: column;
  gap: 0.35rem;
}

.field-full {
  grid-column: 1 / -1;
}

.label {
  font-size: 0.85rem;
  font-weight: 650;
  color: var(--text-primary);
}

.req {
  color: var(--danger);
}

input,
select {
  width: 100%;
  padding: 0.65rem 0.75rem;
  border: 1px solid var(--border);
  border-radius: var(--radius-sm);
  background: var(--surface);
  color: var(--text-primary);
  transition: border-color var(--transition), box-shadow var(--transition);
}

input:hover,
select:hover {
  border-color: var(--border-strong);
}

input:focus,
select:focus {
  border-color: var(--primary);
}

.field.invalid input,
.field.invalid select {
  border-color: var(--danger);
  background: #fffafa;
}

.field-error {
  color: var(--danger);
  font-size: 0.8rem;
}

.form-actions {
  display: flex;
  justify-content: flex-end;
  gap: 0.75rem;
  margin-top: 1.35rem;
  padding-top: 1rem;
  border-top: 1px solid var(--border);
}

.btn-cancel,
.btn-submit {
  padding: 0.65rem 1.1rem;
  border-radius: 10px;
  font-weight: 700;
  cursor: pointer;
  transition: background var(--transition), border-color var(--transition), transform var(--transition);
}

.btn-cancel {
  border: 1px solid var(--border);
  background: var(--surface);
  color: var(--text-primary);
}

.btn-cancel:hover:not(:disabled) {
  background: var(--surface-muted);
}

.btn-submit {
  border: none;
  background: linear-gradient(135deg, #4f46e5, #7c3aed);
  color: #fff;
  box-shadow: 0 6px 16px rgba(79, 70, 229, 0.25);
}

.btn-submit:hover:not(:disabled) {
  filter: brightness(1.05);
  transform: translateY(-1px);
}

.btn-cancel:disabled,
.btn-submit:disabled {
  opacity: 0.6;
  cursor: not-allowed;
  transform: none;
}

@media (max-width: 640px) {
  .grid {
    grid-template-columns: 1fr;
  }

  .form-card {
    padding: 1.15rem;
  }

  .form-actions {
    flex-direction: column-reverse;
  }

  .btn-cancel,
  .btn-submit {
    width: 100%;
  }
}
</style>
