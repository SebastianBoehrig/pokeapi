<script lang="ts">
	let { showModal, changeShowModal, children } = $props<{
		showModal: boolean;
		changeShowModal: (b: boolean) => void;
		children: any;
	}>();

	let dialog: any = $state(); //TODO: figure types out

	$effect(() => {
		if (showModal) dialog.showModal();
		if (showModal == false) dialog.close();
	});
</script>

<dialog
	bind:this={dialog}
	onclose={changeShowModal(false)}
	onclick={(e) => {
		if (e.target === dialog) changeShowModal(false);
	}}
>
	<div>
		{@render children?.()}
		<button autofocus onclick={() => changeShowModal(false)}>close modal</button>
	</div>
</dialog>

<style>
	dialog {
		/* max-width: 32em; */
		width: 50rem;
		border-radius: 0.2em;
		border: none;
		padding: 0;
	}
	dialog::backdrop {
		background: rgba(0, 0, 0, 0.3);
	}
	dialog > div {
		padding: 1em;
	}
	dialog[open] {
		animation: zoom 0.3s cubic-bezier(0.34, 1.56, 0.64, 1);
	}
	@keyframes zoom {
		from {
			transform: scale(0.95);
		}
		to {
			transform: scale(1);
		}
	}
	dialog[open]::backdrop {
		animation: fade 0.2s ease-out;
	}
	@keyframes fade {
		from {
			opacity: 0;
		}
		to {
			opacity: 1;
		}
	}
	button {
		display: block;
	}
</style>
