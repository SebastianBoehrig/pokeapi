<script lang="ts">
	import type { Pokemon } from './types';

	interface Props extends Pokemon {}
	let pokemon: Pokemon = $props();
</script>

<p>{pokemon.name}</p>
<p>{pokemon.weight} {pokemon.height}</p>
<p>{pokemon.types}</p>
<img src={pokemon.img.default} alt={`picture of ${pokemon.name}`} />

<!-- TODO: on hover -->
<style>
	p {
		background-color: lime;
		width: fit-content;
	}

	img {
		max-width: 100rem;
		max-height: 100rem;
	}
</style>
