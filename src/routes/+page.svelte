<script>
  import { onMount } from 'svelte';
  import { pb } from '$lib/pocketbase';

  let distros = [];
  let page = 1;
  let perPage = 10;
  let totalPages = 1;
  let search = '';
  let filter = '';

  async function fetchDistros() {
    const response = await pb.collection('distros').getList(page, perPage, {
      sort: 'release_date',
      search: search ? { name: { $regex: search, $options: 'i' } } : {},
      filter: filter ? { [filter]: true } : {}
    });
    distros = response.items;
    totalPages = response.totalPages;
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
  <ul>
    {#each distros as distro}
      <li>{distro.name} - {distro.release_date}</li>
    {/each}
  </ul>
  <div>
    <button on:click={prevPage} disabled={page === 1}>Previous</button>
    <button on:click={nextPage} disabled={page === totalPages}>Next</button>
  </div>
</main>
