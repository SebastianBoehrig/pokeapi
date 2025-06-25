import type { PageLoad } from './$types';
import type { TypesType } from '$lib/types';

export const load: PageLoad = async ({ fetch }) => {
	const response: Response = await fetch('/api/initial/types');
	const allTypes: TypesType[] = await response.json();

	return { allTypes };
};
