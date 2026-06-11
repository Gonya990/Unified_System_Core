/**
 * Dashboard Screen — Live System Monitor
 * 
 * Real-time status from igor-gaming via Firestore relay.
 * Shows: connection status, active services, HA state, recent events.
 */
import { StyleSheet, View, ScrollView, TouchableOpacity, RefreshControl } from 'react-native';
import { SafeAreaView } from 'react-native-safe-area-context';
import { useCallback, useState } from 'react';
import { useRouter } from 'expo-router';

import { ThemedText } from '@/components/themed-text';
import { ThemedView } from '@/components/themed-view';
import { BottomTabInset, Colors, MaxContentWidth, Spacing } from '@/constants/theme';
import { useSystemStore } from '@/store/systemStore';
import { requestStatusRefresh } from '@/services/firestoreRelay';

export default function DashboardScreen() {
  const { connected, services, haEntities, haOnline, scrubberActive, mode, backendHost } =
    useSystemStore();
  const [refreshing, setRefreshing] = useState(false);
  const router = useRouter();

  const onRefresh = useCallback(async () => {
    setRefreshing(true);
    await requestStatusRefresh();
    setTimeout(() => setRefreshing(false), 2000);
  }, []);

  const onlineServices = services.filter((s) => s.status === 'online').length;
  const offlineServices = services.filter((s) => s.status === 'offline').length;
  const haOnlineEntities = haEntities.filter((e) => e.state === 'on').length;

  return (
    <ThemedView style={styles.container}>
      <SafeAreaView style={styles.safeArea}>
        <View style={styles.header}>
          <ThemedText style={styles.title}>UNIFIED CORE</ThemedText>
          <View style={[styles.statusBadge, connected ? styles.badgeOnline : styles.badgeOffline]}>
            <View style={[styles.statusDot, { backgroundColor: connected ? Colors.dark.accent : Colors.dark.danger }]} />
            <ThemedText style={[styles.statusText, { color: connected ? Colors.dark.accent : Colors.dark.danger }]}>
              {connected ? 'ONLINE' : 'OFFLINE'}
            </ThemedText>
          </View>
        </View>

        <ScrollView
          contentContainerStyle={styles.content}
          refreshControl={
            <RefreshControl refreshing={refreshing} onRefresh={onRefresh} tintColor={Colors.dark.accent} />
          }
        >
          {/* Primary node */}
          <MetricCard
            label="PRIMARY BACKEND"
            value={backendHost}
            sub="100.126.23.67 • Tailscale"
            accent={Colors.dark.accent}
            icon="🖥"
          />

          {/* Services row */}
          <View style={styles.row}>
            <MetricCard
              label="SERVICES"
              value={`${onlineServices}/${services.length}`}
              sub={`${offlineServices} offline`}
              accent={offlineServices > 0 ? '#ffaa00' : Colors.dark.accent}
              icon="🔧"
              onPress={() => router.push('/services' as any)}
              flex
            />
            <MetricCard
              label="SMART HOME"
              value={haOnline ? `${haOnlineEntities} ON` : 'OFFLINE'}
              sub={`${haEntities.length} устройств`}
              accent={haOnline ? Colors.dark.accent : Colors.dark.danger}
              icon="🏠"
              onPress={() => router.push('/smart-home' as any)}
              flex
            />
          </View>

          {/* Scrubber status */}
          <MetricCard
            label="SCRUBBER"
            value={scrubberActive ? 'ACTIVE' : 'STANDBY'}
            sub={scrubberActive ? 'Анализирует систему' : 'Ожидание активации'}
            accent={scrubberActive ? Colors.dark.accent : Colors.dark.textSecondary}
            icon="🛡"
            onPress={() => router.push('/scrubber' as any)}
          />

          {/* Mode */}
          <MetricCard
            label="SYSTEM MODE"
            value={mode.toUpperCase()}
            sub={
              mode === 'normal' ? 'Стандартный режим' :
              mode === 'scrubber' ? 'Режим очистки активен' :
              '🚨 Аварийный режим'
            }
            accent={
              mode === 'normal' ? Colors.dark.accent :
              mode === 'scrubber' ? '#ffaa00' :
              Colors.dark.danger
            }
            icon={mode === 'normal' ? '✅' : mode === 'scrubber' ? '🔄' : '🚨'}
          />

          {/* Quick actions */}
          <View style={styles.section}>
            <ThemedText style={styles.sectionLabel}>QUICK ACTIONS</ThemedText>
            <View style={styles.quickActions}>
              <QuickBtn label="💬 Chat" onPress={() => router.push('/')} />
              <QuickBtn label="🏠 Home" onPress={() => router.push('/smart-home' as any)} />
              <QuickBtn label="🛡 Scrub" onPress={() => router.push('/scrubber' as any)} />
              <QuickBtn label="⌨️ CMD" onPress={() => router.push('/commands' as any)} />
            </View>
          </View>
        </ScrollView>
      </SafeAreaView>
    </ThemedView>
  );
}

