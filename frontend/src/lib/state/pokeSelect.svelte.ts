import getErrorMessage from '$lib/error_handeling';
import type { PokemonDetail } from '$lib/types';

class PokemonSelect {
	data: PokemonDetail | null = $state(null);
	showModal: boolean = $state(false);
	loading: boolean = $state(false);
	error: string | null = $state(null);

	async searchSelectPokemon(pokeName: string) {
		try {
			this.loading = true;

			console.log(`searchSelecting for: ${pokeName}`);
			const response: Response = await fetch(`/api/pokemon/detail/${pokeName}`);

			this.data = await response.json();
		} catch (error: unknown) {
			console.error(`Error during /pokemon/detail/${pokeName}:\n${error}`);
			this.error = getErrorMessage(error);
		} finally {
			this.loading = false;
		}
	}
}

export const PokeSelect = new PokemonSelect();
