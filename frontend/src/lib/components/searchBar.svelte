<script lang="ts">
	import { PokeSearch } from '$lib/state/pokeSearch.svelte';
</script>

<div class="mb-10 flex rounded-lg border border-neutral-400 p-2">
	<input
		type="search"
		bind:value={PokeSearch.searchString}
		class="mx-1 grow outline-neutral-400 focus:outline"
	/>
	<div class="w-0.5 bg-neutral-300 dark:bg-white/10"></div>
	<button onclick={() => PokeSearch.searchPokemon()} class="mx-1">search</button>
</div>
