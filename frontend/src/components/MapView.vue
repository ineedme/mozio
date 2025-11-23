<template>
  <div>
    <div class="p-4 bg-gray-100">
      <input type="text" v-model="searchQuery" placeholder="Search for a location" class="p-2 border rounded">
      <button @click="searchLocation" class="p-2 ml-2 text-white bg-blue-500 rounded">Search</button>
    </div>
    <div id="map" style="height: 500px;"></div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import L from 'leaflet';
import 'leaflet/dist/leaflet.css';
import axios from 'axios';

const map = ref(null);
const serviceAreas = ref([]);
const searchQuery = ref('');
const marker = ref(null);

const emit = defineEmits(['search-results']);

const fetchServiceAreas = async () => {
  try {
    const apiUrl = import.meta.env.VITE_API_URL || 'http://127.0.0.1:8000';
    const response = await axios.get(`${apiUrl}/api/v1/serviceareas/`);
    serviceAreas.value = response.data.features;
    displayServiceAreas();
  } catch (error) {
    console.error('Error fetching service areas:', error);
  }
};

const displayServiceAreas = () => {
  if (serviceAreas.value.length > 0) {
    const geoJsonLayer = L.geoJSON(serviceAreas.value, {
      onEachFeature: (feature, layer) => {
        if (feature.properties) {
          layer.bindPopup(
            `<strong>Name:</strong> ${feature.properties.name}<br>` +
            `<strong>Price:</strong> ${feature.properties.price}`
          );
        }
      }
    }).addTo(map.value);
    if (geoJsonLayer.getBounds().isValid()) {
        map.value.fitBounds(geoJsonLayer.getBounds());
    }
  }
};

const searchLocation = async () => {
  if (!searchQuery.value) return;

  try {
    const response = await axios.get(`https://nominatim.openstreetmap.org/search?q=${searchQuery.value}&format=json&limit=1`);
    if (response.data.length > 0) {
      const { lat, lon } = response.data[0];
      const latLng = [parseFloat(lat), parseFloat(lon)];

      if (marker.value) {
        map.value.removeLayer(marker.value);
      }

      marker.value = L.marker(latLng).addTo(map.value);
      map.value.setView(latLng, 13);

      // Fetch providers from the backend
      const apiUrl = import.meta.env.VITE_API_URL || 'http://127.0.0.1:8000';
      const providersResponse = await axios.get(`${apiUrl}/api/v1/serviceareas/get_providers_in_the_area/`, {
        params: { lat, lng: lon }
      });
      emit('search-results', providersResponse.data);

    } else {
      alert('Location not found');
    }
  } catch (error) {
    console.error('Error searching for location:', error);
  }
};

onMounted(() => {
  map.value = L.map('map').setView([51.505, -0.09], 13);
  L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
    attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
  }).addTo(map.value);

  fetchServiceAreas();
});
</script>
