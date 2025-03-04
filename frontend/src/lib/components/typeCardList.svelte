<script lang="ts">
	import type { TypesType } from '$lib/types';
	import TypeCard from '$lib/components/typeCard.svelte';
	let { allTypes } = $props<{ allTypes: TypesType[] | null }>();
</script>

<div class="no-wrap flex flex-col">
	{#if allTypes}
		{#each allTypes as type}
			<TypeCard {type} />
		{/each}
	{:else}
		<p>Loading...</p>
	{/if}
</div>
