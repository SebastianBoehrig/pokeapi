<script lang="ts">
	import type { EvolutionTree } from '$lib/types';

	let { evolutionTree } = $props<{
		evolutionTree: EvolutionTree;
	}>();
    console.log(evolutionTree)
</script>

<div>{evolutionTree.pokemonPrimitive.name}</div>
{#each evolutionTree.evolvesTo as node}
    No time for the Recursive display of the tree in svelte
	<!-- <RecursiveTreeNode evolutionTree={node} /> -->
{/each}
