<script lang="ts">
	import RecursiveTreeNode from '$lib/components/modal/recursiveTreeNode.svelte';
	import TypeCardSmall from '$lib/components/modal/typeCardSmall.svelte';
	import { PokeSelect } from '$lib/state/pokeSelect.svelte';
	import type { PokemonPrimitive, TypesType } from '$lib/types';
	import { onMount } from 'svelte';
	import AlternativeTypes from './alternativeTypes.svelte';

	let { allTypes } = $props<{ allTypes: TypesType[] | null }>();

	let imgHover: boolean = $state(false);

	let scrollContainer: HTMLDivElement | null = null;
	let scrollbarHeight: number = $state(0);
	let scrollbarTop: number = $state(0);

	function updateScrollbar(): void {
		if (!scrollContainer) return;

		const { scrollHeight, scrollTop, clientHeight } = scrollContainer;

		let clientHeightWithSpace = clientHeight - 8;

		scrollbarTop = scrollTop + 4 + ((scrollTop + 4) / scrollHeight) * clientHeightWithSpace;
		scrollbarHeight = (clientHeightWithSpace * clientHeightWithSpace) / scrollHeight;
	}

	onMount(() => {
		updateScrollbar();
	});
	// TODO: convert hight and weight to proppper units in backend
	function get_types(): TypesType[] {
		if (allTypes == null || PokeSelect.data == null) return [];
		let result: TypesType[] = [];

		for (let type of PokeSelect.data.types) {
			result.push(allTypes.find((element: PokemonPrimitive) => element.name === type));
		}
		return result;
	}
</script>

<div
	role="dialog"
	aria-modal="true"
	class="max-h-4/5 scrollbar-hidden relative z-10 flex w-2/5 flex-col overflow-auto overscroll-none rounded-lg bg-lime-300 p-6 shadow-xl"
	bind:this={scrollContainer}
	onscroll={updateScrollbar}
>
	{#if PokeSelect.loading}
		<p>Searching...</p>
	{:else if PokeSelect.data}
		<!-- custom scrollbar -->
		<div
			class="absolute right-1 top-0 w-1 rounded-full bg-neutral-400"
			style="height: {scrollbarHeight}px; transform: translateY({scrollbarTop}px);"
		></div>
		<!-- main container -->
		<div class="relative flex w-1/2 flex-col items-center self-center">
			<img
				src={imgHover ? PokeSelect.data.img.shiny : PokeSelect.data.img.default}
				onmouseenter={() => (imgHover = true)}
				onmouseleave={() => (imgHover = false)}
				alt={`picture of ${PokeSelect.data.name}`}
			/>
			<div class="m-4 text-3xl capitalize">{PokeSelect.data.name}</div>
		</div>
		<hr />
		<p>
			Height: {PokeSelect.data.height} cm
			<br />
			Weight: {PokeSelect.data.weight} kg
		</p>
		<hr />
		<!-- types display -->
		<div class="flex flex-wrap pt-2">
			{#each get_types() as type}
				<TypeCardSmall {type} />
			{/each}
		</div>
		<hr />
		<!-- varietie forms -->
		<AlternativeTypes pokePrimitives={PokeSelect.data.varietieTypes} />
		<hr />
		<!-- cosmetic forms -->
		<!-- evolutions display -->
		<div class="p-2 pb-0">
			{#if PokeSelect.data.evolutionTree}
				<RecursiveTreeNode evolutionTree={PokeSelect.data.evolutionTree} />
			{:else}
				<p>No Evolutions</p>
			{/if}
		</div>
	{/if}
</div>

<style>
	hr {
		width: 100%;
	}

	.scrollbar-hidden::-webkit-scrollbar {
		display: none;
	}

	.scrollbar-hidden {
		-ms-overflow-style: none;
		scrollbar-width: none;
	}
</style>
