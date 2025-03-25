<script lang="ts">
	import { PokeSelect } from '$lib/state/pokeSelect.svelte';
	import type { PokemonPrimitive } from '$lib/types';

	let { pokemonPrimitive } = $props<{ pokemonPrimitive: PokemonPrimitive }>();

	function selectSearchPokemon(): void {
		PokeSelect.searchSelectPokemon(pokemonPrimitive.name);
		PokeSelect.showModal = true;
	}
</script>

<button onclick={() => selectSearchPokemon()}>
	<img src={pokemonPrimitive.img} alt={`picture of ${pokemonPrimitive.name}`} class="w-48 h-48"/>
	<p class="w-fit">{pokemonPrimitive.name}</p>
</button>
