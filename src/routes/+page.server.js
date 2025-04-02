import { pb } from '$lib/pocketbase';
import { error } from '@sveltejs/kit';

async function fetchWithRetry(url, options = {}, retries = 2, delay = 1000) {
    for (let i = 0; i < retries; i++) {
        try {
            const response = await fetch(url, options);
            if (!response.ok) throw new Error('Network response was not ok');
            return await response.json();
        } catch (err) {
            if (i < retries - 1) {
                await new Promise(resolve => setTimeout(resolve, delay));
            } else {
                throw err;
            }
        }
    }
}

export async function load({ url }) {
    const page = parseInt(url.searchParams.get('page')) || 1;
    const perPage = parseInt(url.searchParams.get('perPage')) || 10;
    const search = url.searchParams.get('search') || '';
    const filter = url.searchParams.get('filter') || '';

    try {
        const distros = await fetchWithRetry(`${process.env.PUBLIC_POCKETBASE_URL}/api/collections/distros/records?page=${page}&perPage=${perPage}&search=${search}&filter=${filter}`);

        // Add logoUrl field to each distro object
        const baseUrl = process.env.PUBLIC_POCKETBASE_URL;
        distros.items.forEach(distro => {
            distro.logoUrl = distro.logo ? `${baseUrl}/api/files/${distro.collectionId}/${distro.id}/${distro.logo}` : 'default-logo.png';
        });

        // Cache the fetched data in localStorage
        localStorage.setItem('cachedDistros', JSON.stringify(distros));

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

        // Check if there is cached data available
        const cachedDistros = localStorage.getItem('cachedDistros');
        if (cachedDistros) {
            const distros = JSON.parse(cachedDistros);
            return {
                distros: distros.items,
                pagination: {
                    page: distros.page,
                    perPage: distros.perPage,
                    totalItems: distros.totalItems,
                    totalPages: distros.totalPages
                },
                error: 'Could not fetch latest updates. Showing cached data.'
            };
        }

        throw error(500, 'Failed to load distributions');
    }
}
