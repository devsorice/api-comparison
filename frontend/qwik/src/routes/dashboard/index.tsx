import { component$ } from '@builder.io/qwik';
import '~/components/dashboard/dashboard.css';
import { Dashboard } from '~/components/dashboard/Dashboard';

export default component$(() => {
  return (
    <Dashboard />
  );
});
