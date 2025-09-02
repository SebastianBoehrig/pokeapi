<script lang="ts">
	import ErrorToast from '$lib/components/errorToast.svelte';
	import PokemonDetailModal from '$lib/components/modal/pokemonDetailModal.svelte';
	import PokemonModalContent from '$lib/components/modal/pokemonModalContent.svelte';
	import ModeIndicator from '$lib/components/modeIndicator.svelte';
	import PokemonPrimitiveCard from '$lib/components/pokemonPrimitiveCard.svelte';
	import SearchBar from '$lib/components/searchBar.svelte';
	import TypeCardList from '$lib/components/typeCardList.svelte';
	import { PokeSearch } from '$lib/state/pokeSearch.svelte';
	import type { TypesType } from '$lib/types';

	let { data } = $props<{ allTypes: TypesType[] }>();
	let { allTypes } = $state<{ allTypes: TypesType[] }>(data);
</script>

<div class="flex">
	<div class="pt-50 px-90 max-w-[calc(87.5%-0.25rem)] grow">
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
	<div class="h-auto w-0.5 bg-neutral-300 dark:bg-white/10"></div>
	<div class="w-1/8">
		<!-- Sidebar -->
		<ModeIndicator />
		<TypeCardList {allTypes} />
	</div>
</div>
<PokemonDetailModal>
	<PokemonModalContent {allTypes} />
</PokemonDetailModal>
<ErrorToast />
