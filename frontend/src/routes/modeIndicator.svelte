<script lang="ts">
	let { searchMode } = $props<{
		searchMode: 'Pokemon-Search' | 'Type-search';
	}>();
</script>

<div>
	<p>
		{searchMode}
	</p>
</div>

<style>
	div {
		background-color: cyan;
		width: 12rem;
		height: 4rem;
	}
</style>
