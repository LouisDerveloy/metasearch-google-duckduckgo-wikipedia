<script setup lang="ts">
import type {SearchResult} from "../types/search.ts";

const props = withDefaults(
    defineProps<SearchResult>(),
    {ads: false},
)
</script>

<template>
  <div class="flex flex-col grow max-w-150">
    <a :href="props.url" class="text-base mb-1 text-indigo-600 dark:text-indigo-400 text-ellipsis">{{props.title}}</a>
    <div class="ml-2">
      <div class="flex justify-start align-middle gap-2 text-xs">
        <span v-if="props.ads" class="text-yellow-500 font-bold border-2 border-yellow-500 rounded-md px-1">Ads</span>
        <span class="text-stone-300 dark:text-stone-400 font-bold border-2 border-stone-300 dark:border-stone-400 rounded-md px-1">{{ props.searchEngine }}</span>
        <h3 class="overflow-hidden text-ellipsis line-clamp-1 text-wrap text-stone-500 dark:text-stone-400">{{props.url}}</h3>
      </div>
      <h2 class="text-sm/5 text-justify text-wrap text-ellipsis line-clamp-3">{{props.description}}</h2>
    </div>
  </div>
</template>

<style scoped>

</style>