<script lang="ts">
  export let body: string;
</script>

<span>
  { body }
</span>

<style>
  span {
    display: block;
    color: var(--color-dark-text-2);
    font-size: 80%;
    text-overflow: ellipsis;
    overflow: hidden;
  }
</style>