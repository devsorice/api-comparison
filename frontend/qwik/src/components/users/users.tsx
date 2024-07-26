import { component$, useStore, useTask$ } from '@builder.io/qwik';

interface User {
  id: number;
  name: string;
  email: string;
}

export default component$(() => {
  const state = useStore({ users: [] as User[], loading: true });

  useTask$(async () => {
    try {
      const response = await fetch('http://localhost:5555/user/list'); // Adjust the URL to your backend
      const body = await response.json();
      const users = body?.data || []
      state.users = users;
    } catch (error) {
      console.error('Failed to fetch users:', error);
    } finally {
      state.loading = false;
    }
  });

  return (
    <div class="container mx-auto p-4">
      <h1 class="text-2xl font-bold mb-4">Users</h1>
      {state.loading ? (
        <p>Loading...</p>
      ) : (
        <table class="min-w-full bg-white">
          <thead>
            <tr>
              <th class="py-2">ID</th>
              <th class="py-2">Name</th>
              <th class="py-2">Email</th>
            </tr>
          </thead>
          <tbody>
            {state.users.map((user) => (
              <tr key={user.id}>
                <td class="border px-4 py-2">{user.id}</td>
                <td class="border px-4 py-2">{user.name}</td>
                <td class="border px-4 py-2">{user.email}</td>
              </tr>
            ))}
          </tbody>
        </table>
      )}
    </div>
  );
});
