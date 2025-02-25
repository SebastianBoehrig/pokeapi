<script lang="ts">
	import type { PokemonDetail, TypesType } from './types';
	import TypeCard from './typeCard.svelte';
	import RecursiveTreeNode from './recursiveTreeNode.svelte';
	let { loadingStateSelect, pokemon, allTypes, changeShowModal, searchDetail, serchType } = $props<{
		loadingStateSelect: boolean;
		pokemon: PokemonDetail | null;
		allTypes: TypesType[] | null;
		changeShowModal: (b: boolean) => void;
		serchType: (type: string) => void;
		searchDetail: (pokemonName: string) => void;
	}>();
</script>

<div>
	{#if loadingStateSelect === true}
		<p>Searching...</p>
		<br />
	{:else if pokemon}
		<img src={pokemon.img.default} alt={`picture of ${pokemon.name}`} />
		{pokemon.name}
		<hr />
		<p>
			height = {pokemon.height}
			<br />
			weight = {pokemon.weight}
			<br />
			types = {pokemon.types}
		</p>
		<hr />
		{#each allTypes as type}
			<TypeCard
				onclick={() => {
					changeShowModal(false);
					serchType(type.name);
				}}
				{type}
			/>
		{/each}
		<hr />
		<p>Forms</p>
		<hr />
		{#if pokemon}
			{#if pokemon.evolutionTree}
				<RecursiveTreeNode evolutionTree={pokemon.evolutionTree} />
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
