<script lang="ts">
	import PokemonCard from './pokemonCard.svelte';
	import ModeToggle from './modeToggle.svelte';

	let searchMode: 'single' | 'species' = $state('species');

	function switchMode() {
		searchMode = searchMode === 'single' ? 'species' : 'single';
	}

	let searchString: string = $state('');

	let pokemon = $state({
		name: 'ditto',
		weight: '1',
		height: '1',
		types: ['1', '1'],
		img: 'https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/132.png'
	});

	function search() {
		searchMode === 'single' ? searchSingle() : searchSpecies();
	}

	function searchSingle() {
		console.log('searching for:' + searchString);
		let a = fetch(`http://127.0.0.1:8181/pokemon/${searchString}`)
			.then((response) => response.json())
			.then((obj) => {
				console.log(obj);
				pokemon = obj;
			})
			.catch((error) => console.log(error));
		console.log(a);
	}

	function searchSpecies() {
		console.log('searching for:' + searchString);
		let a = fetch(`http://127.0.0.1:8181/pokemon/${searchString}`)
			.then((response) => response.json())
			.then((obj) => {
				console.log(obj);
				pokemon = obj;
			})
			.catch((error) => console.log(error));
		console.log(a);
	}
</script>

<h1>pokeapi wrapper</h1>

<h2>sidebar</h2>
<ModeToggle onclick={switchMode} searchMode={searchMode} />

<h2>main</h2>
<div>
	<input type="search" bind:value={searchString} />
	<button onclick={() => search()}>search</button>

	<PokemonCard {...pokemon} />
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
