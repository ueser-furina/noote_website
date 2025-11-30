import api from './api'

export interface RegisterData {
  username: string
  email: string
  password: string
}

export interface LoginData {
  username: string
  password: string
}

export const authService = {
  async register(data: RegisterData) {
    const response = await api.post('/auth/register', data)
    return response.data
  },

  async login(data: LoginData) {
    const formData = new FormData()
    formData.append('username', data.username)
    formData.append('password', data.password)

    const response = await api.post('/auth/login', formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
    })

    const { access_token } = response.data
    localStorage.setItem('token', access_token)
    return response.data
  },

  async getCurrentUser() {
    const response = await api.get('/auth/me')
    return response.data
  },

  logout() {
    localStorage.removeItem('token')
  },

  isAuthenticated(): boolean {
    return !!localStorage.getItem('token')
  },
}
