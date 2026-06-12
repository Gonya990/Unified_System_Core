import { Drawer } from 'expo-router/drawer';
import { DarkTheme, DefaultTheme, ThemeProvider } from 'expo-router';
import { useColorScheme } from 'react-native';
import { useEffect } from 'react';

import { AnimatedSplashOverlay } from '@/components/animated-icon';
import { useSystemStore } from '@/store/systemStore';
import { subscribeToSystemStatus } from '@/services/firestoreRelay';

import { Platform } from 'react-native';
import * as Sentry from '@sentry/react-native';

Sentry.init({
  dsn: 'https://6debb0a80478b4db34cedb7dd1ef0690@o4510437397299200.ingest.de.sentry.io/4511549224517712',
  debug: false,
});

// Initialize Analytics & Logging SDKs only on client-side or native
if (Platform.OS !== 'web' || typeof window !== 'undefined') {
  const LogRocket = require('@logrocket/react-native').default;
  const { vexo, identifyDevice } = require('vexo-analytics');
  
  LogRocket.init('pxtwwo/unifiedcoremobile');
  vexo('415c636e-6e1e-4943-bbca-70f4edc5252f');
  identifyDevice('admin@unified-core'); // Set default identifier for the owner
}





function RootLayout() {
  const colorScheme = useColorScheme();
  const { setConnected, updateService, setHAOnline } = useSystemStore();

  // ── Live system status subscription ─────────────────────────────────────
  useEffect(() => {
    const unsub = subscribeToSystemStatus((status) => {
      setConnected(status.ai_core_alive);
      setHAOnline(status.ha_online);

      // Update all service statuses
      Object.entries(status.services).forEach(([id, s]) => {
        updateService(id, { status: s });
      });
    });
    return () => unsub();
  }, []);

  return (
    <ThemeProvider value={colorScheme === 'dark' ? DarkTheme : DefaultTheme}>
      <AnimatedSplashOverlay />
      <Drawer
        screenOptions={{
          headerShown: true,
          headerStyle: {
            backgroundColor: '#000',
          },
          headerTintColor: '#fff',
          drawerStyle: {
            backgroundColor: '#09090b',
            width: 240,
          },
          drawerActiveTintColor: '#00ff9d',
          drawerInactiveTintColor: '#888',
          drawerLabelStyle: {
            fontWeight: '700',
            letterSpacing: 1,
            fontSize: 13,
          },
        }}>
        <Drawer.Screen
          name="index"
          options={{
            drawerLabel: '💬  Chat',
            title: 'Unified Core',
          }}
        />
        <Drawer.Screen
          name="dashboard"
          options={{
            drawerLabel: '📊  Dashboard',
            title: 'System Dashboard',
          }}
        />
        <Drawer.Screen
          name="smart-home"
          options={{
            drawerLabel: '🏠  Умный дом',
            title: 'Smart Home',
          }}
        />
        <Drawer.Screen
          name="scrubber"
          options={{
            drawerLabel: '🛡  Scrubber',
            title: 'Sovereign Scrubber',
          }}
        />
        <Drawer.Screen
          name="services"
          options={{
            drawerLabel: '🔧  Services',
            title: 'Services',
          }}
        />
        <Drawer.Screen
          name="commands"
          options={{
            drawerLabel: '⌨️  Commands',
            title: 'Commands',
          }}
        />
        <Drawer.Screen
          name="logs"
          options={{
            drawerLabel: '📋  Logs',
            title: 'Logs',
          }}
        />
        <Drawer.Screen
          name="settings"
          options={{
            drawerLabel: '⚙️  Settings',
            title: 'Settings',
          }}
        />
        <Drawer.Screen
          name="factory"
          options={{
            drawerLabel: '🎬  Content Factory',
            title: 'Content Factory',
          }}
        />
      </Drawer>
    </ThemeProvider>
  );
}

export default Sentry.wrap(RootLayout);
