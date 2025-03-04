import type { PokemonPrimitive } from '$lib/types';

class PokemonSearch {
	data: PokemonPrimitive[] | null = $state(null);
	mode: 'Pokemon-Search' | 'Type-search' = $state('Pokemon-Search');
	searchString: string = $state('');
	loading: boolean = $state(false);
	error: string | null = $state(null);

	searchPokemon() {
		this.loading = true;
		this.mode = 'Pokemon-Search';
		console.log(`searching for pokemon: ${this.searchString}`);
		fetch(`http://localhost:8181/pokemon/primitives/${this.searchString}`) //TODO: replace with Proxy in svelte, url from env/yml
			.then((response: Response) => response.json())
			.then((obj: PokemonPrimitive) => {
				this.data = [obj];
				this.loading = false;
			})
			.catch((error) => {
				console.log(`Error during /pokemon/primitives/${this.searchString}:\n${error}`); //Handle 404s/500s//TODO: show some kind of error popup
				this.error = error.message;
				this.loading = false;
			});
	}

	searchPokemonByType() {
		this.loading = true;
		this.mode = 'Type-search';
		console.log(`searching for type: ${this.searchString}`);
		fetch(`http://localhost:8181/pokemon/type/${this.searchString}`)
			.then((response: Response) => response.json())
			.then((obj: PokemonPrimitive[]) => {
				this.data = obj;
				this.loading = false;
			})
			.catch((error) => {
				console.log(`Error during /pokemon/type/${this.searchString}:\n${error}`);
				this.error = error.message;
				this.loading = false;
			});
	}
}

export const PokeSearch = new PokemonSearch(); //TODO: make default export + getter singkleton pattern
