import { component$ } from '@builder.io/qwik';
import { Sidebar } from './Sidebar';
import { Header } from './Header';
import { MainContent } from './MainContent';

export const Dashboard = component$(() => {
  return (
    <div class="dashboard">
      <Sidebar />
      <div class="main-area">
        <Header />
        <MainContent />
      </div>
    </div>
  );
});
