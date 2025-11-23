<template>
  <div class="p-4 bg-gray-50">
    <h2 class="text-lg font-bold">Search Results</h2>
    <ul v-if="props.results.length > 0" class="mt-2">
      <li v-for="result in props.results" :key="result.id" class="p-2 border-b">
        <strong>{{ result.provider }}</strong> - {{ result.name }} - ${{ result.price }}
      </li>
    </ul>
    <p v-else class="mt-2">No service areas found for this location.</p>
  </div>
</template>

<script setup>
import { defineProps } from 'vue';

const props = defineProps({
  results: {
    type: Array,
    required: true,
  },
});
</script>
