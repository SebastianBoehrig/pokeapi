<script lang="ts">
	import type { TypesType } from './types';
	let { onclick, type } = $props<{
		onclick: (event: MouseEvent) => void;
		type: TypesType;
	}>();
</script>

<button {onclick}>
	<img src={type.img} alt={`picture of ${type.name}`} />
</button>

<style>
	button {
		max-width: 20rem;
		max-height: 10rem;
	}
</style>
