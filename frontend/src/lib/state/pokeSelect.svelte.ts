import type { PokemonDetail } from '$lib/types';

class PokemonSelect {
	data: PokemonDetail | null = $state(null);
	showModal: boolean = $state(false);
	loading: boolean = $state(false);
	error: string | null = $state(null);

	searchSelectPokemon(pokeName: string) {
		this.loading = true;
		console.log(`searchSelecting for: ${pokeName}`);
		fetch(`http://localhost:8181/pokemon/detail/${pokeName}`)
			.then((response: Response) => response.json())
			.then((obj: PokemonDetail) => {
				this.data = obj;
				this.loading = false;
			})
			.catch((error) => {
				console.log(`Error during /pokemon/detail/${pokeName}:\n${error}`);
				this.error = error.message;
				this.loading = false;
			});
	}
}

export const PokeSelect = new PokemonSelect();
