import getErrorMessage from '$lib/error_handeling';
import type { PokemonPrimitive } from '$lib/types';

class PokemonSearch {
	data: PokemonPrimitive[] | null = $state(null);
	mode: 'Pokemon-Search' | 'Type-search' = $state('Pokemon-Search');
	searchString: string = $state('');
	loading: boolean = $state(false);
	error: string | null = $state(null);

	async searchPokemon() {
		try {
			this.loading = true;
			this.mode = 'Pokemon-Search';

			console.log(`searching for pokemon: ${this.searchString}`);
			const response: Response = await fetch(`/api/pokemon/primitives/${this.searchString}`);

			this.data = [await response.json()];
		} catch (error: unknown) {
			console.error(`Error during /pokemon/primitives/${this.searchString}:\n${error}`);
			this.error = getErrorMessage(error);
		} finally {
			this.loading = false;
		}
	}

	async searchPokemonByType() {
		try {
			this.loading = true;
			this.mode = 'Type-search';
			console.log(`searching for type: ${this.searchString}`);

			const response = await fetch(`api/pokemon/type/${this.searchString}`);

			this.data = await response.json();
		} catch (error: unknown) {
			console.error(`Error during /pokemon/type/${this.searchString}:\n${error}`);
			this.error = getErrorMessage(error);
		} finally {
			this.loading = false;
		}
	}
}

export const PokeSearch = new PokemonSearch();
