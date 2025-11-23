<script setup>
import { ref } from 'vue';
import MapView from './components/MapView.vue';
import SearchResults from './components/SearchResults.vue';

const searchResults = ref([]);

function handleSearchResults(results) {
  searchResults.value = results;
}
</script>

<template>
  <div>
    <MapView @search-results="handleSearchResults" />
    <SearchResults :results="searchResults" />
  </div>
</template>
