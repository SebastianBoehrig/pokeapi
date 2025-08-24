import type { PageLoad } from './$types';
import type { TypesType, FastAPIException } from '$lib/types';

export const load: PageLoad = async ({ fetch }) => {
	const response: Response = await fetch('/api/initial/types');
	const responseData: TypesType[] | FastAPIException = await response.json();

	if ('detail' in responseData) {
		return { allTypes: [] };
	}

	return { allTypes: responseData };
};
