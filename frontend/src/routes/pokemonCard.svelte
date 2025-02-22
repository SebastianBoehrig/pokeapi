<script lang="ts">
	let {
		name = null,
		weight = null,
		height = null,
		types = null,
		img = null
	} = $props();
</script>

<p>{name}</p>
<p>{weight}</p>
<p>{height}</p>
<p>{types}</p>
<img src={img} alt={name} />

<style>
	p {
		background-color: lime;
		width: fit-content;
	}
</style>
