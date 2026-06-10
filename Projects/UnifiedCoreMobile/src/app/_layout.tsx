import { Drawer } from 'expo-router/drawer';
import { DarkTheme, DefaultTheme, ThemeProvider } from 'expo-router';
import { useColorScheme } from 'react-native';

import { AnimatedSplashOverlay } from '@/components/animated-icon';

export default function RootLayout() {
  const colorScheme = useColorScheme();
  return (
    <ThemeProvider value={colorScheme === 'dark' ? DarkTheme : DefaultTheme}>
      <AnimatedSplashOverlay />
      <Drawer
        screenOptions={{
          headerShown: true,
          headerStyle: {
            backgroundColor: colorScheme === 'dark' ? '#000' : '#fff',
          },
          headerTintColor: colorScheme === 'dark' ? '#fff' : '#000',
        }}>
        <Drawer.Screen
          name="index"
          options={{
            drawerLabel: 'Chat',
            title: 'Unified Core',
          }}
        />
        <Drawer.Screen
          name="dashboard"
          options={{
            drawerLabel: 'Dashboard',
            title: 'System Dashboard',
          }}
        />
        <Drawer.Screen
          name="services"
          options={{
            drawerLabel: 'Services',
            title: 'Services',
          }}
        />
        <Drawer.Screen
          name="commands"
          options={{
            drawerLabel: 'Commands',
            title: 'Commands',
          }}
        />
        <Drawer.Screen
          name="logs"
          options={{
            drawerLabel: 'Logs',
            title: 'Logs',
          }}
        />
        <Drawer.Screen
          name="settings"
          options={{
            drawerLabel: 'Settings',
            title: 'Settings',
          }}
        />
      </Drawer>
    </ThemeProvider>
  );
}
