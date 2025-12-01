<script setup lang="ts">
import { useRouter } from 'vue-router'
import { useUserStore } from '../stores/user'
import { onMounted, ref } from 'vue'

const router = useRouter()
const userStore = useUserStore()
const scrollY = ref(0)
const typewriterText = ref('')
const showSecondText = ref(false)

// 打字機效果
const texts = [
  '筆記散落各處？',
  '讓 AI 為你整合'
]
let textIndex = 0
let charIndex = 0
let isDeleting = false

const typeWriter = () => {
  const currentText = texts[textIndex]
  if (!currentText) return

  if (!isDeleting && charIndex < currentText.length) {
    typewriterText.value = currentText.substring(0, charIndex + 1)
    charIndex++
    setTimeout(typeWriter, 100)
  } else if (!isDeleting && charIndex === currentText.length) {
    // 暫停後開始刪除
    setTimeout(() => {
      isDeleting = true
      typeWriter()
    }, 2000)
  } else if (isDeleting && charIndex > 0) {
    typewriterText.value = currentText.substring(0, charIndex - 1)
    charIndex--
    setTimeout(typeWriter, 50)
  } else if (isDeleting && charIndex === 0) {
    isDeleting = false
    textIndex = (textIndex + 1) % texts.length
    if (textIndex === 1) {
      showSecondText.value = true
    }
    setTimeout(typeWriter, 500)
  }
}

onMounted(() => {
  window.addEventListener('scroll', () => {
    scrollY.value = window.scrollY
  })

  // 延遲啟動打字機效果
  setTimeout(() => {
    typeWriter()
  }, 500)
})

function goToNotes() {
  router.push('/notes')
}

function goToMyNotes() {
  router.push('/my-notes')
}

function goToLogin() {
  router.push('/login')
}

// 生成隨機粒子樣式
function getParticleStyle(index: number) {
  const size = Math.random() * 3 + 1
  const left = Math.random() * 100
  const duration = Math.random() * 20 + 10
  const delay = Math.random() * 5

  return {
    width: `${size}px`,
    height: `${size}px`,
    left: `${left}%`,
    animationDuration: `${duration}s`,
    animationDelay: `${delay}s`,
    opacity: Math.random() * 0.5 + 0.3
  }
}
</script>

