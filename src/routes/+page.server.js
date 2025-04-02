import { pb } from '$lib/pocketbase';
import { error } from '@sveltejs/kit';

export async function load({ url }) {
    const page = parseInt(url.searchParams.get('page')) || 1;
    const perPage = parseInt(url.searchParams.get('perPage')) || 10;
    const search = url.searchParams.get('search') || '';
    const filter = url.searchParams.get('filter') || '';

    try {
        const distros = await pb.collection('distros').getList(page, perPage, {
            sort: 'release_date',
            filter: filter ? { [filter]: true } : {},
            search: search ? { name: { $regex: search, $options: 'i' } } : {}
        });

        // Add logoUrl field to each distro object
        const baseUrl = process.env.PUBLIC_POCKETBASE_URL;
        distros.items.forEach(distro => {
            distro.logoUrl = `${baseUrl}/api/files/${distro.collectionId}/${distro.id}/${distro.logo}`;
        });

        return {
            distros: distros.items,
            pagination: {
                page: distros.page,
                perPage: distros.perPage,
                totalItems: distros.totalItems,
                totalPages: distros.totalPages
            }
        };
    } catch (err) {
        console.error('Failed to load distributions:', err);
        throw error(500, 'Failed to load distributions');
    }
}
