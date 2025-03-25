<script lang="ts">
	import { PokeSelect } from '$lib/state/pokeSelect.svelte';
	import type { PokemonPrimitive } from '$lib/types';

	let { pokemonPrimitive } = $props<{ pokemonPrimitive: PokemonPrimitive }>();

	function selectSearchPokemon(): void {
		PokeSelect.searchSelectPokemon(pokemonPrimitive.name);
		PokeSelect.showModal = true;
	}
</script>

<button onclick={() => selectSearchPokemon()} class="flex flex-col items-center">
	<img src={pokemonPrimitive.img} alt={`picture of ${pokemonPrimitive.name}`} class="max-h-48" />
	<p class="m-2 w-fit text-sm">{pokemonPrimitive.name}</p>
</button>
