<script lang="ts">
	import { PokeSearch } from '$lib/state/pokeSearch.svelte';
	import { PokeSelect } from '$lib/state/pokeSelect.svelte';

	import CircleX from '@lucide/svelte/icons/circle-x';

	const positioning = 'z-10 fixed bottom-5 left-1/2 -translate-x-1/2';

	let isVisible = $state(false);

	$effect(() => {
		isVisible = PokeSearch.error != null || PokeSelect.error != null;
		const timer = setTimeout(() => {
			isVisible = false;
		}, 3000);
		return () => {
			clearTimeout(timer);
		};
	});
</script>

{#if isVisible}
	<div
		class={`${positioning} max-w-2/5 border-1 flex w-max content-center gap-2 rounded-lg border-red-700 bg-red-100 px-3 py-2`}
	>
		<CircleX class="size-6 self-center text-red-700" />
		<p class="w-max text-balance text-center">{PokeSearch.error}{PokeSelect.error}</p>
	</div>
{/if}
