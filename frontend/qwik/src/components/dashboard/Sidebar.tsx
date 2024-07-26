import { component$ } from '@builder.io/qwik'
import { Sidebar, useSidebarOpen } from 'flowbite-qwik'
import { IconChartBars3FromLeftSolid } from 'flowbite-qwik-icons'
export default component$(() => {
  const { setIsOpen } = useSidebarOpen()

  return (
    <div class="p-3">
      <button
        onClick$={() => {
          setIsOpen(true)
        }}
        type="button"
        class="ms-3 inline-flex items-center rounded-lg p-2 text-sm text-gray-500 hover:bg-gray-100 focus:outline-none focus:ring-2 focus:ring-gray-200 dark:text-gray-400 dark:hover:bg-gray-700 dark:focus:ring-gray-600 sm:hidden"
      >
        <span class="sr-only">Open sidebar</span>
        <IconChartBars3FromLeftSolid aria-hidden class="h-4 w-4 shrink-0" />
      </button>
      <Sidebar highlight>
        <Sidebar.ItemGroup>
          <Sidebar.Item href='/dashboard/users'>Users</Sidebar.Item>
        </Sidebar.ItemGroup>
      </Sidebar>
    </div>
  )
})
