import { StyleSheet, TouchableOpacity, View } from 'react-native';
import { SafeAreaView } from 'react-native-safe-area-context';

import { ThemedText } from '@/components/themed-text';
import { ThemedView } from '@/components/themed-view';
import { BottomTabInset, Colors, MaxContentWidth, Spacing } from '@/constants/theme';
import { useState } from 'react';

export default function DashboardScreen() {
  const [triggering, setTriggering] = useState(false);

  const handleTrigger = () => {
    setTriggering(true);
    setTimeout(() => {
      setTriggering(false);
      alert("Factory Triggered! SSH Signal sent to GKE Bot.");
    }, 1500);
  };

  return (
    <ThemedView style={styles.container}>
      <SafeAreaView style={styles.safeArea}>
        
        <View style={styles.header}>
          <ThemedText type="title" style={styles.title}>CLOCKWORK</ThemedText>
          <View style={styles.statusBadge}>
            <View style={styles.statusDot} />
            <ThemedText style={styles.statusText}>SYSTEM ONLINE</ThemedText>
          </View>
        </View>

        <View style={styles.content}>
          <ThemedView type="backgroundElement" style={styles.card}>
            <ThemedText style={styles.cardLabel}>REMOTE HOST</ThemedText>
            <ThemedText style={styles.cardValue}>100.126.23.67 (igor-gaming)</ThemedText>
          </ThemedView>

          <ThemedView type="backgroundElement" style={styles.card}>
            <ThemedText style={styles.cardLabel}>ACTIVE TASKS</ThemedText>
            <ThemedText style={styles.cardValue}>3 Pending, 1 In Progress</ThemedText>
          </ThemedView>
        </View>

        <TouchableOpacity 
          style={[styles.triggerButton, triggering && styles.triggerButtonActive]} 
          onPress={handleTrigger}
          activeOpacity={0.8}
          disabled={triggering}
        >
          <ThemedText style={styles.triggerButtonText}>
            {triggering ? "INITIALIZING..." : "TRIGGER FACTORY"}
          </ThemedText>
        </TouchableOpacity>

      </SafeAreaView>
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
  statusBadge: {
    flexDirection: 'row',
    alignItems: 'center',
    backgroundColor: '#00ff9d20',
    paddingHorizontal: 12,
    paddingVertical: 6,
    borderRadius: 20,
    borderWidth: 1,
    borderColor: '#00ff9d50',
  },
  statusDot: {
    width: 8,
    height: 8,
    borderRadius: 4,
    backgroundColor: Colors.dark.accent,
    marginRight: 8,
    shadowColor: Colors.dark.accent,
    shadowOpacity: 1,
    shadowRadius: 5,
  },
  statusText: {
    color: Colors.dark.accent,
    fontSize: 12,
    fontWeight: 'bold',
    letterSpacing: 1,
  },
  content: {
    flex: 1,
    gap: Spacing.three,
  },
  card: {
    padding: Spacing.four,
    borderRadius: Spacing.three,
    borderWidth: 1,
    borderColor: '#333',
  },
  cardLabel: {
    color: Colors.dark.textSecondary,
    fontSize: 12,
    fontWeight: '600',
    letterSpacing: 1,
    marginBottom: 8,
  },
  cardValue: {
    fontSize: 18,
    color: Colors.dark.text,
    fontFamily: 'monospace',
  },
  triggerButton: {
    backgroundColor: 'transparent',
    borderWidth: 2,
    borderColor: Colors.dark.danger,
    paddingVertical: Spacing.four,
    borderRadius: Spacing.three,
    alignItems: 'center',
    justifyContent: 'center',
    marginTop: 'auto',
    shadowColor: Colors.dark.danger,
    shadowOpacity: 0.3,
    shadowRadius: 10,
    shadowOffset: { width: 0, height: 0 },
  },
  triggerButtonActive: {
    backgroundColor: Colors.dark.danger,
  },
  triggerButtonText: {
    color: Colors.dark.danger,
    fontSize: 18,
    fontWeight: 'bold',
    letterSpacing: 2,
  }
});
