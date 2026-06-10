import { StyleSheet, View, TextInput } from 'react-native';
import { SafeAreaView } from 'react-native-safe-area-context';

import { ThemedText } from '@/components/themed-text';
import { ThemedView } from '@/components/themed-view';
import { BottomTabInset, Colors, MaxContentWidth, Spacing } from '@/constants/theme';
import { useState } from 'react';

export default function SettingsScreen() {
  const [ip, setIp] = useState("100.126.23.67");

  return (
    <ThemedView style={styles.container}>
      <SafeAreaView style={styles.safeArea}>
        <View style={styles.header}>
          <ThemedText type="title" style={styles.title}>CONFIG</ThemedText>
        </View>

        <View style={styles.content}>
          
          <ThemedText style={styles.label}>TAILSCALE BACKEND IP</ThemedText>
          <TextInput 
            style={styles.input}
            value={ip}
            onChangeText={setIp}
            keyboardType="numeric"
            placeholderTextColor="#555"
          />

          <View style={styles.divider} />

          <ThemedText style={styles.label}>FIREBASE AUTH STATUS</ThemedText>
          <View style={styles.statusBadge}>
            <View style={styles.statusDot} />
            <ThemedText style={styles.statusText}>ANONYMOUS DEVICE LINKED</ThemedText>
          </View>

        </View>
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
  },
  label: {
    color: Colors.dark.textSecondary,
    fontSize: 12,
    fontWeight: 'bold',
    letterSpacing: 1,
    marginTop: Spacing.four,
  },
  input: {
    backgroundColor: '#111',
    borderWidth: 1,
    borderColor: '#333',
    color: Colors.dark.text,
    fontSize: 18,
    padding: Spacing.four,
    borderRadius: Spacing.two,
    fontFamily: 'monospace',
  },
  divider: {
    height: 1,
    backgroundColor: '#333',
    marginVertical: Spacing.four,
  },
  statusBadge: {
    flexDirection: 'row',
    alignItems: 'center',
    backgroundColor: '#00ff9d10',
    paddingHorizontal: 12,
    paddingVertical: 12,
    borderRadius: Spacing.two,
    borderWidth: 1,
    borderColor: '#00ff9d50',
  },
  statusDot: {
    width: 8,
    height: 8,
    borderRadius: 4,
    backgroundColor: Colors.dark.accent,
    marginRight: 12,
  },
  statusText: {
    color: Colors.dark.accent,
    fontSize: 14,
    fontWeight: 'bold',
    letterSpacing: 1,
  },
});
