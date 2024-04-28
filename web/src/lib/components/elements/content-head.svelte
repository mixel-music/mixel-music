<script lang="ts">
  export let head: string;
</script>

<span>
  {head}
</span>

<style>
  span {
    display: block;
    font-size: 95%;
    font-weight: 600;
    text-overflow: ellipsis;
    overflow: hidden;
  }
</style>