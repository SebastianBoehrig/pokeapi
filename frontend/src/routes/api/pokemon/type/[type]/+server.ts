import type { RequestHandler } from './$types';
import { json } from '@sveltejs/kit';
import type { PokemonPrimitive, FastAPIException } from '$lib/types';
import { sanitizeFastAPIException } from '$lib/error_handeling';

export const GET: RequestHandler = async ({ params }): Promise<Response> => {
    const { type } = params;

    const response: Response = await fetch(`http://backend:8181/pokemon/type/${type}`);
    if (!response.ok) {
        const data = (await response.json()) as FastAPIException;
        const sanitizedData = sanitizeFastAPIException(data);
        return json(sanitizedData);
    }

    const data = (await response.json()) as PokemonPrimitive[];
    return json(data);
};
