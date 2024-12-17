"use client";
import {
  AppShell,
  Burger,
  Group,
  Skeleton,
  MantineProvider,
} from "@mantine/core";
import { useDisclosure } from "@mantine/hooks";
import "@mantine/core/styles.css";
import DoubleNavbar from "@/components/Navbar/Navbar";
import { theme } from '../theme';

export default function RootLayout({ children }: { children: React.ReactNode }) {
  const [opened, { toggle }] = useDisclosure();

  return (
    <html lang="en" suppressHydrationWarning>
      <head>
        <link rel="icon" href="/favicon.ico" />
        <meta name="viewport" content="width=device-width, initial-scale=1" />
        <title>My App</title>
      </head>
      <body>
      <MantineProvider theme={theme}>
          <AppShell
            header={{ height: 60 }}
            navbar={{
              width: 300,
              breakpoint: "sm",
              collapsed: { mobile: !opened },
            }}
            padding="md"
          >
            {/* Header */}
            <AppShell.Header>
              <Group h="100%" px="md">
                <Burger opened={opened} onClick={toggle} hiddenFrom="sm" size="sm" />
                <div>Logo</div>
              </Group>
            </AppShell.Header>

            {/* Navbar */}
            <AppShell.Navbar p="md">
              <DoubleNavbar />
            </AppShell.Navbar>

            {/* Main Content */}
            <AppShell.Main>{children}</AppShell.Main>
          </AppShell>
          {children}</MantineProvider>
      </body>
    </html>
  );
}
