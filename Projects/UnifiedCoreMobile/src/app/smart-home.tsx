/**
 * Smart Home Screen — Умный дом
 * 
 * Real-time Home Assistant control via Firestore relay to igor-gaming.
 * Lights, climate, scenes, sensors — all in one sovereign interface.
 */
import { useState, useEffect, useCallback } from 'react';
import {
  StyleSheet,
  View,
  ScrollView,
  TouchableOpacity,
  ActivityIndicator,
  RefreshControl,
} from 'react-native';
import { SafeAreaView } from 'react-native-safe-area-context';

import { ThemedText } from '@/components/themed-text';
import { ThemedView } from '@/components/themed-view';
import { Colors, Spacing } from '@/constants/theme';
import { useSystemStore, HAEntity } from '@/store/systemStore';
import {
  sendHACommand,
  subscribeToHAStates,
  requestStatusRefresh,
} from '@/services/firestoreRelay';

type HAFilter = 'all' | 'light' | 'climate' | 'sensor' | 'scene';

export default function SmartHomeScreen() {
  const { haEntities, haOnline, setHAEntities, setHAOnline } = useSystemStore();
  const [filter, setFilter] = useState<HAFilter>('all');
  const [loading, setLoading] = useState(false);
  const [refreshing, setRefreshing] = useState(false);
  const [pendingCommands, setPendingCommands] = useState<Set<string>>(new Set());

  // ── Subscribe to HA states from Firestore ───────────────────────────────────
  useEffect(() => {
    const unsub = subscribeToHAStates((states) => {
      const entities: HAEntity[] = states.map((s) => {
        const domain = s.entity_id.split('.')[0] as HAEntity['domain'];
        return {
          entity_id: s.entity_id,
          friendly_name: (s.attributes?.friendly_name as string) ?? s.entity_id,
          state: s.state,
          domain,
          attributes: s.attributes,
          lastUpdated: Date.now(),
        };
      });
      setHAEntities(entities);
      setHAOnline(entities.length > 0);
    });
    return () => unsub();
  }, []);

  // ── Refresh ─────────────────────────────────────────────────────────────────
  const onRefresh = useCallback(async () => {
    setRefreshing(true);
    await requestStatusRefresh();
    setTimeout(() => setRefreshing(false), 2000);
  }, []);

  // ── Toggle entity ───────────────────────────────────────────────────────────
  const toggleEntity = useCallback(async (entity: HAEntity) => {
    const id = entity.entity_id;
    setPendingCommands((prev) => new Set(prev).add(id));
    try {
      const isOn = entity.state === 'on';
      await sendHACommand(isOn ? 'turn_off' : 'turn_on', id);
    } finally {
      setTimeout(() => {
        setPendingCommands((prev) => {
          const next = new Set(prev);
          next.delete(id);
          return next;
        });
      }, 3000);
    }
  }, []);

  // ── Filter entities ─────────────────────────────────────────────────────────
  const filteredEntities = haEntities.filter((e) => {
    if (filter === 'all') return ['light', 'switch', 'climate', 'sensor', 'scene', 'media_player'].includes(e.domain);
    if (filter === 'light') return e.domain === 'light' || e.domain === 'switch';
    if (filter === 'climate') return e.domain === 'climate';
    if (filter === 'sensor') return e.domain === 'sensor' || e.domain === 'binary_sensor';
    if (filter === 'scene') return e.domain === 'scene' || e.domain === 'script';
    return true;
  });

  const FILTERS: { key: HAFilter; label: string; icon: string }[] = [
    { key: 'all',     label: 'Все',      icon: '🏠' },
    { key: 'light',   label: 'Свет',     icon: '💡' },
    { key: 'climate', label: 'Климат',   icon: '🌡' },
    { key: 'sensor',  label: 'Датчики',  icon: '📡' },
    { key: 'scene',   label: 'Сцены',    icon: '🎭' },
  ];

  return (
    <ThemedView style={styles.container}>
      <SafeAreaView style={styles.safeArea}>
        {/* Header */}
        <View style={styles.header}>
          <View>
            <ThemedText style={styles.title}>УМНЫЙ ДОМ</ThemedText>
            <ThemedText style={styles.subtitle}>
              {haOnline
                ? `${haEntities.length} устройств онлайн`
                : 'Home Assistant offline'}
            </ThemedText>
          </View>
          <View style={[styles.statusBadge, haOnline ? styles.statusOnline : styles.statusOffline]}>
            <View style={[styles.statusDot, { backgroundColor: haOnline ? Colors.dark.accent : Colors.dark.danger }]} />
            <ThemedText style={[styles.statusText, { color: haOnline ? Colors.dark.accent : Colors.dark.danger }]}>
              {haOnline ? 'LIVE' : 'OFFLINE'}
            </ThemedText>
          </View>
        </View>

        {/* Filter Tabs */}
        <ScrollView
          horizontal
          showsHorizontalScrollIndicator={false}
          style={styles.filterScroll}
          contentContainerStyle={styles.filterContainer}
        >
          {FILTERS.map((f) => (
            <TouchableOpacity
              key={f.key}
              style={[styles.filterTab, filter === f.key && styles.filterTabActive]}
              onPress={() => setFilter(f.key)}
            >
              <ThemedText style={[styles.filterText, filter === f.key && styles.filterTextActive]}>
                {f.icon} {f.label}
              </ThemedText>
            </TouchableOpacity>
          ))}
        </ScrollView>

        {/* Entity Grid */}
        <ScrollView
          contentContainerStyle={styles.grid}
          refreshControl={
            <RefreshControl
              refreshing={refreshing}
              onRefresh={onRefresh}
              tintColor={Colors.dark.accent}
            />
          }
        >
          {filteredEntities.length === 0 ? (
            <View style={styles.emptyState}>
              <ThemedText style={styles.emptyIcon}>🏠</ThemedText>
              <ThemedText style={styles.emptyText}>
                {haOnline
                  ? 'Нет устройств в этой категории'
                  : 'Ожидание подключения\nк Home Assistant...'}
              </ThemedText>
              <TouchableOpacity style={styles.refreshButton} onPress={onRefresh}>
                <ThemedText style={styles.refreshButtonText}>Обновить</ThemedText>
              </TouchableOpacity>
            </View>
          ) : (
            filteredEntities.map((entity) => (
              <EntityCard
                key={entity.entity_id}
                entity={entity}
                pending={pendingCommands.has(entity.entity_id)}
                onToggle={() => toggleEntity(entity)}
              />
            ))
          )}
        </ScrollView>
      </SafeAreaView>
    </ThemedView>
  );
}

