<script lang="ts" setup>
import SearchBar from "../components/SearchBar.vue";

</script>

<template>
  <section class="h-screen w-screen flex flex-col justify-center items-center">
    <div class="flex flex-col gap-2">
      <label class="text-xl ml-3" for="Rechercher">Search</label>
      <SearchBar />
    </div>
  </section>
</template>

<style scoped>

</style>