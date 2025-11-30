<script setup>
import { ref } from 'vue'

const props = defineProps({
  value: {
    type: Number,
    default: 0
  },
  disabled: {
    type: Boolean,
    default: false
  }
})

const emit = defineEmits(['change', 'update:value'])
const trackRef = ref(null)

const handleClick = (e) => {
  if (props.disabled) return
  const rect = trackRef.value.getBoundingClientRect()
  const percent = Math.max(0, Math.min(100, ((e.clientX - rect.left) / rect.width) * 100))
  emit('change', percent)
  emit('update:value', percent)
}
</script>

<template>
  <div
    class="slider-track"
    ref="trackRef"
    @click="handleClick"
    :class="{ disabled }"
  >
    <div class="slider-fill" :style="{ width: value + '%' }">
      <div class="slider-handle"></div>
    </div>
  </div>
</template>

<style scoped>
.slider-track {
  flex: 1;
  height: 4px;
  background: var(--bg-accent);
  border-radius: 2px;
  cursor: pointer;
  position: relative;
}

.slider-track:hover .slider-fill {
  background: var(--blurple);
}

.slider-track:hover .slider-handle {
  opacity: 1;
}

.slider-fill {
  height: 100%;
  background: var(--header-primary);
  border-radius: 2px;
  position: relative;
  transition: background 0.2s ease;
}

.slider-handle {
  position: absolute;
  right: -6px;
  top: 50%;
  transform: translateY(-50%);
  width: 12px;
  height: 12px;
  background: var(--header-primary);
  border-radius: 50%;
  opacity: 0;
  transition: opacity 0.1s;
}

.slider-track.disabled {
  cursor: not-allowed;
  opacity: 0.5;
}
</style>
