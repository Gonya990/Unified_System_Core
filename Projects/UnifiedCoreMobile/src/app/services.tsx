/**
 * Services Screen — Live Service Monitor
 *
 * Real-time service statuses from igor-gaming via Firestore relay.
 * Pull-to-refresh triggers a status_check command to the backend.
 */
import { StyleSheet, View, ScrollView, TouchableOpacity, RefreshControl } from 'react-native';
import { SafeAreaView } from 'react-native-safe-area-context';
import { useCallback, useState } from 'react';

import { ThemedText } from '@/components/themed-text';
import { ThemedView } from '@/components/themed-view';
import { BottomTabInset, Colors, MaxContentWidth, Spacing } from '@/constants/theme';
import { useSystemStore, ServiceInfo } from '@/store/systemStore';
import { requestStatusRefresh, sendSystemCommand } from '@/services/firestoreRelay';

const SERVICE_ICONS: Record<string, string> = {
  ha:       '🏠',
  n8n:      '🔄',
  docker:   '🐳',
  github:   '🔗',
  firebase: '🔥',
  ai_core:  '⚡',
  bybit:    '📈',
};

export default function ServicesScreen() {
  const { services } = useSystemStore();
  const [refreshing, setRefreshing] = useState(false);

  const onRefresh = useCallback(async () => {
    setRefreshing(true);
    await requestStatusRefresh();
    setTimeout(() => setRefreshing(false), 2000);
  }, []);

  const onlineCount  = services.filter((s) => s.status === 'online').length;
  const offlineCount = services.filter((s) => s.status === 'offline').length;
  const warnCount    = services.filter((s) => s.status === 'warning').length;

  return (
    <ThemedView style={styles.container}>
      <SafeAreaView style={styles.safeArea}>
        {/* Header */}
        <View style={styles.header}>
          <View>
            <ThemedText style={styles.title}>SERVICES</ThemedText>
            <ThemedText style={styles.subtitle}>
              {onlineCount} online · {warnCount} warning · {offlineCount} offline
            </ThemedText>
          </View>
          <TouchableOpacity style={styles.syncBtn} onPress={onRefresh}>
            <ThemedText style={styles.syncBtnText}>⟳ Sync</ThemedText>
          </TouchableOpacity>
        </View>

        <ScrollView
          contentContainerStyle={styles.content}
          refreshControl={
            <RefreshControl refreshing={refreshing} onRefresh={onRefresh} tintColor={Colors.dark.accent} />
          }
        >
          {services.map((service) => (
            <ServiceCard key={service.id} service={service} />
          ))}
        </ScrollView>
      </SafeAreaView>
    </ThemedView>
  );
}

function ServiceCard({ service }: { service: ServiceInfo }) {
  const getStatusColor = () => {
    switch (service.status) {
      case 'online':  return Colors.dark.accent;
      case 'offline': return Colors.dark.danger;
      case 'warning': return '#ffaa00';
      default:        return '#555';
    }
  };

  const color = getStatusColor();
  const icon  = SERVICE_ICONS[service.id] ?? '📦';
  const since = service.lastChecked
    ? new Date(service.lastChecked).toLocaleTimeString()
    : '—';

  return (
    <View style={[styles.card, { borderColor: color + '30' }]}>
      <View style={styles.cardLeft}>
        <ThemedText style={styles.cardIcon}>{icon}</ThemedText>
        <View>
          <ThemedText style={styles.cardName}>{service.name}</ThemedText>
          <ThemedText style={styles.cardTime}>последнее обновление: {since}</ThemedText>
          {service.detail && (
            <ThemedText style={styles.cardDetail}>{service.detail}</ThemedText>
          )}
        </View>
      </View>
      <View style={[styles.statusBadge, { borderColor: color + '40', backgroundColor: color + '15' }]}>
        <View style={[styles.statusDot, { backgroundColor: color, shadowColor: color }]} />
        <ThemedText style={[styles.statusText, { color }]}>{service.status.toUpperCase()}</ThemedText>
      </View>
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
    justifyContent: 'space-between',
    alignItems: 'flex-start',
    paddingHorizontal: Spacing.four,
    marginBottom: Spacing.four,
  },
  title: {
    fontSize: 26,
    fontWeight: '900',
    letterSpacing: 2,
    color: Colors.dark.text,
  },
  subtitle: {
    fontSize: 12,
    color: Colors.dark.textSecondary,
    marginTop: 2,
    letterSpacing: 0.5,
  },
  syncBtn: {
    paddingHorizontal: 16,
    paddingVertical: 8,
    backgroundColor: Colors.dark.accent + '20',
    borderRadius: 20,
    borderWidth: 1,
    borderColor: Colors.dark.accent + '50',
  },
  syncBtnText: {
    color: Colors.dark.accent,
    fontWeight: '700',
    fontSize: 13,
  },
  content: {
    gap: Spacing.two + 2,
    paddingHorizontal: Spacing.four,
    paddingBottom: Spacing.four,
  },
  card: {
    backgroundColor: '#111',
    borderRadius: 14,
    borderWidth: 1,
    padding: Spacing.three + 2,
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
  },
  cardLeft: {
    flexDirection: 'row',
    alignItems: 'center',
    gap: 12,
    flex: 1,
  },
  cardIcon: { fontSize: 26 },
  cardName: {
    color: Colors.dark.text,
    fontSize: 15,
    fontWeight: '700',
    letterSpacing: 0.5,
  },
  cardTime: {
    color: Colors.dark.textSecondary,
    fontSize: 11,
    marginTop: 2,
  },
  cardDetail: {
    color: '#ffaa00',
    fontSize: 11,
    marginTop: 2,
    fontFamily: 'monospace',
  },
  statusBadge: {
    flexDirection: 'row',
    alignItems: 'center',
    paddingHorizontal: 10,
    paddingVertical: 5,
    borderRadius: 20,
    borderWidth: 1,
    gap: 5,
    minWidth: 80,
    justifyContent: 'center',
  },
  statusDot: {
    width: 7,
    height: 7,
    borderRadius: 4,
    shadowOpacity: 1,
    shadowRadius: 5,
  },
  statusText: {
    fontSize: 11,
    fontWeight: 'bold',
    letterSpacing: 1,
  },
});
