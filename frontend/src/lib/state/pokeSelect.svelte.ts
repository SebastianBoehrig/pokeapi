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

			const response = await fetch(`http://localhost:8181/pokemon/detail/${pokeName}`);

			if (!response.ok) {
				throw new Error(`Could not get Pokemon Information! Status: ${response.status}`);
			}

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
