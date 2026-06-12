/**
 * Logs Screen — Live System Logs
 *
 * Real-time log stream from igor-gaming via Firestore relay.
 * igor-gaming backend writes logs to 'system_logs' collection.
 */
import { useEffect, useState } from 'react';
import { StyleSheet, View, FlatList, TouchableOpacity } from 'react-native';
import { SafeAreaView } from 'react-native-safe-area-context';

import { ThemedText } from '@/components/themed-text';
import { ThemedView } from '@/components/themed-view';
import { BottomTabInset, Colors, MaxContentWidth, Spacing } from '@/constants/theme';
import { subscribeToLogs, SystemLog } from '@/services/firestoreRelay';

type LogLevel = 'all' | 'error' | 'warning' | 'info' | 'success';

const LEVEL_COLORS: Record<string, string> = {
  error:   Colors.dark.danger,
  warning: '#ffaa00',
  success: Colors.dark.accent,
  info:    Colors.dark.textSecondary,
};

const LEVEL_ICONS: Record<string, string> = {
  error:   '🔴',
  warning: '🟡',
  success: '🟢',
  info:    '⚪',
};

export default function LogsScreen() {
  const [logs, setLogs] = useState<SystemLog[]>([]);
  const [filter, setFilter] = useState<LogLevel>('all');

  useEffect(() => {
    const unsub = subscribeToLogs((newLogs) => {
      setLogs(newLogs);
    });
    return () => unsub();
  }, []);

  const filtered = filter === 'all' ? logs : logs.filter((l) => l.level === filter);

  const FILTERS: { key: LogLevel; label: string }[] = [
    { key: 'all',     label: 'All' },
    { key: 'error',   label: '🔴 Error' },
    { key: 'warning', label: '🟡 Warn' },
    { key: 'success', label: '🟢 OK' },
    { key: 'info',    label: '⚪ Info' },
  ];

  return (
    <ThemedView style={styles.container}>
      <SafeAreaView style={styles.safeArea}>
        {/* Header */}
        <View style={styles.header}>
          <ThemedText style={styles.title}>SYSTEM LOGS</ThemedText>
          <View style={styles.countBadge}>
            <ThemedText style={styles.countText}>{filtered.length}</ThemedText>
          </View>
        </View>

        {/* Filter Tabs */}
        <View style={styles.filterRow}>
          {FILTERS.map((f) => (
            <TouchableOpacity
              key={f.key}
              style={[styles.filterTab, filter === f.key && styles.filterTabActive]}
              onPress={() => setFilter(f.key)}
            >
              <ThemedText style={[styles.filterText, filter === f.key && styles.filterTextActive]}>
                {f.label}
              </ThemedText>
            </TouchableOpacity>
          ))}
        </View>

        {/* Log List */}
        {filtered.length === 0 ? (
          <View style={styles.emptyState}>
            <ThemedText style={styles.emptyIcon}>📋</ThemedText>
            <ThemedText style={styles.emptyText}>
              {logs.length === 0
                ? 'Ожидание логов с igor-gaming...'
                : 'Нет записей в этой категории'}
            </ThemedText>
          </View>
        ) : (
          <FlatList
            data={filtered}
            keyExtractor={(item) => item.id ?? item.message}
            contentContainerStyle={styles.listContent}
            renderItem={({ item }) => <LogRow log={item} />}
            showsVerticalScrollIndicator={false}
          />
        )}
      </SafeAreaView>
    </ThemedView>
  );
}

function LogRow({ log }: { log: SystemLog }) {
  const color = LEVEL_COLORS[log.level] ?? Colors.dark.textSecondary;
  const icon  = LEVEL_ICONS[log.level]  ?? '⚪';

  const timeStr = log.timestamp
    ? new Date((log.timestamp as any).toDate?.() ?? log.timestamp).toLocaleTimeString()
    : '—';

  return (
    <View style={[styles.logRow, { borderLeftColor: color }]}>
      <View style={styles.logMeta}>
        <ThemedText style={[styles.logIcon]}>{icon}</ThemedText>
        <ThemedText style={[styles.logTime, { color }]}>{timeStr}</ThemedText>
        {log.source && (
          <ThemedText style={styles.logSource}>[{log.source}]</ThemedText>
        )}
      </View>
      <ThemedText style={styles.logMessage}>{log.message}</ThemedText>
    </View>
  );
}

const styles = StyleSheet.create({
  container: { flex: 1 },
  safeArea: {
    flex: 1,
    paddingTop: Spacing.four,
    paddingBottom: BottomTabInset + Spacing.four,
    maxWidth: MaxContentWidth,
    alignSelf: 'center',
    width: '100%',
  },
  header: {
    flexDirection: 'row',
    alignItems: 'center',
    justifyContent: 'space-between',
    paddingHorizontal: Spacing.four,
    marginBottom: Spacing.three,
  },
  title: {
    fontSize: 26,
    fontWeight: '900',
    letterSpacing: 2,
    color: Colors.dark.text,
  },
  countBadge: {
    backgroundColor: '#1A1A1A',
    borderRadius: 12,
    paddingHorizontal: 10,
    paddingVertical: 4,
    borderWidth: 1,
    borderColor: '#333',
  },
  countText: {
    color: Colors.dark.accent,
    fontWeight: 'bold',
    fontFamily: 'monospace',
    fontSize: 13,
  },
  filterRow: {
    flexDirection: 'row',
    paddingHorizontal: Spacing.four,
    gap: 6,
    marginBottom: Spacing.three,
    flexWrap: 'wrap',
  },
  filterTab: {
    paddingHorizontal: 12,
    paddingVertical: 6,
    borderRadius: 16,
    backgroundColor: '#1A1A1A',
    borderWidth: 1,
    borderColor: '#333',
  },
  filterTabActive: {
    backgroundColor: Colors.dark.accent + '20',
    borderColor: Colors.dark.accent + '60',
  },
  filterText: {
    color: Colors.dark.textSecondary,
    fontSize: 12,
    fontWeight: '600',
  },
  filterTextActive: {
    color: Colors.dark.accent,
  },
  listContent: {
    gap: 1,
    paddingHorizontal: Spacing.four,
    paddingBottom: Spacing.four,
  },
  logRow: {
    backgroundColor: '#0D0D0D',
    borderRadius: 8,
    paddingHorizontal: 12,
    paddingVertical: 10,
    borderLeftWidth: 3,
    marginBottom: 4,
  },
  logMeta: {
    flexDirection: 'row',
    alignItems: 'center',
    gap: 6,
    marginBottom: 4,
  },
  logIcon: { fontSize: 11 },
  logTime: {
    fontFamily: 'monospace',
    fontSize: 11,
    fontWeight: 'bold',
  },
  logSource: {
    color: '#555',
    fontFamily: 'monospace',
    fontSize: 11,
  },
  logMessage: {
    color: Colors.dark.text,
    fontSize: 13,
    lineHeight: 18,
    fontFamily: 'monospace',
  },
  emptyState: {
    flex: 1,
    alignItems: 'center',
    justifyContent: 'center',
    paddingVertical: 60,
  },
  emptyIcon: { fontSize: 48, marginBottom: 16 },
  emptyText: {
    color: Colors.dark.textSecondary,
    textAlign: 'center',
    lineHeight: 22,
  },
});
