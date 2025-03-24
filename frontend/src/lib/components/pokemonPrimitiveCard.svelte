<script lang="ts">
	import type { PokemonPrimitive } from '$lib/types';
	import { PokeSelect } from '$lib/state/pokeSelect.svelte';

	let { pokemonPrimitive } = $props<{ pokemonPrimitive: PokemonPrimitive }>();

	function selectSearchPokemon(): void {
		PokeSelect.searchSelectPokemon(pokemonPrimitive.name);
		PokeSelect.showModal = true;
	}
</script>

<button onclick={() => selectSearchPokemon()}>
	<img src={pokemonPrimitive.img} alt={`picture of ${pokemonPrimitive.name}`} />
	<p>{pokemonPrimitive.name}</p>
</button>

<style>
	p {
		width: fit-content;
	}

	img {
		width: 12rem;
		height: 12rem;
	}
</style>