<template>
  <div class="home">
    <!-- Navigation Bar -->
    <nav class="navbar" :class="{ scrolled: scrollY > 50 }">
      <div class="nav-content">
        <div class="logo">
          <span class="logo-icon">📚</span>
          <span class="logo-text">Roll Call AI</span>
        </div>
        <div class="nav-links">
          <router-link to="/notes" class="nav-link">公開筆記</router-link>
          <router-link to="/collections/public" class="nav-link">合集</router-link>
          <router-link v-if="userStore.isLoggedIn" to="/my-notes" class="nav-link">我的筆記</router-link>
          <router-link v-if="userStore.isLoggedIn" to="/create-note" class="nav-link">上傳</router-link>
          <button v-if="userStore.isLoggedIn" @click="userStore.logout(); router.push('/login')" class="nav-btn logout">
            登出
          </button>
          <router-link v-else to="/login" class="nav-btn login">登入</router-link>
        </div>
      </div>
    </nav>

    <!-- Hero Section -->
    <section class="hero">
      <!-- Animated Background -->
      <div class="particles-bg">
        <div class="particle" v-for="i in 50" :key="i" :style="getParticleStyle(i)"></div>
      </div>

      <div class="hero-content">
        <!-- Typewriter Title -->
        <div class="typewriter-container">
          <h1 class="typewriter-title">
            {{ typewriterText }}
            <span class="cursor">|</span>
          </h1>
        </div>

        <p class="hero-subtitle" :class="{ 'fade-in': showSecondText }">
          使用 AI 技術整合多篇筆記<br>
          讓知識更有條理，學習更有效率
        </p>
        <div class="cta-buttons" :class="{ 'fade-in': showSecondText }">
          <button class="cta-primary pulse-button" @click="goToNotes">
            <span>探索筆記</span>
            <svg width="20" height="20" viewBox="0 0 20 20" fill="none">
              <path d="M7.5 15L12.5 10L7.5 5" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
            </svg>
          </button>
          <button v-if="!userStore.isLoggedIn" class="cta-secondary" @click="goToLogin">
            免費開始
          </button>
          <button v-else class="cta-secondary" @click="goToMyNotes">
            我的筆記
          </button>
        </div>
      </div>

      <!-- Floating Elements -->
      <div class="floating-elements">
        <div class="float-card card-1">🎙️</div>
        <div class="float-card card-2">🤖</div>
        <div class="float-card card-3">📝</div>
        <div class="float-card card-4">✨</div>
      </div>
    </section>

    <!-- Features Section -->
    <section class="features">
      <div class="features-content">
        <div class="section-header">
          <h2>為何選擇 Roll Call AI</h2>
          <p>結合最新 AI 技術，打造全新學習體驗</p>
        </div>

        <div class="features-grid">
          <div class="feature-item">
            <div class="feature-icon">
              <div class="icon-wrapper purple">
                <svg width="32" height="32" viewBox="0 0 24 24" fill="none">
                  <path d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm0 18c-4.41 0-8-3.59-8-8s3.59-8 8-8 8 3.59 8 8-3.59 8-8 8zm-1-13h2v6h-2zm0 8h2v2h-2z" fill="currentColor"/>
                </svg>
              </div>
            </div>
            <h3>即時語音轉錄</h3>
            <p>採用 OpenAI Whisper 技術，支援中英文混合語音，準確率高達 95%</p>
          </div>

          <div class="feature-item">
            <div class="feature-icon">
              <div class="icon-wrapper blue">
                <svg width="32" height="32" viewBox="0 0 24 24" fill="none">
                  <path d="M20 2H4c-1.1 0-2 .9-2 2v16c0 1.1.9 2 2 2h16c1.1 0 2-.9 2-2V4c0-1.1-.9-2-2-2zm-1 18H5c-.55 0-1-.45-1-1V5c0-.55.45-1 1-1h14c.55 0 1 .45 1 1v14c0 .55-.45 1-1 1z" fill="currentColor"/>
                </svg>
              </div>
            </div>
            <h3>AI 智能整合</h3>
            <p>使用 Google Gemini 2.0，自動整合多篇筆記，生成完整學習資料</p>
          </div>

          <div class="feature-item">
            <div class="feature-icon">
              <div class="icon-wrapper green">
                <svg width="32" height="32" viewBox="0 0 24 24" fill="none">
                  <path d="M16 11c1.66 0 2.99-1.34 2.99-3S17.66 5 16 5c-1.66 0-3 1.34-3 3s1.34 3 3 3zm-8 0c1.66 0 2.99-1.34 2.99-3S9.66 5 8 5C6.34 5 5 6.34 5 8s1.34 3 3 3zm0 2c-2.33 0-7 1.17-7 3.5V19h14v-2.5c0-2.33-4.67-3.5-7-3.5zm8 0c-.29 0-.62.02-.97.05 1.16.84 1.97 1.97 1.97 3.45V19h6v-2.5c0-2.33-4.67-3.5-7-3.5z" fill="currentColor"/>
                </svg>
              </div>
            </div>
            <h3>協作分享</h3>
            <p>建立合集、分享筆記，與同學一起學習，共同進步</p>
          </div>
        </div>
      </div>
    </section>

    <!-- Stats Section -->
    <section class="stats">
      <div class="stats-content">
        <div class="stat-item">
          <div class="stat-number">10K+</div>
          <div class="stat-label">筆記數量</div>
        </div>
        <div class="stat-item">
          <div class="stat-number">95%</div>
          <div class="stat-label">轉錄準確率</div>
        </div>
        <div class="stat-item">
          <div class="stat-number">5 秒</div>
          <div class="stat-label">AI 整合速度</div>
        </div>
      </div>
    </section>

    <!-- CTA Section -->
    <section class="final-cta">
      <div class="final-cta-content">
        <h2>準備好開始了嗎？</h2>
        <p>加入我們，體驗 AI 驅動的智能學習</p>
        <button class="cta-large" @click="goToLogin">
          <span v-if="!userStore.isLoggedIn">立即註冊</span>
          <span v-else>前往筆記</span>
        </button>
      </div>
    </section>

    <!-- Footer -->
    <footer class="footer">
      <div class="footer-content">
        <div class="footer-section">
          <h4>Roll Call AI</h4>
          <p>智能課堂助理，讓學習更高效</p>
        </div>
        <div class="footer-section">
          <h4>快速連結</h4>
          <router-link to="/notes">公開筆記</router-link>
          <router-link to="/collections/public">公開合集</router-link>
        </div>
        <div class="footer-section">
          <h4>支援</h4>
          <a href="#">使用說明</a>
          <a href="#">常見問題</a>
        </div>
      </div>
      <div class="footer-bottom">
        <p>&copy; 2025 Roll Call AI. All rights reserved.</p>
      </div>
    </footer>
  </div>
