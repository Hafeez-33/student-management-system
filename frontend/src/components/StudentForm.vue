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
  <form class="form" @submit.prevent="onSubmit">
    <h2>{{ isEdit ? 'Edit student' : 'Add student' }}</h2>

    <p v-if="formError" class="form-error" role="alert">{{ formError }}</p>

    <label>
      First name <span class="req">*</span>
      <input v-model="form.first_name" type="text" autocomplete="given-name" />
      <span v-if="fieldErrors.first_name" class="field-error">{{ fieldErrors.first_name }}</span>
    </label>

    <label>
      Last name <span class="req">*</span>
      <input v-model="form.last_name" type="text" autocomplete="family-name" />
      <span v-if="fieldErrors.last_name" class="field-error">{{ fieldErrors.last_name }}</span>
    </label>

    <label>
      Email <span class="req">*</span>
      <input v-model="form.email" type="email" autocomplete="email" />
      <span v-if="fieldErrors.email" class="field-error">{{ fieldErrors.email }}</span>
    </label>

    <label>
      Date of birth <span class="req">*</span>
      <input v-model="form.date_of_birth" type="date" :max="todayLocalIso()" />
      <span v-if="fieldErrors.date_of_birth" class="field-error">{{ fieldErrors.date_of_birth }}</span>
    </label>

    <label>
      Enrollment status <span class="req">*</span>
      <select v-model="form.enrollment_status">
        <option value="active">Active</option>
        <option value="graduated">Graduated</option>
        <option value="dropped">Dropped</option>
      </select>
      <span v-if="fieldErrors.enrollment_status" class="field-error">{{ fieldErrors.enrollment_status }}</span>
    </label>

    <div class="actions">
      <button type="submit" :disabled="submitting">
        {{ submitting ? (isEdit ? 'Updating...' : 'Creating...') : (isEdit ? 'Save changes' : 'Create student') }}
      </button>
      <button type="button" :disabled="submitting" @click="onCancel">Cancel</button>
    </div>
  </form>
</template>

<style scoped>
.form {
  margin-top: 1.5rem;
  max-width: 28rem;
  padding: 1.25rem;
  background: #fff;
  border: 1px solid #e3e3e3;
  border-radius: 8px;
}

.form h2 {
  margin-top: 0;
}

label {
  display: block;
  margin-bottom: 0.9rem;
  font-size: 0.95rem;
}

input,
select {
  display: block;
  width: 100%;
  margin-top: 0.3rem;
  padding: 0.4rem 0.5rem;
  box-sizing: border-box;
}

.req {
  color: #b42318;
}

.field-error,
.form-error {
  color: #8a1f11;
  font-size: 0.85rem;
}

.form-error {
  margin-bottom: 1rem;
}

.actions {
  display: flex;
  gap: 0.75rem;
  margin-top: 1rem;
}

button {
  padding: 0.45rem 0.8rem;
  cursor: pointer;
}

button:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}
</style>
