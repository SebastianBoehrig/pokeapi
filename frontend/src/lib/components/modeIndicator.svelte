<script lang="ts">
	import { PokeSearch } from '$lib/state/pokeSearch.svelte';
</script>

<div class="flex m-2 h-20 items-center justify-center bg-neutral-400 rounded-md">
	<p class="text-white">
		{PokeSearch.mode}
	</p>
</div>

<style>
</style>
