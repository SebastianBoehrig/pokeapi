<script lang="ts">
	import PokemonPrimitiveCard from '$lib/components/pokemonPrimitiveCard.svelte';
	import { onMount } from 'svelte';
	import type { TypesType } from '$lib/types';
	import ModeIndicator from '$lib/components/modeIndicator.svelte';
	import PokemonModalContent from '$lib/components/pokemonModalContent.svelte';
	import TypeCardList from '$lib/components/typeCardList.svelte';
	import PokemonDetailModal from '$lib/components/pokemonDetailModal.svelte';
	import { PokeSearch } from '$lib/state/pokeSearch.svelte';
	import { PokeSelect } from '../lib/state/pokeSelect.svelte';

	// Types:
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
	<div class="grow">
		<!-- Main search and select -->
		<input type="search" bind:value={PokeSearch.searchString} />
		<button onclick={() => PokeSearch.searchPokemon()}>search</button>
		<div>
			{#if PokeSearch.loading === true}
				<p>Searching...</p>
			{:else if PokeSearch.data}
				{#each PokeSearch.data as pokemonPrimitive}
					<PokemonPrimitiveCard {pokemonPrimitive} />
				{/each}
			{/if}
		</div>

		<button onclick={() => (PokeSelect.showModal = true)} class="bg-red-600">show</button>
	</div>
	<div class="w-0.5 bg-neutral-300 dark:bg-white/10"></div>
	<div class="w-3xs">
		<!-- Sidebar -->
		<ModeIndicator />
		<TypeCardList {allTypes} />
	</div>
</div>
<PokemonDetailModal>
	<PokemonModalContent {allTypes} />
</PokemonDetailModal>
