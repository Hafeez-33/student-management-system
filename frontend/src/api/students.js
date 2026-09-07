import axios from 'axios'

const api = axios.create({
  baseURL: import.meta.env.VITE_API_BASE_URL || 'http://127.0.0.1:5000',
  headers: {
    'Content-Type': 'application/json',
  },
})

export function getStudents(params = {}) {
  return api.get('/students', { params })
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
