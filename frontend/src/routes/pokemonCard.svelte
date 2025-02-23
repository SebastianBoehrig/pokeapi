<script lang="ts">
	let { name = null, weight = null, height = null, types = null, img = null } = $props();
</script>

<p>{name}</p>
<p>{weight} {height}</p>
<p>{types}</p>
<img src={img.default} alt={`picture of ${name}`} />
<!-- TODO: on hover -->
<style>
	p {
		background-color: lime;
		width: fit-content;
	}

	img {
		max-width: 100rem;
		max-height: 100rem;
	}
</style>
