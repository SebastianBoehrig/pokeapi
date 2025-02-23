<script lang="ts">
	import PokemonCard from './pokemonCard.svelte';
	import TypeCard from './typeCard.svelte';
	import ModeToggle from './modeToggle.svelte';
	import { Queue } from 'mnemonist';
	import { writable, derived } from 'svelte/store';
	import { onMount } from 'svelte';
	import type { Pokemon, TypesType } from './types';

	// Toggle Mode:
	let searchMode: 'single' | 'species' | 'type' = $state('species');

	function switchMode() {
		searchMode = searchMode === 'species' ? 'single' : 'species';
	}

	// Types:
	let allTypes: TypesType[] | null = $state(null);

	onMount(() => {
		fetch('http://localhost:8181/initial/types')
			.then((response) => response.json())
			.then((obj: TypesType[]) => {
				console.log('Types:');
				console.log(obj);
				allTypes = obj;
			})
			.catch((error) => {
				console.log(`Error during http://localhost:8181/initial/types:`); //TODO: improve logging for potentila user
				console.log(error);
			});
	});

	// PokeQueue:

	const PokeQueue = writable(new Queue<Pokemon>());
	const pokemonQueueArray = derived(PokeQueue, ($queue) => $queue.toArray());

	function addPokemon(pokemon: Pokemon) {
		PokeQueue.update((queue) => {
			//TODO: deduplicate and possibly CircularBuffer
			if (queue.size > 3) {
				//TODO: 16
				queue.dequeue();
			}
			queue.enqueue(pokemon);
			console.log(queue.toArray());
			return queue;
		});
	}

	// Search:
	let searchString: string = $state('');

	function search() {
		if (searchMode === 'species') {
			searchSpecies();
		} else if (searchMode === 'single') {
			searchSingle();
		}
	}

	function searchSingle() {
		console.log('searching for:' + searchString);
		fetch(`http://localhost:8181/pokemon/${searchString}`) //TODO: replace with Proxy in svelte, url from env/yml
			.then((response) => response.json())
			.then((obj: Pokemon) => {
				addPokemon(obj);
			})
			.catch((error) => {
				console.log(`Error during http://localhost:8181/pokemon/${searchString}:`);
				console.log(error);
			});
	}

	function searchSpecies() {
		console.log('searching for:' + searchString);
		fetch(`http://localhost:8181/pokemon/species/${searchString}`) //TODO: replace with Proxy in svelte, url from env/yml
			.then((response) => response.json())
			.then((obj: Pokemon[]) => {
				obj.forEach((pokemon: Pokemon) => {
					addPokemon(pokemon);
				});
			})
			.catch((error) => {
				console.log(`Error during http://localhost:8181/pokemon/${searchString}:`);
				console.log(error);
			});
	}

	function searchType() {
		console.log('searching for:' + searchString);
		fetch(`http://localhost:8181/pokemon/species/${searchString}`) //TODO: replace with Proxy in svelte, url from env/yml
			.then((response) => response.json())
			.then((obj: Pokemon[]) => {
				obj.forEach((pokemon: Pokemon) => {
					addPokemon(pokemon);
				});
			})
			.catch((error) => {
				console.log(`Error during http://localhost:8181/pokemon/${searchString}:`);
				console.log(error);
			});
	}
</script>

<h1>pokeapi wrapper</h1>

<h2>sidebar</h2>
<ModeToggle onclick={switchMode} {searchMode} />

{#if allTypes}
	{#each allTypes as type}
		<TypeCard onclick={() => searchType()} {type} />
		<br />
	{/each}
{:else}
	<p>Loading...</p>
{/if}

<h2>main</h2>
<div>
	<input type="search" bind:value={searchString} />
	<button onclick={() => search()}>search</button>

	{#each $pokemonQueueArray as pokeQueueEntry}
		<PokemonCard {...pokeQueueEntry} />
		<br />
	{/each}
</div>

<style>
	div {
		background-color: red;
		width: fit-content;
	}
	input {
		background-color: aquamarine;
	}
</style>
