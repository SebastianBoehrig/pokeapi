<script lang="ts">
	let searchString: string = $state('');
	import PokemonCard from './pokemonCard.svelte';
	//let pokemonArray=[{description: 'ditto'}, {description: 'ditto2'}, {description: 'ditto3'}]
	let pokemon = $state({
		name: 'ditto',
		weight: '1',
		height: '1',
		types: ['1', '1'],
		img: 'https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/132.png'
	});

	function search() {
		console.log('searching for:' + searchString);
		let a = fetch('https://pokeapi.co/api/v2/pokemon/' + searchString)
			.then((response) => response.json())
			.then((obj) => {
                console.log(obj)
				pokemon = obj;
			})
			.catch((error) => console.log(error));
		console.log(a);
	}
</script>

<h1>pokeapi wrapper</h1>

<div>
	<input type="search" bind:value={searchString} />
	<button onclick={() => search()}>search</button>
</div>

<PokemonCard {...pokemon} />

<style>
	div {
		background-color: red;
		width: fit-content;
	}
	input {
		background-color: aquamarine;
	}
</style>
