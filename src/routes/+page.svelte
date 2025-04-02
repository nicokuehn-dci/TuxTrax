<script>
  import { onMount } from 'svelte';
  import { debounce } from 'lodash';
  import VirtualList from 'svelte-virtual-list';

  let distros = [];
  let page = 1;
  let perPage = 10;
  let totalPages = 1;
  let search = '';
  let filter = '';
  let loading = false;
  let error = '';
  let observer;
  let noResults = false;

  async function fetchDistros() {
    loading = true;
    error = '';
    noResults = false;
    try {
      const response = await fetch(`/api/distros?page=${page}&perPage=${perPage}&search=${search}&filter=${filter}`);
      const data = await response.json();
      if (data.distros.length === 0) {
        noResults = true;
      } else {
        distros = [...distros, ...data.distros];
        totalPages = data.pagination.totalPages;
        localStorage.setItem('cachedDistros', JSON.stringify(distros));
      }
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

  const handleSearchChange = debounce((event) => {
    search = event.target.value;
    distros = [];
    page = 1;
    fetchDistros();
  }, 300);

  const handleFilterChange = debounce((event) => {
    filter = event.target.value;
    distros = [];
    page = 1;
    fetchDistros();
  }, 300);

  function handleIntersection(entries) {
    if (entries[0].isIntersecting && page < totalPages) {
      nextPage();
    }
  }

  onMount(() => {
    fetchDistros();
    observer = new IntersectionObserver(handleIntersection);
    observer.observe(document.querySelector('#load-more-trigger'));
  });
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
  {:else if noResults}
    <p>No distributions match your current filters. Try removing some filters.</p>
  {:else}
    <VirtualList items={distros} let:item>
      <div>
        {item?.name ?? 'Unknown'} - {item?.release_date ?? 'Date unknown'}
        <img src={item?.logoUrl ?? 'default-logo.png'} alt="{item?.name ?? 'Unknown'} logo" />
      </div>
    </VirtualList>
    <div id="load-more-trigger"></div>
  {/if}
</main>
