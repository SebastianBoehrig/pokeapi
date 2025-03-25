<script lang="ts">
	import { PokeSearch } from '$lib/state/pokeSearch.svelte';
	import type { TypesType } from '$lib/types';

	let { type } = $props<{ type: TypesType }>();

	function searchType(): void {
		PokeSearch.searchString = type.name;
		PokeSearch.searchPokemonByType();
	}
</script>

<button onclick={() => searchType()} class="p-2">
	<img src={type.img} alt={`search for ${type.name}-pokemon`} class="w-100 max-h-12" />
</button>
