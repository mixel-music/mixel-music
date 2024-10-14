<script lang="ts">
  import { goto } from "$app/navigation";

  let username = '';
  let password = '';

  async function handleSubmit(event) {
    event.preventDefault();
    
    try {
      const response = await fetch('http://localhost:2843/api/signin', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({ username, password }),
        credentials: 'include'
      });

      if (response.ok) {
        await goto('/');
      }
      else {
        console.error('Login failed');
      }
    }
    catch (error) {
      console.error('Login failed', error);
    }
  }
</script>

<form on:submit={handleSubmit}>
  <label for="username">Username :</label>
  <input
    id="username"
    bind:value={username}
    autocomplete="username"
    required
  >
  <label for="password">Password :</label>
  <input
    id="password"
    type="password"
    bind:value={password}
    autocomplete="current-password"
    required
  >

  <button type="submit">Login</button>
</form>
