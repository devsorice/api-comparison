import { component$ } from '@builder.io/qwik';

export const Sidebar = component$(() => {
  return (
    <aside class="sidebar">
      <nav>
        <ul>
          <li><a href="/">Dashboard</a></li>
          <li><a href="/reports">Reports</a></li>
          <li><a href="/settings">Settings</a></li>
        </ul>
      </nav>
    </aside>
  );
});
