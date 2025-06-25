import type { RequestHandler } from './$types';
import { json } from '@sveltejs/kit';
import type { PokemonDetail } from '$lib/types';

export const GET: RequestHandler = async ({ params }) => {
	const { name } = params;

	const response: Response = await fetch(`http://backend:8181/pokemon/detail/${name}`);
	if (!response.ok) {
		throw new Error(`Could not get Pokemon Information! Status: ${response.status}`);
	}

	const allTypes = (await response.json()) as PokemonDetail;
	return json(allTypes);
};
