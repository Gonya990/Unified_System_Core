import { StyleSheet, View, ScrollView } from 'react-native';
import { SafeAreaView } from 'react-native-safe-area-context';

import { ThemedText } from '@/components/themed-text';
import { ThemedView } from '@/components/themed-view';
import { BottomTabInset, Colors, MaxContentWidth, Spacing } from '@/constants/theme';

export default function LogsScreen() {
  return (
    <ThemedView style={styles.container}>
      <SafeAreaView style={styles.safeArea}>
        <View style={styles.header}>
          <ThemedText type="title" style={styles.title}>SYSTEM LOGS</ThemedText>
        </View>

        <ScrollView contentContainerStyle={styles.content}>
          <LogItem time="14:20" message="System reboot initiated by user" level="info" />
          <LogItem time="14:15" message="N8N container failed to respond (timeout)" level="error" />
          <LogItem time="12:00" message="GitHub sync completed successfully" level="success" />
          <LogItem time="09:00" message="High memory usage on Content Factory" level="warning" />
        </ScrollView>
      </SafeAreaView>
    </ThemedView>
  );
}

function LogItem({ time, message, level }: { time: string, message: string, level: 'info' | 'error' | 'warning' | 'success' }) {
  const getColor = () => {
    switch(level) {
      case 'error': return Colors.dark.danger;
      case 'warning': return '#ffaa00';
      case 'success': return Colors.dark.accent;
      default: return Colors.dark.textSecondary;
    }
  };

  return (
    <View style={styles.logRow}>
      <ThemedText style={[styles.time, { color: getColor() }]}>[{time}]</ThemedText>
      <ThemedText style={styles.message}>{message}</ThemedText>
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
  },
  safeArea: {
    flex: 1,
    paddingHorizontal: Spacing.four,
    paddingTop: Spacing.four,
    paddingBottom: BottomTabInset + Spacing.four,
    maxWidth: MaxContentWidth,
    alignSelf: 'center',
    width: '100%',
  },
  header: {
    marginBottom: Spacing.five,
  },
  title: {
    fontSize: 28,
    fontWeight: '900',
    letterSpacing: 2,
    color: Colors.dark.text,
  },
  content: {
    gap: Spacing.three,
    paddingBottom: Spacing.four,
    backgroundColor: '#050505',
    padding: Spacing.four,
    borderRadius: Spacing.three,
    borderWidth: 1,
    borderColor: '#222',
  },
  logRow: {
    flexDirection: 'row',
    gap: Spacing.three,
    borderBottomWidth: 1,
    borderBottomColor: '#222',
    paddingBottom: 8,
  },
  time: {
    fontFamily: 'monospace',
    fontWeight: 'bold',
  },
  message: {
    flex: 1,
    color: Colors.dark.text,
  }
});
