import api from './api'

export interface Collection {
  id?: number
  name: string
  description: string
  cover_image?: string
  is_public: boolean
  user_id?: number
  owner_username?: string
  note_count?: number
  created_at?: string
  updated_at?: string
}

export interface IntegrationRequest {
  custom_prompt?: string
  api_key: string
}

export interface IntegrationResponse {
  integrated_content: string
  note_count: number
  created_at: string
}

export const collectionsService = {
  async createCollection(collection: Collection) {
    const response = await api.post('/collections/', collection)
    return response.data
  },

  async getPublicCollections(skip = 0, limit = 20) {
    const response = await api.get(`/collections/?skip=${skip}&limit=${limit}`)
    return response.data
  },

  async getMyCollections() {
    const response = await api.get('/collections/my')
    return response.data
  },

  async getCollection(id: number) {
    const response = await api.get(`/collections/${id}`)
    return response.data
  },

  async updateCollection(id: number, collection: Partial<Collection>) {
    const response = await api.put(`/collections/${id}`, collection)
    return response.data
  },

  async deleteCollection(id: number) {
    await api.delete(`/collections/${id}`)
  },

  async getCollectionNotes(id: number) {
    const response = await api.get(`/collections/${id}/notes`)
    return response.data
  },

  async addNoteToCollection(collectionId: number, noteId: number) {
    const response = await api.post(`/collections/${collectionId}/notes`, {
      note_id: noteId
    })
    return response.data
  },

  async removeNoteFromCollection(collectionId: number, noteId: number) {
    await api.delete(`/collections/${collectionId}/notes/${noteId}`)
  },

  async reorderCollectionNotes(collectionId: number, noteIds: number[]) {
    const response = await api.put(`/collections/${collectionId}/notes/reorder`, {
      note_ids: noteIds
    })
    return response.data
  },

  async integrateCollectionNotes(
    collectionId: number,
    request: IntegrationRequest
  ): Promise<IntegrationResponse> {
    const response = await api.post(`/collections/${collectionId}/integrate`, request)
    return response.data
  },
}
