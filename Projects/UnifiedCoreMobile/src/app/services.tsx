import { StyleSheet, View, ScrollView } from 'react-native';
import { SafeAreaView } from 'react-native-safe-area-context';

import { ThemedText } from '@/components/themed-text';
import { ThemedView } from '@/components/themed-view';
import { BottomTabInset, Colors, MaxContentWidth, Spacing } from '@/constants/theme';

export default function ServicesScreen() {
  return (
    <ThemedView style={styles.container}>
      <SafeAreaView style={styles.safeArea}>
        <View style={styles.header}>
          <ThemedText type="title" style={styles.title}>SERVICES</ThemedText>
        </View>

        <ScrollView contentContainerStyle={styles.content}>
          
          <ServiceCard name="Home Assistant" status="offline" />
          <ServiceCard name="N8N" status="offline" />
          <ServiceCard name="Docker Node" status="online" />
          <ServiceCard name="GitHub Sync" status="online" />
          <ServiceCard name="Firestore DB" status="online" />

        </ScrollView>
      </SafeAreaView>
    </ThemedView>
  );
}

function ServiceCard({ name, status }: { name: string, status: 'online' | 'offline' | 'warning' }) {
  const getStatusColor = () => {
    switch(status) {
      case 'online': return Colors.dark.accent; // green
      case 'offline': return Colors.dark.danger; // red
      case 'warning': return '#ffaa00'; // yellow
      default: return '#777';
    }
  };

  return (
    <ThemedView type="backgroundElement" style={styles.card}>
      <ThemedText style={styles.cardLabel}>{name}</ThemedText>
      <View style={styles.statusBadge}>
        <View style={[styles.statusDot, { backgroundColor: getStatusColor(), shadowColor: getStatusColor() }]} />
        <ThemedText style={[styles.statusText, { color: getStatusColor() }]}>{status.toUpperCase()}</ThemedText>
      </View>
    </ThemedView>
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
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
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
  },
  card: {
    padding: Spacing.four,
    borderRadius: Spacing.three,
    borderWidth: 1,
    borderColor: '#333',
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
  },
  cardLabel: {
    color: Colors.dark.text,
    fontSize: 18,
    fontWeight: 'bold',
    letterSpacing: 1,
  },
  statusBadge: {
    flexDirection: 'row',
    alignItems: 'center',
    backgroundColor: '#111',
    paddingHorizontal: 12,
    paddingVertical: 6,
    borderRadius: 20,
    borderWidth: 1,
    borderColor: '#333',
  },
  statusDot: {
    width: 8,
    height: 8,
    borderRadius: 4,
    marginRight: 8,
    shadowOpacity: 1,
    shadowRadius: 5,
  },
  statusText: {
    fontSize: 12,
    fontWeight: 'bold',
    letterSpacing: 1,
  },
});
