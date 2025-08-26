<script lang="ts" setup>
import {onMounted, ref} from "vue";
import {parse_query} from "../Utils/parsing.ts";
import {rules} from "../config.ts";

const props = defineProps<{
  autofocus?: boolean,
}>();

let search_input = ref("");
let error = ref("")
let autocompletion: Array<string> = [];
let autocompletion_display = ref<Array<string>>([]);

function search() {
  error.value = "";
  if (search_input.value.trim().slice(undefined, 1) === "!") {
    let {identifier, arg} = parse_query(search_input.value);
    let ruleIndex = rule_index(identifier);
    if (ruleIndex === -1) {
      error.value = "Aucune règle ne correspond a votre requette.";
      return;
    }

    document.location = buildUrl(ruleIndex, arg);
  } else {
    console.log(search_input.value);
    console.dir(rules);
  }
}

function rule_index(identifier: string): number {
  for (let i = 0; i < rules.length; i++) {
    if (rules[i].identifier.toLowerCase() === identifier.toLowerCase()) return i;
    if (rules[i].aliases?.includes(identifier.toLowerCase())) return i;
  }

  return -1
}

function buildUrl(ruleIndex: number, arg?: string) {
  if (typeof rules[ruleIndex].urlWithNoArg !== 'undefined' && arg === undefined) {
    return rules[ruleIndex].urlWithNoArg;
  } else {
    let url = rules[ruleIndex].url;
    url = url.replace("{}" as string, arg ?? "");
    return url;
  }
}

// TODO: Faire la recherche en fonction des argument avec le moteur de recherche Google, Duckduckgo, wikipedia...

onMounted(() => {
  autocompletion = get_autocompletion_list();
})

function get_autocompletion_list(): Array<string> {
  let result: Array<string> = []
  for (let i = 0; i < rules.length; i++) {
    result.push(rules[i].identifier);
    if (typeof rules[i].aliases !== "undefined") rules[i].aliases!.map(value => result.push(value));
  }

  return result
}
</script>

<template>
  <div>
    <form
        class="flex flex-row border-2 border-stone-500 dark:border-stone-500 p-3 rounded-md gap-1 lg:min-w-lg xl:min-w-xl md:min-w-md min-w-70 max-w-200"
        @submit.prevent="search">

<!--  TODO: Augmenter taille de la hitbox peut etre avec le ::before ou ::after    -->
      <div class="grow">
        <input id="search" v-model="search_input" :autofocus="props.autofocus" autocomplete="off"
               class="w-full focus:outline-none" name="search" placeholder="!youtube rick roll..." type="text">

      </div>
<!--  TODO: Gerer le fait que quand on fasse ctrl+entrer (@keydown.ctrl.enter="") la recherche souvre sur une autre page.    -->
      <button class="grow-0" type="submit">
        <svg
            class="stroke-stone-500 aspect-square fill-none" height="16" stroke-linecap="round"
            stroke-linejoin="round" stroke-width="3" viewBox="0 0 24 24"
            width="16"
            xmlns="http://www.w3.org/2000/svg"
        >
          <circle cx="11" cy="11" r="8"></circle>
          <line x1="21" x2="16.65" y1="21" y2="16.65"></line>
        </svg>
      </button>
    </form>
    <span v-if="error !== ''" class="text-xs text-red-700 font-bold">{{ error }}</span>
  </div>
</template>

<style scoped>

</style>