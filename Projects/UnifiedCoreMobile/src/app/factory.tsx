/**
 * Content Factory Screen — Video Production Monitor
 */
import { StyleSheet, View, ScrollView, RefreshControl, Button, TouchableOpacity } from 'react-native';
import { SafeAreaView } from 'react-native-safe-area-context';
import { useCallback, useState, useEffect } from 'react';

import { ThemedText } from '@/components/themed-text';
import { ThemedView } from '@/components/themed-view';
import { BottomTabInset, Colors, MaxContentWidth, Spacing } from '@/constants/theme';
import { useSystemStore } from '@/store/systemStore';
import { db } from '@/firebaseConfig';
import { collection, query, onSnapshot, addDoc, doc, updateDoc, orderBy, limit } from 'firebase/firestore';

export default function FactoryScreen() {
  const { connected } = useSystemStore();
  const [refreshing, setRefreshing] = useState(false);
  const [factoryJobs, setFactoryJobs] = useState<any[]>([]);

  useEffect(() => {
    // Listen to latest factory jobs
    const q = query(collection(db, 'factory_jobs'), orderBy('createdAt', 'desc'), limit(5));
    const unsub = onSnapshot(q, (snapshot) => {
      const jobs: any[] = [];
      snapshot.forEach(doc => jobs.push({ id: doc.id, ...doc.data() }));
      setFactoryJobs(jobs);
    });
    return () => unsub();
  }, []);

  const onRefresh = useCallback(async () => {
    setRefreshing(true);
    setTimeout(() => setRefreshing(false), 1000);
  }, []);

  const triggerFactory = async () => {
    try {
      await addDoc(collection(db, 'factory_jobs'), {
        status: 'pending',
        progress: 0,
        text: "Сверхмощная генерация! Технологии будущего и нейросети меняют наш мир прямо сейчас. Подписывайся!",
        lang: "ru",
        style: "impact",
        scenes: [
          { keyword: "futuristic AI technology cinematic" },
          { keyword: "abstract digital world glowing" }
        ],
        createdAt: new Date().toISOString()
      });
      alert('Job Sent to Sovereign Node!');
    } catch (e) {
      console.error(e);
      alert('Failed to send job');
    }
  };

  const approveForYouTube = async (jobId: string) => {
    try {
      await updateDoc(doc(db, 'factory_jobs', jobId), {
        status: 'approved'
      });
      alert('Approved for YouTube Publish!');
    } catch (e) {
      console.error(e);
      alert('Failed to approve');
    }
  };

  const activeJob = factoryJobs.find(j => j.status === 'pending' || j.status === 'processing');
  const readyJob = factoryJobs.find(j => j.status === 'ready');

  return (
    <ThemedView style={styles.container}>
      <SafeAreaView style={styles.safeArea}>
        <View style={styles.header}>
          <ThemedText style={styles.title}>CONTENT FACTORY</ThemedText>
          <View style={[styles.statusBadge, connected ? styles.badgeOnline : styles.badgeOffline]}>
            <View style={[styles.statusDot, { backgroundColor: connected ? Colors.dark.accent : Colors.dark.danger }]} />
            <ThemedText style={[styles.statusText, { color: connected ? Colors.dark.accent : Colors.dark.danger }]}>
              SOVEREIGN NODE
            </ThemedText>
          </View>
        </View>

        <ScrollView
          contentContainerStyle={styles.content}
          refreshControl={
            <RefreshControl refreshing={refreshing} onRefresh={onRefresh} tintColor={Colors.dark.accent} />
          }
        >
          {/* Main Controls */}
          <MetricCard
            label="PRODUCTION STATUS"
            value={activeJob ? "PROCESSING" : "IDLE"}
            sub={activeJob ? `Job ${activeJob.id.slice(0, 6)} running...` : "Ready to generate"}
            accent={activeJob ? "#FF9D00" : Colors.dark.accent}
            icon={activeJob ? "⚙️" : "🎬"}
            onPress={activeJob ? undefined : triggerFactory}
          />

          {activeJob && (
            <View style={styles.progressContainer}>
              <ThemedText style={styles.sectionLabel}>PROGRESS</ThemedText>
              <View style={styles.progressBarBg}>
                <View style={[styles.progressBarFill, { width: `${activeJob.progress || 0}%` }]} />
              </View>
              <ThemedText style={styles.progressText}>{activeJob.progress || 0}%</ThemedText>
            </View>
          )}

          {readyJob && (
            <View style={styles.videoCard}>
              <ThemedText style={styles.sectionLabel}>FINAL RENDER READY</ThemedText>
              <ThemedText style={{color: '#aaa', marginVertical: 8}}>Job: {readyJob.id}</ThemedText>
              
              {/* Note: In a real app we'd use expo-video. For now we provide a link or button */}
              <TouchableOpacity 
                style={styles.actionBtn}
                onPress={() => approveForYouTube(readyJob.id)}
              >
                <ThemedText style={styles.actionBtnText}>👍 APPROVE TO YOUTUBE</ThemedText>
              </TouchableOpacity>
            </View>
          )}

          <View style={styles.section}>
            <ThemedText style={styles.sectionLabel}>RECENT JOBS</ThemedText>
            {factoryJobs.length === 0 ? (
              <ThemedText style={styles.emptyText}>No factory jobs yet.</ThemedText>
            ) : (
              factoryJobs.map((job) => (
                <View key={job.id} style={styles.logCard}>
                  <ThemedText style={styles.logText}>Job: {job.id.slice(0, 8)}...</ThemedText>
                  <ThemedText style={[styles.logTime, { color: job.status === 'error' ? 'red' : Colors.dark.accent }]}>
                    STATUS: {job.status.toUpperCase()}
                  </ThemedText>
                </View>
              ))
            )}
          </View>
        </ScrollView>
      </SafeAreaView>
    </ThemedView>
  );
}

