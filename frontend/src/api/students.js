import axios from 'axios'

const api = axios.create({
  baseURL: import.meta.env.VITE_API_BASE_URL || 'http://127.0.0.1:5000',
  headers: {
    'Content-Type': 'application/json',
  },
})

export function getStudents(params = {}) {
  const query = {}

  if (params.page != null && params.page !== '') {
    query.page = params.page
  }
  if (params.per_page != null && params.per_page !== '') {
    query.per_page = params.per_page
  }
  if (params.enrollment_status) {
    query.enrollment_status = params.enrollment_status
  }

  return api.get('/students', { params: query })
}

export function getStudent(id) {
  return api.get(`/students/${id}`)
}

export function createStudent(data) {
  return api.post('/students', data)
}

export function updateStudent(id, data) {
  return api.put(`/students/${id}`, data)
}

export function deleteStudent(id) {
  return api.delete(`/students/${id}`)
}
