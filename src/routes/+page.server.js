import { pb } from '$lib/pocketbase';

export async function load({ url }) {
    const page = parseInt(url.searchParams.get('page')) || 1;
    const perPage = parseInt(url.searchParams.get('perPage')) || 10;

    const distros = await pb.collection('distros').getList(page, perPage, { sort: 'release_date' });

    return {
        distros: distros.items,
        pagination: {
            page: distros.page,
            perPage: distros.perPage,
            totalItems: distros.totalItems,
            totalPages: distros.totalPages
        }
    };
}
