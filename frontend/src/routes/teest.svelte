<script lang="ts">
	let value: string = 'world';
	let { func } = $props();
</script>

<button onclick={() => func(value)}>qrteh</button>
