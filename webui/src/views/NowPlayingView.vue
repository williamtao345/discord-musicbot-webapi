<script setup>
import NowPlayingHero from '../components/NowPlayingHero.vue'
import QueueSection from '../components/QueueSection.vue'
</script>

<template>
  <div class="now-playing-view">
    <NowPlayingHero />
    <QueueSection />
  </div>
</template>

<style scoped>
.now-playing-view {
  max-width: 1200px;
}
</style>