// ─── EntityCard Component ──────────────────────────────────────────────────────

function EntityCard({
  entity,
  pending,
  onToggle,
}: {
  entity: HAEntity;
  pending: boolean;
  onToggle: () => void;
}) {
  const isOn = entity.state === 'on';
  const isToggleable = ['light', 'switch', 'scene', 'script'].includes(entity.domain);
  const isSensor = entity.domain === 'sensor' || entity.domain === 'binary_sensor';

  const getDomainIcon = () => {
    switch (entity.domain) {
      case 'light':  return isOn ? '💡' : '🔦';
      case 'switch': return isOn ? '🟢' : '⭕';
      case 'climate': return '🌡';
      case 'sensor': return '📡';
      case 'binary_sensor': return entity.state === 'on' ? '🔴' : '🟢';
      case 'scene':  return '🎭';
      case 'script': return '⚡';
      case 'media_player': return '🎵';
      default: return '📱';
    }
  };

  const getStateColor = () => {
    if (isOn) return Colors.dark.accent;
    if (entity.state === 'unavailable') return Colors.dark.danger;
    return Colors.dark.textSecondary;
  };

  const unit = entity.attributes?.unit_of_measurement as string | undefined;
  const displayState = `${entity.state}${unit ? ' ' + unit : ''}`;

  return (
    <TouchableOpacity
      style={[styles.card, isOn && styles.cardActive]}
      onPress={isToggleable ? onToggle : undefined}
      activeOpacity={isToggleable ? 0.7 : 1}
      disabled={pending}
    >
      <View style={styles.cardHeader}>
        <ThemedText style={styles.cardIcon}>{getDomainIcon()}</ThemedText>
        {pending && <ActivityIndicator size="small" color={Colors.dark.accent} />}
        {!pending && isToggleable && (
          <View style={[styles.toggleDot, isOn && styles.toggleDotOn]} />
        )}
      </View>
      <ThemedText style={styles.cardName} numberOfLines={2}>
        {entity.friendly_name}
      </ThemedText>
      <ThemedText style={[styles.cardState, { color: getStateColor() }]}>
        {displayState}
      </ThemedText>
    </TouchableOpacity>
  );
}

