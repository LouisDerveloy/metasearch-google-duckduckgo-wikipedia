<script setup lang="ts">
import SearchBar from "../components/SearchBar.vue";
import WebsiteResult from "../components/WebsiteResult.vue";
import DarkModeButton from "../components/DarkModeButton.vue";
import {useRoute} from "vue-router";
import {onMounted, ref, watch} from "vue";
import type {EngineResponse, SearchResponse, SearchResult} from "../types/search.ts";

const route = useRoute();

const searching = ref(false);
const results = ref<Array<{
  title: string;
  description: string;
  url: string;
  ads: boolean;
  searchEngine: string;
}>>([]);

watch(route, search, { immediate: true });

async function search() {
  if (!route.query.hasOwnProperty("search")) return console.error("No search querry");

  const response = await fetch('http://localhost:8001/api/search', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json'
    },
    body: JSON.stringify({
      query: route.query.search!,
      engines: ['google', 'duckduckgo', 'wikipedia'],
      max_results: 20
    })
  })

  if (!response.ok) {
    throw new Error(`HTTP ${response.status}: ${response.statusText}`);
  }

  const data = (await response.json()) as SearchResponse;

  results.value = fuzeResult(data.engines_responses);

  function fuzeResult(responses: Array<EngineResponse>) {
    const validResults = responses
        .filter(resp => resp.success)
        .map(resp => resp.results);

    const maxLen = Math.max(...validResults.map(arr => arr.length));

    return Array.from({ length: maxLen }, (_, i) =>
        validResults.map(arr => arr[i]).filter(Boolean)
    ).flat();
  }
}

</script>

<template>
<section class="flex flex-col gap-4 w-full h-full px-2 py-4">
  <section class="flex w-full justify-between align-middle px-2">
    <SearchBar />
    <DarkModeButton />
  </section>
  <section v-if="!searching" class="flex justify-around flex-wrap gap-x-4 gap-y-2 px-4 overflow-x-hidden">
    <WebsiteResult v-for="result in results" :title="result.title" :url="result.url" :description="result.description" :ads="result.ads" :search-engine="result.searchEngine"/>
  </section>
  <section v-else>
    En train de chercher...
  </section>
</section>
</template>

<style scoped>

</style>