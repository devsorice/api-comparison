import { routeLoader$ } from '@builder.io/qwik-city';
import type { User } from '~/interfaces/user';

export const useUsersLoader = routeLoader$(async ({ cacheControl }) => {
  // Set the cache control headers
  cacheControl({
    public: true,
    maxAge: 3600, // 1 hour
    sMaxAge: 3600, // 1 hour for shared caches
    staleWhileRevalidate: 3600, // 1 hour to serve stale content while revalidating
  });

  // Your API logic here
  const users = await fetchUsersFromCacheOrDatabase(); // Use cache first

  return users;
});



let cachedUsers: User[] | null = null;
let cacheTimestamp = 0;

async function fetchUsersFromCacheOrDatabase() {
  const CACHE_DURATION = 5000; // 1 hour in milliseconds
  const now = Date.now();

  if (cachedUsers && (now - cacheTimestamp) < CACHE_DURATION) {
    return cachedUsers;
  }

  try {
    const response = await fetch('http://localhost:5555/user/list'); // Adjust the URL to your backend
    const body = await response.json();
    const users = body?.data || [];
    cachedUsers = users;
    cacheTimestamp = now;
    return users;
  } catch (error) {
    console.error('Failed to fetch users:', error);
    return [];
  }
}
