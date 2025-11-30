<script setup>
import { onMounted, onUnmounted } from 'vue'
import NavSidebar from './components/NavSidebar.vue'
import MainHeader from './components/MainHeader.vue'
import PlaybackBar from './components/PlaybackBar.vue'
import ApiKeyPopup from './components/ApiKeyPopup.vue'
import { usePlayerStore } from './composables/usePlayerStore'

const { startPolling, stopPolling } = usePlayerStore()

onMounted(() => {
  startPolling(2000) // Poll every 2 seconds
})

onUnmounted(() => {
  stopPolling()
})
</script>

<template>
  <div class="app-container">
    <NavSidebar />
    <main class="main-area">
      <MainHeader />
      <div class="content">
        <router-view />
      </div>
    </main>
    <PlaybackBar />
    <ApiKeyPopup />
  </div>
</template>

<style scoped>
.app-container {
  display: flex;
  height: 100vh;
}

.main-area {
  flex: 1;
  display: flex;
  flex-direction: column;
  background: var(--bg-primary);
  padding-bottom: 80px;
}

.content {
  flex: 1;
  overflow-y: auto;
  padding: 20px;
}
</style>
