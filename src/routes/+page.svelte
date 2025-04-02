<script>
  import { onMount } from 'svelte';

  let distros = [];
  let page = 1;
  let perPage = 10;
  let totalPages = 1;
  let search = '';
  let filter = '';
  let loading = false;
  let error = '';

  async function fetchDistros() {
    loading = true;
    error = '';
    try {
      const response = await fetch(`/api/distros?page=${page}&perPage=${perPage}&search=${search}&filter=${filter}`);
      const data = await response.json();
      distros = data.distros;
      totalPages = data.pagination.totalPages;
      localStorage.setItem('cachedDistros', JSON.stringify(distros));
    } catch (err) {
      console.error('Failed to load distributions:', err);
      error = 'Could not load distribution data. Please check your connection or try again later.';
      const cachedDistros = localStorage.getItem('cachedDistros');
      if (cachedDistros) {
        distros = JSON.parse(cachedDistros);
        error += ' Showing cached data.';
      }
    } finally {
      loading = false;
    }
  }

  function retryFetch() {
    fetchDistros();
  }

  function nextPage() {
    if (page < totalPages) {
      page += 1;
      fetchDistros();
    }
  }

  function prevPage() {
    if (page > 1) {
      page -= 1;
      fetchDistros();
    }
  }

  function handleSearchChange(event) {
    search = event.target.value;
    fetchDistros();
  }

  function handleFilterChange(event) {
    filter = event.target.value;
    fetchDistros();
  }

  onMount(fetchDistros);
</script>

<main>
  <h1>Distributions</h1>
  <div>
    <input type="text" placeholder="Search..." on:input={handleSearchChange} />
    <select on:change={handleFilterChange}>
      <option value="">All</option>
      <option value="stable">Stable</option>
      <option value="beta">Beta</option>
      <option value="alpha">Alpha</option>
    </select>
  </div>
  {#if loading}
    <p>Loading...</p>
  {:else if error}
    <p>{error}</p>
    <button on:click={retryFetch}>Retry</button>
  {:else}
    <ul>
      {#each distros as distro}
        <li>
          {distro?.name ?? 'Unknown'} - {distro?.release_date ?? 'Date unknown'}
          <img src={distro?.logoUrl ?? 'default-logo.png'} alt="{distro?.name ?? 'Unknown'} logo" />
        </li>
      {/each}
    </ul>
    <div>
      <button on:click={prevPage} disabled={page === 1}>Previous</button>
      <button on:click={nextPage} disabled={page === totalPages}>Next</button>
    </div>
  {/if}
</main>
