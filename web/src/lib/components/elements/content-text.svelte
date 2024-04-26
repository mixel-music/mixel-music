<script lang="ts">
  export let text: string;
</script>

<span>
  { text }
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