function MetricCard({
  label, value, sub, accent, icon, onPress,
}: {
  label: string;
  value: string;
  sub?: string;
  accent: string;
  icon: string;
  onPress?: () => void;
}) {
  const Wrapper = onPress ? TouchableOpacity : View; 
  return (
    <Wrapper style={[styles.card, { borderColor: accent + '30' }]} onPress={onPress}>
      <View style={styles.cardTopRow}>
        <ThemedText style={styles.cardLabel}>{label}</ThemedText>
        <ThemedText style={styles.cardIcon}>{icon}</ThemedText>
      </View>
      <ThemedText style={[styles.cardValue, { color: accent }]}>{value}</ThemedText>
      {sub && <ThemedText style={styles.cardSub}>{sub}</ThemedText>}
    </Wrapper>
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
  },
  statusText: {
    fontSize: 11, fontWeight: 'bold', letterSpacing: 1,
  },
  content: { gap: Spacing.three, paddingBottom: Spacing.four },
  card: {
    backgroundColor: '#111',
    padding: Spacing.four,
    borderRadius: 16,
    borderWidth: 1,
    borderColor: '#222',
    gap: 4,
  },
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
  progressContainer: {
    padding: Spacing.four,
    backgroundColor: '#1A1A1A',
    borderRadius: 12,
  },
  progressBarBg: {
    height: 8,
    backgroundColor: '#333',
    borderRadius: 4,
    marginVertical: 12,
    overflow: 'hidden'
  },
  progressBarFill: {
    height: '100%',
    backgroundColor: '#00ff9d',
  },
  progressText: {
    textAlign: 'right',
    color: '#00ff9d',
    fontWeight: 'bold'
  },
  videoCard: {
    backgroundColor: '#151515',
    padding: Spacing.four,
    borderRadius: 12,
    borderWidth: 1,
    borderColor: '#444'
  },
  actionBtn: {
    backgroundColor: '#FF0000',
    padding: 12,
    borderRadius: 8,
    alignItems: 'center',
    marginTop: 10
  },
  actionBtnText: {
    color: 'white',
    fontWeight: '900',
    letterSpacing: 1
  },
  section: { gap: Spacing.two, marginTop: Spacing.four },
  sectionLabel: {
    color: Colors.dark.textSecondary,
    fontSize: 10,
    fontWeight: '700',
    letterSpacing: 2,
  },
  logCard: {
    backgroundColor: '#1A1A1A',
    padding: Spacing.three,
    borderRadius: 10,
    borderWidth: 1,
    borderColor: '#2A2A2A',
    flexDirection: 'row',
    justifyContent: 'space-between'
  },
  logText: {
    color: Colors.dark.text,
    fontSize: 13,
  },
  logTime: {
    fontSize: 11,
    fontWeight: 'bold',
  },
  emptyText: {
    color: Colors.dark.textSecondary,
    fontSize: 13,
    fontStyle: 'italic',
  }
});