function MetricCard({
  label, value, sub, accent, icon, onPress, flex,
}: {
  label: string;
  value: string;
  sub?: string;
  accent: string;
  icon: string;
  onPress?: () => void;
  flex?: boolean;
}) {
  const Wrapper = onPress ? TouchableOpacity : View;
  return (
    <Wrapper
      style={[styles.card, flex && styles.cardFlex, { borderColor: accent + '30' }]}
      onPress={onPress}
      activeOpacity={0.8}
    >
      <View style={styles.cardTopRow}>
        <ThemedText style={styles.cardLabel}>{label}</ThemedText>
        <ThemedText style={styles.cardIcon}>{icon}</ThemedText>
      </View>
      <ThemedText style={[styles.cardValue, { color: accent }]}>{value}</ThemedText>
      {sub && <ThemedText style={styles.cardSub}>{sub}</ThemedText>}
    </Wrapper>
  );
}

function QuickBtn({ label, onPress }: { label: string; onPress: () => void }) {
  return (
    <TouchableOpacity style={styles.quickBtn} onPress={onPress} activeOpacity={0.7}>
      <ThemedText style={styles.quickBtnText}>{label}</ThemedText>
    </TouchableOpacity>
  );
}

const styles = StyleSheet.create({
  container: { flex: 1 },
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
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
    marginBottom: Spacing.four,
  },
  title: {
    fontSize: 22,
    fontWeight: '900',
    letterSpacing: 2,
    color: Colors.dark.text,
  },
  statusBadge: {
    flexDirection: 'row',
    alignItems: 'center',
    paddingHorizontal: 12,
    paddingVertical: 6,
    borderRadius: 20,
    borderWidth: 1,
    gap: 6,
  },
  badgeOnline: { backgroundColor: '#00ff9d15', borderColor: '#00ff9d30' },
  badgeOffline: { backgroundColor: '#ff003c15', borderColor: '#ff003c30' },
  statusDot: {
    width: 7, height: 7, borderRadius: 4,
    shadowOpacity: 0.8, shadowRadius: 4,
  },
  statusText: {
    fontSize: 11, fontWeight: 'bold', letterSpacing: 1,
  },
  content: { gap: Spacing.three, paddingBottom: Spacing.four },
  row: { flexDirection: 'row', gap: Spacing.three },
  card: {
    backgroundColor: '#111',
    padding: Spacing.four,
    borderRadius: 16,
    borderWidth: 1,
    borderColor: '#222',
    gap: 4,
  },
  cardFlex: { flex: 1 },
  cardTopRow: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
  },
  cardLabel: {
    color: Colors.dark.textSecondary,
    fontSize: 10,
    fontWeight: '700',
    letterSpacing: 1.5,
  },
  cardIcon: { fontSize: 18 },
  cardValue: {
    fontSize: 20,
    fontWeight: '900',
    letterSpacing: 1,
    fontFamily: 'monospace',
  },
  cardSub: {
    color: Colors.dark.textSecondary,
    fontSize: 11,
    marginTop: 2,
  },
  section: { gap: Spacing.two },
  sectionLabel: {
    color: Colors.dark.textSecondary,
    fontSize: 10,
    fontWeight: '700',
    letterSpacing: 2,
  },
  quickActions: {
    flexDirection: 'row',
    gap: Spacing.two,
    flexWrap: 'wrap',
  },
  quickBtn: {
    paddingHorizontal: 16,
    paddingVertical: 10,
    backgroundColor: '#1A1A1A',
    borderRadius: 10,
    borderWidth: 1,
    borderColor: '#2A2A2A',
  },
  quickBtnText: {
    color: Colors.dark.text,
    fontSize: 13,
    fontWeight: '600',
  },
});
