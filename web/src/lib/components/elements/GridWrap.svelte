<script lang="ts">

</script>

<div>
  <slot />
</div>

<style>
  div {
    display: grid;
    grid-template-columns: repeat(8, minmax(180px, 1fr));
    grid-gap: var(--space-m);
    overflow-x: hidden;
  }

  @media screen and (max-width: 1960px) {
    div {
      grid-template-columns: repeat(6, minmax(180px, 1fr));
    }
  }

  @media screen and (max-width: 1560px) {
    div {
      grid-template-columns: repeat(4, minmax(180px, 1fr));
    }
  }

  @media screen and (max-width: 1160px) {
    div {
      grid-template-columns: repeat(3, minmax(180px, 1fr));
    }
  }

  @media screen and (max-width: 960px) {
    div {
      grid-template-columns: repeat(2, minmax(180px, 1fr));
    }
  }

  /* @media screen and (max-width: 1560px) {
    div {
      grid-template-columns: repeat(5, minmax(180px, 1fr));
    }
  } */

  /* @media screen and (max-width: 1360px) {
    div {
      grid-template-columns: repeat(4, minmax(180px, 1fr));
    }
  } */
</style>