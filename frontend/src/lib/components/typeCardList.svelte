<script lang="ts">
	import TypeCard from '$lib/components/typeCard.svelte';
	import type { TypesType } from '$lib/types';
	let { allTypes } = $props<{ allTypes: TypesType[] | null }>();
</script>

<div class="no-wrap flex flex-col items-center">
	{#if allTypes}
		{#each allTypes as type}
			<TypeCard {type} />
		{/each}
	{:else}
		<p>Loading...</p>
	{/if}
</div>
