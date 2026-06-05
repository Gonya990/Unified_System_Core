import { StyleSheet, View, FlatList } from 'react-native';
import { SafeAreaView } from 'react-native-safe-area-context';

import { ThemedText } from '@/components/themed-text';
import { ThemedView } from '@/components/themed-view';
import { BottomTabInset, Colors, MaxContentWidth, Spacing } from '@/constants/theme';

const MOCK_TASKS = [
  { id: '1', title: 'GH-001', context: 'FamilyAssistant', capability: 'Morning Brief', status: 'Completed' },
  { id: '2', title: 'GH-002', context: 'ContentFactory', capability: 'Video Processing', status: 'Active' },
  { id: '3', title: 'GH-003', context: 'Infrastructure', capability: 'Proxy Routing', status: 'Pending' },
];

export default function TasksScreen() {
  const renderItem = ({ item }: { item: typeof MOCK_TASKS[0] }) => (
    <ThemedView type="backgroundElement" style={styles.taskCard}>
      <View style={styles.taskHeader}>
        <ThemedText style={styles.taskTitle}>{item.title}</ThemedText>
        <View style={[styles.statusBadge, { borderColor: getStatusColor(item.status) }]}>
          <ThemedText style={[styles.statusText, { color: getStatusColor(item.status) }]}>
            {item.status.toUpperCase()}
          </ThemedText>
        </View>
      </View>
      <ThemedText style={styles.taskContext}>CONTEXT: {item.context}</ThemedText>
      <ThemedText style={styles.taskContext}>CAPABILITY: {item.capability}</ThemedText>
    </ThemedView>
  );

  return (
    <ThemedView style={styles.container}>
      <SafeAreaView style={styles.safeArea}>
        <ThemedText type="title" style={styles.headerTitle}>BILLBOARD TASKS</ThemedText>
        <FlatList
          data={MOCK_TASKS}
          keyExtractor={(item) => item.id}
          renderItem={renderItem}
          contentContainerStyle={styles.listContent}
        />
      </SafeAreaView>
    </ThemedView>
  );
}

const getStatusColor = (status: string) => {
  switch (status) {
    case 'Completed': return Colors.dark.accent;
    case 'Active': return '#00d0ff';
    case 'Pending': return Colors.dark.textSecondary;
    default: return Colors.dark.text;
  }
};

const styles = StyleSheet.create({
  container: { flex: 1 },
  safeArea: {
    flex: 1,
    paddingHorizontal: Spacing.four,
    paddingTop: Spacing.four,
    maxWidth: MaxContentWidth,
    alignSelf: 'center',
    width: '100%',
  },
  headerTitle: {
    fontSize: 24,
    fontWeight: '800',
    letterSpacing: 2,
    marginBottom: Spacing.four,
    color: Colors.dark.text,
  },
  listContent: {
    paddingBottom: BottomTabInset + Spacing.four,
    gap: Spacing.three,
  },
  taskCard: {
    padding: Spacing.four,
    borderRadius: Spacing.three,
    borderWidth: 1,
    borderColor: '#333',
  },
  taskHeader: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
    marginBottom: Spacing.three,
  },
  taskTitle: {
    fontSize: 18,
    fontWeight: 'bold',
    fontFamily: 'monospace',
  },
  statusBadge: {
    paddingHorizontal: 8,
    paddingVertical: 4,
    borderRadius: 4,
    borderWidth: 1,
  },
  statusText: {
    fontSize: 10,
    fontWeight: 'bold',
    letterSpacing: 1,
  },
  taskContext: {
    fontSize: 12,
    color: Colors.dark.textSecondary,
    marginBottom: 4,
    fontFamily: 'monospace',
  }
});
