import api from './api'

export interface Note {
  id?: number
  title: string
  content: string
  file_type: string
  is_public: boolean
  user_id?: number
  owner_username?: string
  created_at?: string
  updated_at?: string
}

export const notesService = {
  async createNote(note: Note) {
    const response = await api.post('/notes/', note)
    return response.data
  },

  async getPublicNotes(skip = 0, limit = 20) {
    const response = await api.get(`/notes/?skip=${skip}&limit=${limit}`)
    return response.data
  },

  async getMyNotes() {
    const response = await api.get('/notes/my')
    return response.data
  },

  async getNote(id: number) {
    const response = await api.get(`/notes/${id}`)
    return response.data
  },

  async updateNote(id: number, note: Partial<Note>) {
    const response = await api.put(`/notes/${id}`, note)
    return response.data
  },

  async deleteNote(id: number) {
    await api.delete(`/notes/${id}`)
  },

  async searchNotes(query: string, scope: 'public' | 'my' | 'all' = 'public') {
    const response = await api.get(`/notes/search?q=${encodeURIComponent(query)}&scope=${scope}`)
    return response.data
  },
}
