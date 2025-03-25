<script lang="ts">
	import { PokeSelect } from '$lib/state/pokeSelect.svelte';
	import type { EvolutionTree } from '$lib/types';
	import RecursiveTreeNode from './recursiveTreeNode.svelte';
	let { evolutionTree } = $props<{
		evolutionTree: EvolutionTree;
	}>();
</script>

<div>
	<button onclick={() => PokeSelect.searchSelectPokemon(evolutionTree.pokemonPrimitive.name)}>
		<img
			src={evolutionTree.pokemonPrimitive.img}
			alt={`picture of ${evolutionTree.pokemonPrimitive.name}`}
			class="h-12 w-12"
		/>
	</button>

	{#each evolutionTree.evolvesTo as node}
		<div class="flex-column flex">
			<div class="h-12 w-12 content-center">
				<p class="text-center">🠂</p>
			</div>
			<RecursiveTreeNode evolutionTree={node} />
		</div>
	{/each}
</div>
