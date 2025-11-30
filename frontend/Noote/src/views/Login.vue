<script setup lang="ts">
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { authService } from '../services/auth'
import { useUserStore } from '../stores/user'

const router = useRouter()
const userStore = useUserStore()

const username = ref('')
const password = ref('')
const error = ref('')
const loading = ref(false)

async function handleLogin() {
  if (!username.value || !password.value) {
    error.value = '請填寫所有欄位'
    return
  }

  loading.value = true
  error.value = ''

  try {
    await authService.login({
      username: username.value,
      password: password.value,
    })

    await userStore.fetchUser()
    router.push('/')
  } catch (err: any) {
    error.value = err.response?.data?.detail || '登入失敗'
  } finally {
    loading.value = false
  }
}
</script>

<template>
  <div class="login-container">
    <!-- Background gradient overlay -->
    <div class="gradient-bg"></div>

    <!-- Floating elements -->
    <div class="floating-element" style="top: 10%; left: 10%">🔐</div>
    <div class="floating-element" style="top: 20%; right: 15%">✨</div>
    <div class="floating-element" style="bottom: 15%; left: 20%">🎯</div>
    <div class="floating-element" style="bottom: 25%; right: 10%">💫</div>

    <div class="login-card">
      <div class="card-glow"></div>

      <h1 class="title">
        <span class="gradient-text">歡迎回來</span>
      </h1>
      <p class="subtitle">登入你的帳號</p>

      <form @submit.prevent="handleLogin">
        <div class="form-group">
          <label for="username">用戶名</label>
          <input
            id="username"
            v-model="username"
            type="text"
            placeholder="請輸入用戶名"
            required
          />
        </div>

        <div class="form-group">
          <label for="password">密碼</label>
          <input
            id="password"
            v-model="password"
            type="password"
            placeholder="請輸入密碼"
            required
          />
        </div>

        <div v-if="error" class="error-message">
          <span class="error-icon">⚠️</span>
          {{ error }}
        </div>

        <button type="submit" :disabled="loading" class="submit-btn">
          <span v-if="!loading">登入</span>
          <span v-else class="loading-text">
            <span class="spinner"></span>
            登入中...
          </span>
        </button>
      </form>

      <div class="footer">
        還沒有帳號？
        <router-link to="/register" class="link">立即註冊</router-link>
      </div>
    </div>
  </div>
</template>

<style scoped>
.login-container {
  position: relative;
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 100vh;
  background: #000;
  overflow: hidden;
}

.gradient-bg {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: radial-gradient(circle at 20% 30%, rgba(102, 126, 234, 0.2) 0%, transparent 50%),
              radial-gradient(circle at 80% 70%, rgba(118, 75, 162, 0.2) 0%, transparent 50%);
  z-index: 0;
}

.floating-element {
  position: absolute;
  font-size: clamp(2rem, 4vw, 3rem);
  opacity: 0.3;
  animation: float 6s ease-in-out infinite;
  z-index: 0;
}

.floating-element:nth-child(2) {
  animation-delay: -2s;
}

.floating-element:nth-child(3) {
  animation-delay: -4s;
}

.floating-element:nth-child(4) {
  animation-delay: -1s;
}

@keyframes float {
  0%, 100% {
    transform: translateY(0) rotate(0deg);
  }
  25% {
    transform: translateY(-20px) rotate(5deg);
  }
  50% {
    transform: translateY(-10px) rotate(-5deg);
  }
  75% {
    transform: translateY(-15px) rotate(3deg);
  }
}

.login-card {
  position: relative;
  background: rgba(255, 255, 255, 0.08);
  backdrop-filter: blur(30px);
  border: 1px solid rgba(255, 255, 255, 0.15);
  padding: 3rem;
  border-radius: 24px;
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.4);
  width: 100%;
  max-width: 440px;
  z-index: 1;
  animation: fadeInUp 0.8s ease-out;
}

@keyframes fadeInUp {
  from {
    opacity: 0;
    transform: translateY(30px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.card-glow {
  position: absolute;
  top: -2px;
  left: -2px;
  right: -2px;
  bottom: -2px;
  background: linear-gradient(135deg, rgba(102, 126, 234, 0.3), rgba(118, 75, 162, 0.3));
  border-radius: 24px;
  opacity: 0;
  transition: opacity 0.3s;
  z-index: -1;
}

.login-card:hover .card-glow {
  opacity: 1;
}

.title {
  text-align: center;
  margin-bottom: 0.5rem;
  font-size: clamp(2rem, 5vw, 2.5rem);
  font-weight: 700;
}

.gradient-text {
  background: linear-gradient(135deg, #667eea, #764ba2, #f093fb);
  background-size: 200% 200%;
  background-clip: text;
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  animation: gradientShift 3s ease infinite;
}

@keyframes gradientShift {
  0%, 100% {
    background-position: 0% 50%;
  }
  50% {
    background-position: 100% 50%;
  }
}

.subtitle {
  text-align: center;
  color: rgba(255, 255, 255, 0.6);
  margin-bottom: 2rem;
  font-size: 1rem;
}

.form-group {
  margin-bottom: 1.5rem;
}

label {
  display: block;
  margin-bottom: 0.5rem;
  color: rgba(255, 255, 255, 0.8);
  font-weight: 500;
  font-size: 0.9rem;
}

input {
  width: 100%;
  padding: 0.9rem 1rem;
  background: rgba(255, 255, 255, 0.08);
  border: 1px solid rgba(255, 255, 255, 0.15);
  border-radius: 12px;
  font-size: 1rem;
  color: #fff;
  box-sizing: border-box;
  transition: all 0.3s;
}

input::placeholder {
  color: rgba(255, 255, 255, 0.3);
}

input:focus {
  outline: none;
  background: rgba(255, 255, 255, 0.12);
  border-color: #667eea;
  box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1);
}

.submit-btn {
  width: 100%;
  padding: 1rem;
  background: linear-gradient(135deg, #667eea, #764ba2);
  color: white;
  border: none;
  border-radius: 12px;
  font-size: 1rem;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s;
  margin-top: 0.5rem;
}

.submit-btn:hover:not(:disabled) {
  transform: translateY(-2px);
  box-shadow: 0 8px 20px rgba(102, 126, 234, 0.4);
}

.submit-btn:active:not(:disabled) {
  transform: translateY(0);
}

.submit-btn:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

.loading-text {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 0.5rem;
}

.spinner {
  width: 16px;
  height: 16px;
  border: 2px solid rgba(255, 255, 255, 0.3);
  border-top-color: white;
  border-radius: 50%;
  animation: spin 0.8s linear infinite;
}

@keyframes spin {
  to {
    transform: rotate(360deg);
  }
}

.error-message {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  color: #fc8181;
  margin-bottom: 1rem;
  padding: 0.9rem;
  background: rgba(252, 129, 129, 0.1);
  border-radius: 12px;
  border: 1px solid rgba(252, 129, 129, 0.2);
  font-size: 0.9rem;
}

.error-icon {
  font-size: 1.2rem;
}

.footer {
  text-align: center;
  margin-top: 2rem;
  color: rgba(255, 255, 255, 0.6);
  font-size: 0.9rem;
}

.link {
  color: #667eea;
  text-decoration: none;
  font-weight: 600;
  transition: color 0.3s;
}

.link:hover {
  color: #764ba2;
}

@media (max-width: 768px) {
  .login-card {
    padding: 2rem;
    margin: 1rem;
  }

  .floating-element {
    display: none;
  }
}
</style>
