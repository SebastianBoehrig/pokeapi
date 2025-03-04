<script lang="ts">
	import type { TypesType } from '$lib/types';
	import { PokeSelect } from '$lib/state/pokeSelect.svelte';
	import TypeCard from '$lib/components/typeCard.svelte';
	import RecursiveTreeNode from '$lib/components/recursiveTreeNode.svelte';
	let { allTypes } = $props<{ allTypes: TypesType[] | null }>();

	function get_types() {
		if (allTypes == null || PokeSelect.data == null) return [];
		let result: TypesType[] = [];
		for (let type of PokeSelect.data.types) {
			for (let at of allTypes) {
				if (at.name == type) {
					result.push(at);
					break;
				}
			}
		}
		return result;
	}
</script>

<div>
	{#if PokeSelect.loading}
		<p>Searching...</p>
	{:else if PokeSelect.data}
		<img src={PokeSelect.data.img.default} alt={`picture of ${PokeSelect.data.name}`} />
		{PokeSelect.data.name}
		<hr />
		<p>
			height = {PokeSelect.data.height}
			<br />
			weight = {PokeSelect.data.weight}
		</p>
		<hr />
		{#each get_types() as type}
			<!-- <TypeCard TODO: make smaller typpecard
				onclick={() => {
					changeShowModal(false);
					serchType(type.name);
				}}
				{type}
			/> -->
		{/each}
		<hr />
		<p>Forms</p>
		<hr />
		{#if PokeSelect.data}
			{#if PokeSelect.data.evolutionTree}
				<p>
					{JSON.stringify(PokeSelect.data.evolutionTree)}
				</p>
				<!-- <RecursiveTreeNode evolutionTree={pokemon.evolutionTree} /> -->
			{:else}
				<p>No Evolutions</p>
			{/if}
		{/if}
	{/if}
</div>

<style>
	div {
		background-color: rgb(175, 214, 130);
		width: 50rem;
	}
</style>
