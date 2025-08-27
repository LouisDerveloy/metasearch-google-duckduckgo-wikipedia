<script setup lang="ts">

const props = withDefaults(
    defineProps<{
      title: string,
      url: string,
      description: string,
      ads?: boolean,
    }>(),
    {ads: false},
)
</script>

<template>
  <div class="flex flex-col grow max-w-150">
    <a :href="url" class="text-base mb-1 text-indigo-600 dark:text-indigo-400 text-ellipsis">{{title}}</a>
    <div class="ml-2">
      <div class="flex justify-start align-middle gap-2 text-xs">
        <span v-if="ads" class="text-yellow-500 font-bold border-2 border-yellow-500 rounded-md px-1">Ads</span>
        <h3 class="overflow-hidden text-clip text-stone-500 dark:text-stone-400">{{url}}</h3>
      </div>
      <h2 class="text-sm/5 text-justify line-clamp-3">{{description}}</h2>
    </div>
  </div>
</template>

<style scoped>

</style>