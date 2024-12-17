"use client";

import { MantineProvider } from "@mantine/core";

export default function Providers({ children }: { children: React.ReactNode }) {
  return (
    <MantineProvider
      theme={{

      }}
    >
      {children}
    </MantineProvider>
  );
}