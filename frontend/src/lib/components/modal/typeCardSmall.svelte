<script lang="ts">
	import { PokeSearch } from '$lib/state/pokeSearch.svelte';
	import { PokeSelect } from '$lib/state/pokeSelect.svelte';
	import type { TypesType } from '$lib/types';

	let { type } = $props<{ type: TypesType }>();

	function searchType(): void {
		PokeSearch.searchString = type.name;
		PokeSelect.showModal = false;
		PokeSearch.searchPokemonByType();
	}
</script>

<button onclick={() => searchType()} class="pb-2 pr-2">
	<img src={type.img} alt={`search for ${type.name}-pokemon`} class="h-6" />
</button>
