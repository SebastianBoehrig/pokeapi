<script lang="ts">
	import type { PokemonPrimitive } from './types';

	let { onclick, pokemonPrimitive } = $props<{
		onclick: (event: MouseEvent) => void;
		pokemonPrimitive: PokemonPrimitive;
	}>();
</script>

<button {onclick}>
	<img src={pokemonPrimitive.img} alt={`picture of ${pokemonPrimitive.name}`} />
	<p>{pokemonPrimitive.name}</p>
</button>

<style>
	p {
		width: fit-content;
	}

	img {
		max-width: 12rem;
		max-height: 12rem;
	}
</style>
