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

	onMount(async () => await getTypes());

	async function getTypes(): Promise<void> {
		try {
			const response = await fetch('http://localhost:8181/initial/types');

			if (!response.ok) {
				throw new Error(`Could not get Types! Status: ${response.status}`);
			}

			allTypes = await response.json();
		} catch (error: unknown) {
			console.error(`Error during http://localhost:8181/initial/types:\n${error}`);
		}
	}
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

		<button onclick={() => console.log(PokeSearch.error)} class="bg-orange-300">a</button>
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
