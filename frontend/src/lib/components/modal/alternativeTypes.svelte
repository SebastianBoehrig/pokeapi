<script lang="ts">
	import { PokeSelect } from '$lib/state/pokeSelect.svelte';
	import type { PokemonPrimitive } from '$lib/types';

	let { pokePrimitives } = $props<{ pokePrimitives: PokemonPrimitive[] | null }>();
</script>

<div class="flex flex-wrap pt-2">
	{#if pokePrimitives}
		{#each pokePrimitives as type}
			<button onclick={() => PokeSelect.searchSelectPokemon(type.name)} class="pb-2 pr-2">
				<img src={type.img} alt={`picture of ${type.name}`} class="h-12 w-12" />
			</button>
		{/each}
	{:else}
		<p>No alternate Forms</p>
	{/if}
</div>
