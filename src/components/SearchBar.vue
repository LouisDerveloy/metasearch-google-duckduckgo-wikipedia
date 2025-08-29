<script lang="ts" setup>
import {onMounted, ref} from "vue";
import {parse_query} from "../Utils/parsing.ts";
import {rules} from "../config.ts";
import {useRoute, useRouter} from "vue-router";

const router = useRouter();
const route = useRoute();

const props = defineProps<{
  autofocus?: boolean,
}>();

let search_input = ref(route.query.hasOwnProperty("search") ? decodeURIComponent(route.query.search! as string) : "");
let error = ref("");

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
    router.push({name: "results", query: { search: encodeURIComponent(search_input.value) }, force: true, replace: false });
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


let autocompletion: Array<string> = [];
autocompletion.toString(); // Just to erase the unused error

let autocompletion_display = ref<Array<string>>([]);
let autocompletion_index = ref<number>(-1)

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

async function change() {

  let search = search_input.value.trim();
  if (search.length < 1) return;

  /*
  * Only match when searching a rule but not when we have found one and we are typing the search arg
  * !<rule> <search arg>
  * will match : !youtube
  * will not match : !youtube a
  */
  if (search[0] === "!" && search.search(" ") === -1) {
    autocompletion_display.value = [];
    autocompletion_index.value = -1;
    search = search.slice(1); // Remove the "!"

    for (let i = 0; i < rules.length; i++) {

      if (rules[i].identifier.toLowerCase().startsWith(search.toLowerCase())) {
        autocompletion_display.value.push(rules[i].identifier);
      } else {
        for (let j = 0; j < rules[i].aliases!.length; j++) {
          if (rules[i].aliases![j].toLowerCase().startsWith(search.toLowerCase())) {
            autocompletion_display.value.push(rules[i].identifier);
            break;
          }
        }
      }
    }

    if (autocompletion_display.value.length >= 1) autocompletion_index.value = 0;
  }
}

function arrow_down() {
  if (autocompletion_display.value.length <= 0) return;

  autocompletion_index.value = (autocompletion_index.value + 1) % autocompletion_display.value.length;
}

function arrow_up() {
  if (autocompletion_display.value.length <= 0) return;
  console.log(autocompletion_index.value);

  autocompletion_index.value = (autocompletion_index.value - 1) % autocompletion_display.value.length;
}

function tab() {
  if (autocompletion_index.value === -1) return;

  search_input.value = `!${autocompletion_display.value[autocompletion_index.value]}`; // replace the content by the autocompletion
  autocompletion_display.value = []
  autocompletion_index.value = -1;
}
</script>

<template>
  <div>
    <form
        class="flex flex-row border-2 border-stone-500 dark:border-stone-300 rounded-md gap-1 lg:min-w-lg xl:min-w-xl md:min-w-md min-w-70 max-w-200 relative px-3"
        @submit.prevent="search"
    >

      <!--  TODO: Augmenter taille de la hitbox peut etre avec le ::before ou ::after    -->
      <div class="grow">
        <input id="search" v-model="search_input" :autofocus="props.autofocus" autocomplete="off"
               name="search" placeholder="!youtube rick roll..." type="text"
               class="w-full focus:outline-none py-3"
               @input="change"
               @submit.prevent="search"
               @focus="change"
               @keydown.tab.prevent="tab"
               @keydown.esc.prevent="autocompletion_display = []"
               @keydown.up.prevent="arrow_up"
               @keydown.down.prevent="arrow_down"
        >
        <div v-if="autocompletion_display.length > 0"
            class="appearance-none bg-white dark:bg-stone-800 w-full top-full mt-2 absolute left-0 z-10 flex flex-col border-1 border-black dark:border-white rounded-md overflow-hidden">
          <span
              v-for="(rule, index) in autocompletion_display"
              :class="['hover:bg-stone-200', 'px-2', 'py-1', 'dark:hover:bg-stone-700', index === autocompletion_index ? 'bg-blue-500 text-stone-50' : '']"
              @click="autocompletion_index=index; tab()"
          >{{ rule }}</span>
        </div>
      </div>
      <!--  TODO: Gerer le fait que quand on fasse ctrl+entrer (@keydown.ctrl.enter="") la recherche souvre sur une autre page.    -->
      <button class="grow-0 z-30 cursor-pointer" type="submit">
        <svg
            class="stroke-stone-500 dark:stroke-stone-300 aspect-square fill-none" height="16" stroke-linecap="round"
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