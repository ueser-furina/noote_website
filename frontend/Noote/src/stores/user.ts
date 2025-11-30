import { defineStore } from 'pinia'
import { ref } from 'vue'
import { authService } from '../services/auth'

export const useUserStore = defineStore('user', () => {
  const user = ref<any>(null)
  const isLoggedIn = ref(false)

  async function fetchUser() {
    try {
      user.value = await authService.getCurrentUser()
      isLoggedIn.value = true
    } catch (error) {
      user.value = null
      isLoggedIn.value = false
    }
  }

  function logout() {
    authService.logout()
    user.value = null
    isLoggedIn.value = false
  }

  return {
    user,
    isLoggedIn,
    fetchUser,
    logout,
  }
})
