<script>
  export let distro;
</script>

<div class="timeline-item">
  <h2>{distro.name}</h2>
  <p>{distro.description}</p>
  <img src={distro.logoUrl} alt="{distro.name} logo" />
</div>
