import { component$ } from "@builder.io/qwik";
import type { DocumentHead } from "@builder.io/qwik-city";
import { Link } from "@builder.io/qwik-city";
import { Button } from "flowbite-qwik";
import Hero from "../components/starter/hero/hero";

export default component$(() => {
  return (
    <>
      <Hero />
      <div class="flex flex-wrap items-center justify-center gap-2">
        <Button href="/dashboard" size="xl" tag={Link}>Visit Dashboard</Button>
      </div>
    </>
  );
});

export const head: DocumentHead = {
  title: "Generic Dashboard",
  meta: [
    {
      name: "description",
      content: "Generic Crud Dashboard",
    },
  ],
};