</template>

<style scoped>
* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

.home {
  background: #000;
  color: #fff;
  overflow-x: hidden;
}

/* Navbar */
.navbar {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  z-index: 1000;
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
  background: rgba(0, 0, 0, 0.3);
  backdrop-filter: blur(20px) saturate(180%);
}

.navbar.scrolled {
  background: rgba(0, 0, 0, 0.8);
  backdrop-filter: blur(20px) saturate(180%);
  box-shadow: 0 1px 0 rgba(255, 255, 255, 0.1);
}

.nav-content {
  max-width: 1200px;
  margin: 0 auto;
  padding: 1.2rem 2rem;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.logo {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  font-size: 1.3rem;
  font-weight: 600;
}

.logo-icon {
  font-size: 1.5rem;
}

.logo-text {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}

.nav-links {
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.nav-link {
  color: rgba(255, 255, 255, 0.8);
  text-decoration: none;
  padding: 0.6rem 1rem;
  border-radius: 8px;
  font-size: 0.95rem;
  transition: all 0.2s;
}

.nav-link:hover {
  color: #fff;
  background: rgba(255, 255, 255, 0.1);
}

.nav-btn {
  padding: 0.6rem 1.2rem;
  border-radius: 8px;
  font-size: 0.95rem;
  border: none;
  cursor: pointer;
  transition: all 0.2s;
  font-weight: 500;
}

.nav-btn.logout {
  background: rgba(255, 255, 255, 0.1);
  color: #fff;
}

.nav-btn.logout:hover {
  background: rgba(255, 255, 255, 0.15);
}

.nav-btn.login {
  background: #fff;
  color: #000;
  text-decoration: none;
  display: inline-block;
}

.nav-btn.login:hover {
  background: rgba(255, 255, 255, 0.9);
}

/* Hero Section */
.hero {
  position: relative;
  min-height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 8rem 2rem 4rem;
  background: radial-gradient(ellipse at top, #1e1b4b 0%, #000 50%);
  overflow: hidden;
}

/* Particles Background */
.particles-bg {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  z-index: 1;
  overflow: hidden;
}

.particle {
  position: absolute;
  bottom: -10px;
  background: linear-gradient(135deg, #667eea, #764ba2, #f093fb);
  border-radius: 50%;
  animation: float-up linear infinite;
  pointer-events: none;
}

@keyframes float-up {
  0% {
    transform: translateY(0) rotate(0deg);
    opacity: 1;
  }
  100% {
    transform: translateY(-100vh) rotate(720deg);
    opacity: 0;
  }
}

.hero::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background:
    radial-gradient(circle at 20% 50%, rgba(102, 126, 234, 0.15) 0%, transparent 50%),
    radial-gradient(circle at 80% 80%, rgba(118, 75, 162, 0.15) 0%, transparent 50%);
  animation: pulse 8s ease-in-out infinite;
  z-index: 0;
}

@keyframes pulse {
  0%, 100% { opacity: 1; }
  50% { opacity: 0.8; }
}

.hero-content {
  position: relative;
  z-index: 2;
  text-align: center;
  max-width: 900px;
}

/* Typewriter Effect */
.typewriter-container {
  min-height: 150px;
  display: flex;
  align-items: center;
  justify-content: center;
  margin-bottom: 2rem;
}

.typewriter-title {
  font-size: clamp(2.5rem, 8vw, 5rem);
  font-weight: 700;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 50%, #f093fb 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
  background-size: 200% auto;
  animation: gradientShift 3s linear infinite;
  display: inline-block;
}

.cursor {
  display: inline-block;
  width: 3px;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  margin-left: 5px;
  animation: blink 1s step-end infinite;
}

@keyframes blink {
  0%, 50% { opacity: 1; }
  51%, 100% { opacity: 0; }
}

@keyframes gradientShift {
  to { background-position: 200% center; }
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

.hero-subtitle {
  font-size: clamp(1rem, 3vw, 1.3rem);
  color: rgba(255, 255, 255, 0.7);
  margin-bottom: 3rem;
  line-height: 1.6;
  opacity: 0;
  transition: opacity 0.8s ease-out;
}

.hero-subtitle.fade-in {
  opacity: 1;
}

.cta-buttons {
  display: flex;
  gap: 1rem;
  justify-content: center;
  flex-wrap: wrap;
  opacity: 0;
  transition: opacity 0.8s ease-out 0.3s;
}

.cta-buttons.fade-in {
  opacity: 1;
}

.cta-primary,
.cta-secondary {
  padding: 1rem 2rem;
  border-radius: 12px;
  font-size: 1.1rem;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
  border: none;
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.cta-primary {
  background: #fff;
  color: #000;
}

.cta-primary:hover {
  transform: translateY(-2px);
  box-shadow: 0 20px 40px rgba(255, 255, 255, 0.2);
}

.cta-primary svg {
  transition: transform 0.3s;
}

.cta-primary:hover svg {
  transform: translateX(4px);
}

/* Pulse Animation for Primary Button */
.pulse-button {
  position: relative;
  animation: pulse-glow 2s ease-in-out infinite;
}

@keyframes pulse-glow {
  0%, 100% {
    box-shadow: 0 0 20px rgba(255, 255, 255, 0.3),
                0 0 40px rgba(102, 126, 234, 0.2);
  }
  50% {
    box-shadow: 0 0 30px rgba(255, 255, 255, 0.5),
                0 0 60px rgba(102, 126, 234, 0.4);
  }
}

.cta-secondary {
  background: rgba(255, 255, 255, 0.1);
  color: #fff;
  backdrop-filter: blur(10px);
  border: 1px solid rgba(255, 255, 255, 0.2);
}

.cta-secondary:hover {
  background: rgba(255, 255, 255, 0.15);
  border-color: rgba(255, 255, 255, 0.3);
}

/* Floating Elements */
.floating-elements {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  pointer-events: none;
}

.float-card {
  position: absolute;
  font-size: 3rem;
  opacity: 0.1;
  animation: float 20s ease-in-out infinite;
}

.card-1 {
  top: 20%;
  left: 10%;
  animation-delay: 0s;
}

.card-2 {
  top: 60%;
  right: 15%;
  animation-delay: -5s;
}

.card-3 {
  bottom: 25%;
  left: 15%;
  animation-delay: -10s;
}

.card-4 {
  top: 40%;
  right: 10%;
  animation-delay: -15s;
}

@keyframes float {
  0%, 100% {
    transform: translateY(0) rotate(0deg);
  }
  25% {
    transform: translateY(-20px) rotate(5deg);
  }
  50% {
    transform: translateY(0) rotate(0deg);
  }
  75% {
    transform: translateY(20px) rotate(-5deg);
  }
}

/* Features Section */
.features {
  padding: 8rem 2rem;
  background: linear-gradient(180deg, #000 0%, #0a0a0a 100%);
}

.features-content {
  max-width: 1200px;
  margin: 0 auto;
}

.section-header {
  text-align: center;
  margin-bottom: 5rem;
}

.section-header h2 {
  font-size: clamp(2rem, 5vw, 3.5rem);
  font-weight: 700;
  margin-bottom: 1rem;
}

.section-header p {
  font-size: 1.2rem;
  color: rgba(255, 255, 255, 0.6);
}

.features-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
  gap: 3rem;
}

.feature-item {
  text-align: center;
  padding: 2rem;
  border-radius: 20px;
  background: rgba(255, 255, 255, 0.03);
  backdrop-filter: blur(10px);
  border: 1px solid rgba(255, 255, 255, 0.05);
  transition: all 0.3s;
}

.feature-item:hover {
  transform: translateY(-10px);
  background: rgba(255, 255, 255, 0.05);
  border-color: rgba(255, 255, 255, 0.1);
}

.feature-icon {
  margin-bottom: 1.5rem;
}

.icon-wrapper {
  width: 80px;
  height: 80px;
  margin: 0 auto;
  border-radius: 20px;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: transform 0.3s;
}

.feature-item:hover .icon-wrapper {
  transform: scale(1.1) rotate(5deg);
}

.icon-wrapper.purple {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
}

.icon-wrapper.blue {
  background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);
}

.icon-wrapper.green {
  background: linear-gradient(135deg, #43e97b 0%, #38f9d7 100%);
}

.feature-item h3 {
  font-size: 1.5rem;
  margin-bottom: 1rem;
}

.feature-item p {
  color: rgba(255, 255, 255, 0.7);
  line-height: 1.6;
}

/* Stats Section */
.stats {
  padding: 6rem 2rem;
  background: #000;
}

.stats-content {
  max-width: 1200px;
  margin: 0 auto;
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 3rem;
  text-align: center;
}

.stat-item {
  padding: 2rem;
}

.stat-number {
  font-size: 3.5rem;
  font-weight: 700;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
  margin-bottom: 0.5rem;
}

.stat-label {
  font-size: 1.1rem;
  color: rgba(255, 255, 255, 0.6);
}

/* Final CTA */
.final-cta {
  padding: 8rem 2rem;
  background: radial-gradient(ellipse at center, #1e1b4b 0%, #000 70%);
  text-align: center;
}

.final-cta-content {
  max-width: 800px;
  margin: 0 auto;
}

.final-cta-content h2 {
  font-size: clamp(2rem, 5vw, 3.5rem);
  font-weight: 700;
  margin-bottom: 1rem;
}

.final-cta-content p {
  font-size: 1.3rem;
  color: rgba(255, 255, 255, 0.7);
  margin-bottom: 3rem;
}

.cta-large {
  padding: 1.5rem 3rem;
  font-size: 1.3rem;
  font-weight: 600;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: #fff;
  border: none;
  border-radius: 16px;
  cursor: pointer;
  transition: all 0.3s;
}

.cta-large:hover {
  transform: translateY(-4px) scale(1.05);
  box-shadow: 0 25px 50px rgba(102, 126, 234, 0.4);
}

/* Footer */
.footer {
  background: #000;
  border-top: 1px solid rgba(255, 255, 255, 0.1);
  padding: 4rem 2rem 2rem;
}

.footer-content {
  max-width: 1200px;
  margin: 0 auto;
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 3rem;
  margin-bottom: 3rem;
}

.footer-section h4 {
  font-size: 1.1rem;
  margin-bottom: 1rem;
}

.footer-section p {
  color: rgba(255, 255, 255, 0.6);
  line-height: 1.6;
}

.footer-section a {
  display: block;
  color: rgba(255, 255, 255, 0.6);
  text-decoration: none;
  margin-bottom: 0.5rem;
  transition: color 0.2s;
}

.footer-section a:hover {
  color: #fff;
}

.footer-bottom {
  text-align: center;
  padding-top: 2rem;
  border-top: 1px solid rgba(255, 255, 255, 0.1);
  color: rgba(255, 255, 255, 0.5);
}

/* Responsive */
@media (max-width: 768px) {
  .nav-links {
    display: none;
  }

  .hero {
    padding: 6rem 1.5rem 3rem;
  }

  .features-grid {
    grid-template-columns: 1fr;
  }

  .stats-content {
    grid-template-columns: 1fr;
    gap: 2rem;
  }
}
</style>
