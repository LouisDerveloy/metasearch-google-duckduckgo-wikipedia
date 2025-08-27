<script setup lang="ts">

import {ref} from "vue";

const theme = ref<'light' | 'dark'| 'default'>(getTheme());

function getTheme(): "dark" | "light" | "default" {
  const theme = localStorage.getItem("theme");
  if (theme === "light") {
    return "light";
  } else if (theme === "dark") {
    return "dark";
  } else {
    return "default";
  }

}

function changeTheme() {
  if (theme.value === "default") {
    localStorage.removeItem("theme");
  } else {
    localStorage.setItem("theme", theme.value);
  }
  document.location.reload();
}
</script>
<template>
  <select @change.prevent="changeTheme" v-model="theme" class="appearance-none dark:bg-stone-800 p-2 focus:outline-none hover:bg-stone-100 dark:hover:bg-stone-700 rounded-md text-center">
    <option value="dark">Dark</option>
    <option value="light">Light</option>
    <option value="default">Par défaut</option>
  </select>
</template>

<style scoped>

</style>