<script setup>
import { useRoute, useRouter } from 'vue-router'
import { navItems } from '../config/routes'

const route = useRoute()
const router = useRouter()

const isActive = (path) => {
  return route.path === path
}

const navigate = (path) => {
  router.push(path)
}
</script>

<template>
  <nav class="nav-sidebar">
    <template v-for="(item, index) in navItems" :key="index">
      <div v-if="item.divider" class="nav-divider"></div>
      <div
        v-else
        class="nav-item"
        :class="{ active: isActive(item.path) }"
        @click="navigate(item.path)"
      >
        <component :is="item.icon" :size="20" />
        <span class="nav-tooltip">{{ item.label }}</span>
      </div>
    </template>
  </nav>
</template>

<style scoped>
.nav-sidebar {
  width: 72px;
  background: var(--bg-tertiary);
  padding: 12px 0;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 8px;
}

.nav-item {
  width: 48px;
  height: 48px;
  border-radius: 50%;
  background: var(--bg-primary);
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  transition: all 0.2s;
  color: var(--text-normal);
  position: relative;
}

.nav-item:hover {
  border-radius: 16px;
  background: var(--blurple);
}

.nav-item.active {
  border-radius: 16px;
  background: var(--blurple);
}

.nav-item::before {
  content: '';
  position: absolute;
  left: -12px;
  width: 4px;
  height: 0;
  background: var(--header-primary);
  border-radius: 0 4px 4px 0;
  transition: height 0.2s;
}

.nav-item:hover::before {
  height: 20px;
}

.nav-item.active::before {
  height: 40px;
}

.nav-divider {
  width: 32px;
  height: 2px;
  background: var(--bg-accent);
  border-radius: 1px;
  margin: 4px 0;
}

.nav-tooltip {
  position: absolute;
  left: 60px;
  background: var(--bg-tertiary);
  color: var(--header-primary);
  padding: 8px 12px;
  border-radius: 4px;
  font-size: 14px;
  font-weight: 500;
  white-space: nowrap;
  opacity: 0;
  pointer-events: none;
  transition: opacity 0.1s;
  z-index: 100;
  box-shadow: 0 8px 16px rgba(0, 0, 0, 0.24);
}

.nav-item:hover .nav-tooltip {
  opacity: 1;
}

@media (max-width: 600px) {
  .nav-sidebar {
    width: 60px;
  }
}
</style>
