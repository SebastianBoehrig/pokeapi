<script lang="ts">
	import { PokeSelect } from '$lib/state/pokeSelect.svelte';
	let { children } = $props<{ children: any }>();
</script>

{#if PokeSelect.showModal}
	<div class="fixed inset-0 flex items-center justify-center">
		<!-- Button for closing the modal -->
		<button
			class="backdrop-blur-xs absolute inset-0 bg-black/60 transition-opacity duration-300"
			onclick={() => (PokeSelect.showModal = false)}
			aria-label="Close modal"
		></button>
		<!-- Modal content container -->
		<div role="dialog" aria-modal="true" class="relative z-10 rounded-lg bg-white p-6 shadow-xl">
			{@render children?.()}
		</div>
	</div>
{/if}
