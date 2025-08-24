import type { RequestHandler } from './$types';
import { json } from '@sveltejs/kit';
import type { TypesType, FastAPIException } from '$lib/types';
import { sanitizeFastAPIException } from '$lib/error_handeling';

export const GET: RequestHandler = async (): Promise<Response> => {
	const response: Response = await fetch('http://backend:8181/initial/types');
	if (!response.ok) {
		const data = (await response.json()) as FastAPIException;
		const sanitizedData = sanitizeFastAPIException(data);
		return json(sanitizedData);
	}
	const allTypes = (await response.json()) as TypesType[];
	return json(allTypes);
};
