import {
  IconCalendarStats,
  IconDeviceDesktopAnalytics,
  IconFingerprint,
  IconGauge,
  IconHome2,
  IconSettings,
  IconUser,
} from "@tabler/icons-react";
import Link from "next/link";
import { Title, Tooltip, UnstyledButton, Stack } from "@mantine/core";
import classes from "./Navbar.module.css";
import { useState } from "react";

const mainLinksMockdata = [
  {
    icon: IconGauge,
    label: "Bulletin",
    pages: [
      { label: "Stats", href: "/" },
      { label: "Reports", href: "/dashboard/reports" },
    ],
  },
  {
    icon: IconHome2,
    label: "Mammals",
    pages: [
      { label: "Profiles", href: "/animals?category=mammal" },
      { label: "Species", href: "/mammals/species" },
      { label: "Habitats", href: "/mammals/habitats" },
    ],
  },
  {
    icon: IconDeviceDesktopAnalytics,
    label: "Analytics",
    pages: [
      { label: "Traffic", href: "/analytics/traffic" },
      { label: "Engagement", href: "/analytics/engagement" },
    ],
  },
  {
    icon: IconCalendarStats,
    label: "Releases",
    pages: [
      { label: "Upcoming", href: "/releases/upcoming" },
      { label: "History", href: "/releases/history" },
    ],
  },
  {
    icon: IconUser,
    label: "Account",
    pages: [
      { label: "Profile", href: "/account/profile" },
      { label: "Settings", href: "/account/settings" },
    ],
  },
  {
    icon: IconFingerprint,
    label: "Security",
    pages: [
      { label: "2FA", href: "/security/2fa" },
      { label: "Activity Log", href: "/security/activity" },
    ],
  },
  {
    icon: IconSettings,
    label: "Settings",
    pages: [
      { label: "Preferences", href: "/settings/preferences" },
      { label: "Notifications", href: "/settings/notifications" },
    ],
  },
];

export function DoubleNavbar() {
  const [active, setActive] = useState<string | null>(mainLinksMockdata[0]?.label || null);

  // Render the icons in the sidebar
  const mainLinks = mainLinksMockdata.map((link) => (
    <Tooltip
      label={link.label}
      position="right"
      withArrow
      transitionProps={{ duration: 0 }}
      key={link.label}
    >
      <UnstyledButton
        onClick={() => setActive(link.label)} // Only sets active; no additional actions
        className={classes.mainLink}
        data-active={link.label === active || undefined}
      >
        <link.icon size={22} stroke={1.5} />
      </UnstyledButton>
    </Tooltip>
  ));

  // Render the tabs for the selected section
  const activeTabs = mainLinksMockdata.find((link) => link.label === active)?.pages;

  return (
    <nav className={classes.navbar}>
      <div className={classes.wrapper}>
        {/* Sidebar with icons */}
        <div className={classes.aside}>
          <div className={classes.logo}></div>
          {mainLinks}
        </div>

        {/* Main area with tabs */}
        <div className={classes.main}>
          <Title order={4} className={classes.title}>
            {active}
          </Title>

          {activeTabs ? (
            <Stack spacing="xs">
              {activeTabs.map((tab) => (
                <Link
                  href={tab.href}
                  key={tab.label}
                  className={classes.link}
                  shallow
                >
                  {tab.label}
                </Link>
              ))}
            </Stack>
          ) : (
            <div>Select an icon to view pages</div>
          )}
        </div>
      </div>
    </nav>
  );
}

export default DoubleNavbar;
