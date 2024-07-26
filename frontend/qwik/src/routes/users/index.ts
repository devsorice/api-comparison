import { routeLoader$ } from '@builder.io/qwik-city';

export const useUsersLoader = routeLoader$(async ({ cacheControl }) => {
  // Set the cache control headers
  cacheControl({
    public: true,
    maxAge: 3600, // 1 hour
    sMaxAge: 3600, // 1 hour for shared caches
    staleWhileRevalidate: 3600, // 1 hour to serve stale content while revalidating
  });

  // Your API logic here
  const users = await fetchUsersFromDatabase(); // Replace with your data fetching logic

  return users;
});

async function fetchUsersFromDatabase() {
  // Simulate fetching data from a database
  try {
    const response = await fetch('http://localhost:5555/user/list'); // Adjust the URL to your backend
    const body = await response.json();
    return body?.data || []
  } catch (error) {
    console.error('Failed to fetch users:', error);
    return []
  }
}
