import { component$ } from '@builder.io/qwik';

export const Header = component$(() => {
  return (
    <header class="header">
      <h1>Dashboard</h1>
      <div class="header-actions">
        <button>Profile</button>
        <button>Logout</button>
      </div>
    </header>
  );
});
