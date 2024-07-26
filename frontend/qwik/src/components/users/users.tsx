import { component$ } from '@builder.io/qwik';
import { useUsersLoader } from '../../routes/dashboard/users';
import type { User } from '~/interfaces/user';
import "./users.css";


export default component$(() => {
  const users = useUsersLoader().value;

  return (
    <div class="container mx-auto p-4">
      <h1 class="text-2xl font-bold mb-4">Users</h1>
      {users.length === 0 ? (
        <p>Loading...</p>
      ) : (
        <table class="users min-w-full bg-white">
          <thead>
            <tr>
              <th class="py-2">ID</th>
              <th class="py-2">Name</th>
              <th class="py-2">Email</th>
            </tr>
          </thead>
          <tbody>
            {users.map((user: User) => (
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
