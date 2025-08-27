<script lang="ts" setup>
import SearchBar from "../components/SearchBar.vue";
import DarkModeButton from "../components/DarkModeButton.vue";

</script>

<template>
  <DarkModeButton class="self-end m-3 absolute" />
  <section class="h-screen w-screen flex flex-col justify-center items-center">
    <div class="flex flex-col gap-2">
      <label class="text-xl ml-3" for="Rechercher">Search</label>
      <SearchBar autofocus />
    </div>
  </section>
</template>

<style scoped>

</style>