<script lang="ts">
	let { onclick, searchMode } = $props<{
		onclick: (event: MouseEvent) => void;
		searchMode: 'single' | 'species' | 'type';
	}>();
</script>

<button {onclick} class="my-button">
	Toggle me, currently: {searchMode}
</button>
