<script lang="ts">
	let { onclick, searchMode } = $props<{
		onclick: (event: MouseEvent) => void;
		searchMode: 'single' | 'species' | 'type';
	}>();
</script>

<button {onclick}>
	Toggle me, currently: {searchMode}
</button>
