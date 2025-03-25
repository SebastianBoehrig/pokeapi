<script lang="ts">
	import PokemonDetailModal from '$lib/components/modal/pokemonDetailModal.svelte';
	import PokemonModalContent from '$lib/components/modal/pokemonModalContent.svelte';
	import ModeIndicator from '$lib/components/modeIndicator.svelte';
	import PokemonPrimitiveCard from '$lib/components/pokemonPrimitiveCard.svelte';
	import SearchBar from '$lib/components/searchBar.svelte';
	import TypeCardList from '$lib/components/typeCardList.svelte';
	import { PokeSearch } from '$lib/state/pokeSearch.svelte';
	import type { TypesType } from '$lib/types';
	import { onMount } from 'svelte';

	let allTypes: TypesType[] | null = $state(null);
	onMount(() => {
		fetch('http://localhost:8181/initial/types')
			.then((response) => response.json())
			.then((obj: TypesType[]) => {
				allTypes = obj;
			})
			.catch((error) => {
				console.log(`Error during http://localhost:8181/initial/types:\n${error}`); //TODO: improve logging for potential user
			});
	});
</script>

<div class="flex-column flex">
	<div class="pt-50 px-90 grow">
		<!-- Main search and select -->
		<SearchBar />
		<div class="grid grid-cols-4">
			{#if PokeSearch.loading === true}
				<p class="text-sm">Searching...</p>
			{:else if PokeSearch.data}
				{#each PokeSearch.data as pokemonPrimitive}
					<PokemonPrimitiveCard {pokemonPrimitive} />
				{/each}
			{/if}
		</div>
	</div>
	<div class="h-screen w-0.5 bg-neutral-300 dark:bg-white/10"></div>
	<div class="w-3xs">
		<!-- Sidebar -->
		<ModeIndicator />
		<TypeCardList {allTypes} />
	</div>
</div>
<PokemonDetailModal>
	<PokemonModalContent {allTypes} />
</PokemonDetailModal>
