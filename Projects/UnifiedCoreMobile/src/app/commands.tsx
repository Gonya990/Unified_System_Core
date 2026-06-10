import { StyleSheet, View, ScrollView, TouchableOpacity } from 'react-native';
import { SafeAreaView } from 'react-native-safe-area-context';

import { ThemedText } from '@/components/themed-text';
import { ThemedView } from '@/components/themed-view';
import { BottomTabInset, Colors, MaxContentWidth, Spacing } from '@/constants/theme';
import { useState } from 'react';

export default function CommandsScreen() {
  return (
    <ThemedView style={styles.container}>
      <SafeAreaView style={styles.safeArea}>
        <View style={styles.header}>
          <ThemedText type="title" style={styles.title}>COMMANDS</ThemedText>
        </View>

        <ScrollView contentContainerStyle={styles.content}>
          <CommandButton label="SYNC GITHUB" variant="normal" />
          <CommandButton label="RESTART N8N" variant="warning" />
          <CommandButton label="TRIGGER FACTORY" variant="danger" />
          <CommandButton label="CHECK TAILSCALE" variant="normal" />
        </ScrollView>
      </SafeAreaView>
    </ThemedView>
  );
}

function CommandButton({ label, variant = 'normal' }: { label: string, variant?: 'normal' | 'danger' | 'warning' }) {
  const [active, setActive] = useState(false);

  const getColor = () => {
    switch (variant) {
      case 'danger': return Colors.dark.danger;
      case 'warning': return '#ffaa00';
      default: return Colors.dark.accent;
    }
  };

  const color = getColor();

  return (
    <TouchableOpacity 
      style={[
        styles.button, 
        { borderColor: color, shadowColor: color },
        active && { backgroundColor: color }
      ]}
      onPress={() => {
        setActive(true);
        setTimeout(() => setActive(false), 1000);
      }}
      activeOpacity={0.8}
    >
      <ThemedText style={[styles.buttonText, { color: active ? '#000' : color }]}>
        {active ? "EXECUTING..." : label}
      </ThemedText>
    </TouchableOpacity>
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
    gap: Spacing.four,
    paddingBottom: Spacing.four,
  },
  button: {
    backgroundColor: 'transparent',
    borderWidth: 2,
    paddingVertical: Spacing.four,
    borderRadius: Spacing.three,
    alignItems: 'center',
    justifyContent: 'center',
    shadowOpacity: 0.2,
    shadowRadius: 10,
    shadowOffset: { width: 0, height: 0 },
  },
  buttonText: {
    fontSize: 18,
    fontWeight: 'bold',
    letterSpacing: 2,
  }
});