// ─── Styles ────────────────────────────────────────────────────────────────────

const styles = StyleSheet.create({
  container: { flex: 1 },
  safeArea: {
    flex: 1,
    paddingTop: Spacing.four,
  },
  header: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
    paddingHorizontal: Spacing.four,
    marginBottom: Spacing.three,
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
  statusBadge: {
    flexDirection: 'row',
    alignItems: 'center',
    paddingHorizontal: 12,
    paddingVertical: 6,
    borderRadius: 20,
    borderWidth: 1,
    gap: 6,
  },
  statusOnline: {
    backgroundColor: '#00ff9d15',
    borderColor: '#00ff9d30',
  },
  statusOffline: {
    backgroundColor: '#ff003c15',
    borderColor: '#ff003c30',
  },
  statusDot: {
    width: 7,
    height: 7,
    borderRadius: 4,
    shadowOpacity: 0.8,
    shadowRadius: 4,
  },
  statusText: {
    fontSize: 11,
    fontWeight: 'bold',
    letterSpacing: 1,
  },
  filterScroll: {
    maxHeight: 48,
    marginBottom: Spacing.three,
  },
  filterContainer: {
    paddingHorizontal: Spacing.four,
    gap: 8,
    alignItems: 'center',
  },
  filterTab: {
    paddingHorizontal: 16,
    paddingVertical: 8,
    borderRadius: 20,
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
    fontSize: 13,
    fontWeight: '600',
  },
  filterTextActive: {
    color: Colors.dark.accent,
  },
  grid: {
    flexDirection: 'row',
    flexWrap: 'wrap',
    padding: Spacing.three,
    gap: Spacing.three,
  },
  card: {
    width: '47%',
    backgroundColor: '#111',
    borderRadius: 16,
    padding: Spacing.three,
    borderWidth: 1,
    borderColor: '#222',
    minHeight: 110,
    justifyContent: 'space-between',
  },
  cardActive: {
    borderColor: Colors.dark.accent + '50',
    backgroundColor: '#00ff9d08',
  },
  cardHeader: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
    marginBottom: 8,
  },
  cardIcon: { fontSize: 24 },
  toggleDot: {
    width: 10,
    height: 10,
    borderRadius: 5,
    backgroundColor: '#333',
    borderWidth: 1,
    borderColor: '#444',
  },
  toggleDotOn: {
    backgroundColor: Colors.dark.accent,
    borderColor: Colors.dark.accent,
    shadowColor: Colors.dark.accent,
    shadowOpacity: 0.8,
    shadowRadius: 4,
  },
  cardName: {
    fontSize: 13,
    fontWeight: '700',
    color: Colors.dark.text,
    letterSpacing: 0.3,
    flex: 1,
  },
  cardState: {
    fontSize: 12,
    marginTop: 4,
    fontFamily: 'monospace',
  },
  emptyState: {
    flex: 1,
    alignItems: 'center',
    justifyContent: 'center',
    paddingVertical: 60,
    width: '100%',
  },
  emptyIcon: { fontSize: 48, marginBottom: 16 },
  emptyText: {
    color: Colors.dark.textSecondary,
    textAlign: 'center',
    lineHeight: 22,
    marginBottom: 20,
  },
  refreshButton: {
    paddingHorizontal: 24,
    paddingVertical: 10,
    backgroundColor: Colors.dark.accent + '20',
    borderRadius: 20,
    borderWidth: 1,
    borderColor: Colors.dark.accent + '50',
  },
  refreshButtonText: {
    color: Colors.dark.accent,
    fontWeight: '700',
  },
});
