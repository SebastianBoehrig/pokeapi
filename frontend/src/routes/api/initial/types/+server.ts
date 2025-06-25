import type { RequestHandler } from './$types';
import { json } from '@sveltejs/kit';
import type { TypesType } from '$lib/types';

export const GET: RequestHandler = async () => {
	const response: Response = await fetch('http://backend:8181/initial/types');
	if (!response.ok) {
		throw new Error(`Could not get Types! Status: ${response.status}`);
	}
	const allTypes = (await response.json()) as TypesType[];
	return json(allTypes);
};
