<script setup>
import { ref, computed, onUnmounted } from 'vue'

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
const isDragging = ref(false)
const dragValue = ref(0)

// Display value: show drag preview while dragging, otherwise show prop value
const displayValue = computed(() => isDragging.value ? dragValue.value : props.value)

const getPercentFromEvent = (e) => {
  if (!trackRef.value) return 0
  const rect = trackRef.value.getBoundingClientRect()
  return Math.max(0, Math.min(100, ((e.clientX - rect.left) / rect.width) * 100))
}

const handleMouseDown = (e) => {
  if (props.disabled) return
  e.preventDefault()
  isDragging.value = true
  dragValue.value = getPercentFromEvent(e)

  document.addEventListener('mousemove', handleMouseMove)
  document.addEventListener('mouseup', handleMouseUp)
}

const handleMouseMove = (e) => {
  if (!isDragging.value) return
  dragValue.value = getPercentFromEvent(e)
}

const handleMouseUp = (e) => {
  if (!isDragging.value) return
  const finalValue = getPercentFromEvent(e)
  isDragging.value = false

  document.removeEventListener('mousemove', handleMouseMove)
  document.removeEventListener('mouseup', handleMouseUp)

  emit('change', finalValue)
  emit('update:value', finalValue)
}

// Cleanup listeners on unmount
onUnmounted(() => {
  document.removeEventListener('mousemove', handleMouseMove)
  document.removeEventListener('mouseup', handleMouseUp)
})
</script>

<template>
  <div
    class="slider-track"
    ref="trackRef"
    @mousedown="handleMouseDown"
    :class="{ disabled, dragging: isDragging }"
  >
    <div class="slider-fill" :style="{ width: displayValue + '%' }">
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

.slider-track:hover .slider-fill,
.slider-track.dragging .slider-fill {
  background: var(--blurple);
}

.slider-track:hover .slider-handle,
.slider-track.dragging .slider-handle {
  opacity: 1;
}

.slider-fill {
  height: 100%;
  background: var(--header-primary);
  border-radius: 2px;
  position: relative;
  transition: background 0.2s ease;
}

.slider-track.dragging .slider-fill {
  transition: none;
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
