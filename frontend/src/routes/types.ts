export type TypesType = {
	name: string;
	img: string;
};

export type PokemonPrimitive = {
	name: string;
	img: string; // only the default image
};

export type EvolutionTree = {
	pokemonPrimitive: PokemonPrimitive;
	evolvesTo: EvolutionTree[] | null;
};

export type PokemonDetail = {
	name: string;
	weight: number | null;
	height: number | null;
	types: string[];
	img: {
		default: string;
		shiny: string; // in the modal on-hover
	};
	varietieTypes: PokemonPrimitive[] | null;
	cosmeticTypes: PokemonPrimitive[] | null; // maybe an additional feature
	evolutionTree: EvolutionTree;
};
