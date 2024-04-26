<script lang="ts">
  export let title: string;
</script>

<span>
  { title }
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