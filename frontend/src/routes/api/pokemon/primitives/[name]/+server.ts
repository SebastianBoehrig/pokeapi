import type { RequestHandler } from './$types';
import { json } from '@sveltejs/kit';
import type { PokemonPrimitive } from '$lib/types';

export const GET: RequestHandler = async ({ params }) => {
	const { name } = params;

	const response: Response = await fetch(`http://backend:8181/pokemon/primitives/${name}`);
	if (!response.ok) {
		throw new Error(`Could not find Pokemon! Status: ${response.status}`);
	}

	const data = (await response.json()) as PokemonPrimitive;
	return json(data);
};
