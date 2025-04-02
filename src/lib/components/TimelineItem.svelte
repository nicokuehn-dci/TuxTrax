<script>
  export let distro;
</script>

<div class="timeline-item">
  <h2>{distro?.name ?? 'Unknown'}</h2>
  <p>{distro?.description ?? 'No description available'}</p>
  <img src={distro?.logoUrl ?? 'default-logo.png'} alt="{distro?.name ?? 'Unknown'} logo" />
</div>
