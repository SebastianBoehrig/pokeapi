<script lang="ts">
	import PokemonPrimitiveCard from './pokemonPrimitiveCard.svelte';
	import PokemonDetailModal from './pokemonDetailModal.svelte';
	import TypeCard from './typeCard.svelte';
	import { onMount } from 'svelte';
	import type { PokemonDetail, PokemonPrimitive, TypesType } from './types';
	import ModeIndicator from './modeIndicator.svelte';
	import PokemonModalContent from './pokemonModalContent.svelte';

	// Toggle Mode:
	let searchMode: 'Pokemon-Search' | 'Type-search' = $state('Pokemon-Search');
	let showModal: boolean = $state(false);
	function changeShowModal(b: boolean) {
		console.log(`setting showmodal to ${b}`);
		showModal = b;
	}

	// Types:
	let allTypes: TypesType[] | null = $state(null);

	onMount(() => {
		fetch('http://localhost:8181/initial/types')
			.then((response) => response.json())
			.then((obj: TypesType[]) => {
				allTypes = obj;
			})
			.catch((error) => {
				console.log(`Error during http://localhost:8181/initial/types:`); //TODO: improve logging for potential user
				console.log(error);
			});
	});

	// PokeArray:
	let pokemonPrimitiveArray: PokemonPrimitive[] | null = $state(null);
	let pokemon: PokemonDetail | null = $state(null);

	// Search:
	let searchString: string = $state('');
	let loadingStateSearch: boolean = $state(false);
	let loadingStateSelect: boolean = $state(false);

	function searchPokemon() {
		loadingStateSearch = true;
		searchMode = 'Pokemon-Search';
		console.log(`searching for: ${searchString}`);
		fetch(`http://localhost:8181/pokemon/primitives/${searchString}`) //TODO: replace with Proxy in svelte, url from env/yml
			.then((response: Response) => response.json())
			.then((obj: PokemonPrimitive) => {
				pokemonPrimitiveArray = [obj];
				loadingStateSearch = false;
			})
			.catch((error) => {
				console.log(`Error during /pokemon/primitives/${searchString}:\n${error}`); //Handle 404s/500s//TODO: show some kind of error popup
				loadingStateSearch = false;
			});
	}

	function searchPokemonByType(typeName: string) {
		loadingStateSearch = true;
		searchMode = 'Type-search';
		searchString = typeName;
		console.log(`searching for: ${typeName}`);
		fetch(`http://localhost:8181/pokemon/type/${typeName}`)
			.then((response: Response) => response.json())
			.then((obj: PokemonPrimitive[]) => {
				pokemonPrimitiveArray = obj;
				loadingStateSearch = false;
			})
			.catch((error) => {
				console.log(`Error during /pokemon/type/${typeName}:\n${error}`);
				loadingStateSearch = false;
			});
	}

	function searchSelectPokemon(pokemonName: string) {
		loadingStateSelect = true;
		console.log(`searchSelecting for: ${pokemonName}`);
		fetch(`http://localhost:8181/pokemon/detail/${pokemonName}`)
			.then((response: Response) => response.json())
			.then((obj: PokemonDetail) => {
				pokemon = obj;
				loadingStateSelect = false;
			})
			.catch((error) => {
				console.log(`Error during /pokemon/detail/${pokemonName}:\n${error}`);
				loadingStateSelect = false;
			});
	}
</script>

<h1>pokeapi wrapper</h1>

<h2>sidebar</h2>
<ModeIndicator {searchMode} />

{#if allTypes}
	{#each allTypes as type}
		<TypeCard onclick={() => searchPokemonByType(type.name)} {type} />
	{/each}
{:else}
	<p>Loading...</p>
{/if}

<h2>main</h2>

<input type="search" bind:value={searchString} />
<button onclick={() => searchPokemon()}>search</button>

<div>
	{#if loadingStateSearch === true}
		<p>Searching...</p>
		<br />
	{:else if pokemonPrimitiveArray}
		{#each pokemonPrimitiveArray as pokemonPrimitive}
			<PokemonPrimitiveCard
				onclick={() => {
					searchSelectPokemon(pokemonPrimitive.name);
					showModal = true;
				}}
				{pokemonPrimitive}
			/>
		{/each}
	{/if}
</div>

<PokemonDetailModal {showModal} {changeShowModal}>
	<PokemonModalContent
		{loadingStateSelect}
		{pokemon}
		{allTypes}
		{changeShowModal}
		serchType={(type: string) => searchPokemonByType(type)}
		searchDetail={(pokemonName: string) => searchSelectPokemon(pokemonName)}
	/>
</PokemonDetailModal>

<style>
	div {
		background-color: red;
		width: fit-content;
	}
</style>
