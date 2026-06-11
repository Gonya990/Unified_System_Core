/**
 * Scrubber Screen — Суверенный Скрабер
 * 
 * Filters, analyzes, and cleans data flowing through the Unified System.
 * Sends scrubber tasks to igor-gaming for processing.
 * Real-time log stream from backend via Firestore.
 */
import { useState, useEffect, useRef } from 'react';
import {
  StyleSheet,
  View,
  ScrollView,
  TouchableOpacity,
  Switch,
  Animated,
} from 'react-native';
import { SafeAreaView } from 'react-native-safe-area-context';

import { ThemedText } from '@/components/themed-text';
import { ThemedView } from '@/components/themed-view';
import { Colors, Spacing } from '@/constants/theme';
import { useSystemStore } from '@/store/systemStore';
import { runScrubber, subscribeToResponses } from '@/services/firestoreRelay';

type ScrubberTarget =
  | 'logs'
  | 'firestore'
  | 'emails'
  | 'content'
  | 'security'
  | 'memory';

interface ScrubberJob {
  id: string;
  target: ScrubberTarget;
  label: string;
  icon: string;
  description: string;
  running: boolean;
  lastResult?: string;
  lastRun?: number;
}

const DEFAULT_JOBS: ScrubberJob[] = [
  {
    id: 'logs',
    target: 'logs',
    label: 'Очистка логов',
    icon: '📋',
    description: 'Архивирует и очищает старые логи системы',
    running: false,
  },
  {
    id: 'firestore',
    target: 'firestore',
    label: 'Firestore Audit',
    icon: '🗄',
    description: 'Проверяет целостность и устаревшие записи',
    running: false,
  },
  {
    id: 'emails',
    target: 'emails',
    label: 'Email Scrub',
    icon: '📧',
    description: 'Фильтрует спам и нерелевантные письма',
    running: false,
  },
  {
    id: 'content',
    target: 'content',
    label: 'Content Factory',
    icon: '🎬',
    description: 'Очищает временные медиафайлы и кэш',
    running: false,
  },
  {
    id: 'security',
    target: 'security',
    label: 'Security Scan',
    icon: '🛡',
    description: 'Проверяет токены, ключи и права доступа',
    running: false,
  },
  {
    id: 'memory',
    target: 'memory',
    label: 'Memory Consolidation',
    icon: '🧠',
    description: 'Сжимает и консолидирует память агентов',
    running: false,
  },
];

export default function ScrubberScreen() {
  const { scrubberActive, setScrubberActive, scrubberLogs, addScrubberLog, clearScrubberLogs } =
    useSystemStore();
  const [jobs, setJobs] = useState<ScrubberJob[]>(DEFAULT_JOBS);
  const scrollRef = useRef<ScrollView>(null);
  const pulseAnim = useRef(new Animated.Value(1)).current;

  // ── Pulse animation for active scrubber ──────────────────────────────────
  useEffect(() => {
    if (scrubberActive) {
      Animated.loop(
        Animated.sequence([
          Animated.timing(pulseAnim, { toValue: 1.05, duration: 800, useNativeDriver: true }),
          Animated.timing(pulseAnim, { toValue: 1, duration: 800, useNativeDriver: true }),
        ])
      ).start();
    } else {
      pulseAnim.setValue(1);
    }
  }, [scrubberActive]);

  // ── Subscribe to scrubber results ────────────────────────────────────────
  useEffect(() => {
    const unsub = subscribeToResponses((response) => {
      if (response.type === 'scrubber_result') {
        addScrubberLog(`✅ ${response.text}`);
        // Update job status
        const meta = response.metadata as { target?: ScrubberTarget } | undefined;
        if (meta?.target) {
          setJobs((prev) =>
            prev.map((j) =>
              j.target === meta.target
                ? { ...j, running: false, lastResult: response.text, lastRun: Date.now() }
                : j
            )
          );
        }
      }
    });
    return () => unsub();
  }, []);

  // ── Run a scrubber job ──────────────────────────────────────────────────
  const runJob = async (job: ScrubberJob) => {
    setJobs((prev) =>
      prev.map((j) => (j.id === job.id ? { ...j, running: true } : j))
    );
    addScrubberLog(`🔄 Запуск: ${job.label}...`);
    try {
      await runScrubber(job.target, { label: job.label });
    } catch {
      addScrubberLog(`❌ Ошибка запуска ${job.label}`);
      setJobs((prev) =>
        prev.map((j) => (j.id === job.id ? { ...j, running: false } : j))
      );
    }
  };

  // ── Run all jobs ─────────────────────────────────────────────────────────
  const runAllJobs = async () => {
    setScrubberActive(true);
    addScrubberLog('⚡ ПОЛНЫЙ СКРАБ ЗАПУЩЕН');
    for (const job of jobs) {
      await runJob(job);
      await new Promise((r) => setTimeout(r, 500));
    }
  };

  return (
    <ThemedView style={styles.container}>
      <SafeAreaView style={styles.safeArea}>
        {/* Header */}
        <View style={styles.header}>
          <View>
            <ThemedText style={styles.title}>SCRUBBER</ThemedText>
            <ThemedText style={styles.subtitle}>Суверенная очистка системы</ThemedText>
          </View>
          <Animated.View style={[styles.masterToggle, { transform: [{ scale: pulseAnim }] }]}>
            <Switch
              value={scrubberActive}
              onValueChange={setScrubberActive}
              trackColor={{ false: '#333', true: Colors.dark.accent + '60' }}
              thumbColor={scrubberActive ? Colors.dark.accent : '#555'}
            />
          </Animated.View>
        </View>

        {/* Run All Button */}
        {scrubberActive && (
          <TouchableOpacity style={styles.runAllButton} onPress={runAllJobs}>
            <ThemedText style={styles.runAllText}>⚡ ПОЛНЫЙ СКРАБ</ThemedText>
          </TouchableOpacity>
        )}

        <ScrollView contentContainerStyle={styles.content}>
          {/* Jobs */}
          <View style={styles.section}>
            <ThemedText style={styles.sectionTitle}>ЗАДАЧИ</ThemedText>
            {jobs.map((job) => (
              <JobCard
                key={job.id}
                job={job}
                enabled={scrubberActive}
                onRun={() => runJob(job)}
              />
            ))}
          </View>

          {/* Log Stream */}
          <View style={styles.section}>
            <View style={styles.logHeader}>
              <ThemedText style={styles.sectionTitle}>LOG STREAM</ThemedText>
              <TouchableOpacity onPress={clearScrubberLogs}>
                <ThemedText style={styles.clearBtn}>CLEAR</ThemedText>
              </TouchableOpacity>
            </View>
            <View style={styles.logContainer}>
              <ScrollView
                ref={scrollRef}
                style={styles.logScroll}
                onContentSizeChange={() => scrollRef.current?.scrollToEnd()}
              >
                {scrubberLogs.length === 0 ? (
                  <ThemedText style={styles.logEmpty}>
                    {'> Скрабер готов. Активируй режим.'}
                  </ThemedText>
                ) : (
                  scrubberLogs.map((log, i) => (
                    <ThemedText key={i} style={styles.logLine}>
                      {log}
                    </ThemedText>
                  ))
                )}
              </ScrollView>
            </View>
          </View>
        </ScrollView>
      </SafeAreaView>
    </ThemedView>
  );
}

function JobCard({
  job,
  enabled,
  onRun,
}: {
  job: ScrubberJob;
  enabled: boolean;
  onRun: () => void;
}) {
  return (
    <ThemedView type="backgroundElement" style={styles.jobCard}>
      <View style={styles.jobLeft}>
        <ThemedText style={styles.jobIcon}>{job.icon}</ThemedText>
        <View style={styles.jobInfo}>
          <ThemedText style={styles.jobLabel}>{job.label}</ThemedText>
          <ThemedText style={styles.jobDesc}>{job.description}</ThemedText>
          {job.lastRun && (
            <ThemedText style={styles.jobLastRun}>
              Последний запуск: {new Date(job.lastRun).toLocaleTimeString()}
            </ThemedText>
          )}
        </View>
      </View>
      <TouchableOpacity
        style={[styles.jobRunBtn, (!enabled || job.running) && styles.jobRunBtnDisabled]}
        onPress={onRun}
        disabled={!enabled || job.running}
      >
        <ThemedText style={[styles.jobRunText, (!enabled || job.running) && styles.jobRunTextDisabled]}>
          {job.running ? '...' : '▶'}
        </ThemedText>
      </TouchableOpacity>
    </ThemedView>
  );
}

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
    letterSpacing: 3,
    color: Colors.dark.text,
  },
  subtitle: {
    fontSize: 11,
    color: Colors.dark.textSecondary,
    letterSpacing: 0.5,
    marginTop: 2,
  },
  masterToggle: {
    padding: 4,
  },
  runAllButton: {
    marginHorizontal: Spacing.four,
    marginBottom: Spacing.three,
    paddingVertical: 14,
    backgroundColor: Colors.dark.accent + '15',
    borderWidth: 1,
    borderColor: Colors.dark.accent,
    borderRadius: 12,
    alignItems: 'center',
  },
  runAllText: {
    color: Colors.dark.accent,
    fontWeight: '900',
    letterSpacing: 2,
    fontSize: 14,
  },
  content: {
    padding: Spacing.four,
    gap: Spacing.four,
    paddingBottom: Spacing.six,
  },
  section: { gap: Spacing.two },
  sectionTitle: {
    fontSize: 11,
    fontWeight: '700',
    letterSpacing: 2,
    color: Colors.dark.textSecondary,
    marginBottom: 4,
  },
  logHeader: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
    marginBottom: 4,
  },
  clearBtn: {
    color: Colors.dark.danger,
    fontSize: 11,
    fontWeight: '700',
    letterSpacing: 1,
  },
  jobCard: {
    flexDirection: 'row',
    alignItems: 'center',
    justifyContent: 'space-between',
    padding: Spacing.three,
    borderRadius: 14,
    borderWidth: 1,
    borderColor: '#222',
    gap: 12,
  },
  jobLeft: {
    flex: 1,
    flexDirection: 'row',
    alignItems: 'flex-start',
    gap: 12,
  },
  jobIcon: { fontSize: 22, marginTop: 2 },
  jobInfo: { flex: 1 },
  jobLabel: {
    fontSize: 14,
    fontWeight: '700',
    color: Colors.dark.text,
  },
  jobDesc: {
    fontSize: 12,
    color: Colors.dark.textSecondary,
    marginTop: 2,
    lineHeight: 17,
  },
  jobLastRun: {
    fontSize: 10,
    color: Colors.dark.accent,
    marginTop: 4,
    fontFamily: 'monospace',
  },
  jobRunBtn: {
    width: 38,
    height: 38,
    borderRadius: 19,
    backgroundColor: Colors.dark.accent + '20',
    borderWidth: 1,
    borderColor: Colors.dark.accent + '60',
    alignItems: 'center',
    justifyContent: 'center',
  },
  jobRunBtnDisabled: {
    backgroundColor: '#1A1A1A',
    borderColor: '#333',
  },
  jobRunText: {
    color: Colors.dark.accent,
    fontWeight: '900',
    fontSize: 16,
  },
  jobRunTextDisabled: {
    color: '#444',
  },
  logContainer: {
    backgroundColor: '#050505',
    borderRadius: 12,
    borderWidth: 1,
    borderColor: '#1A1A1A',
    height: 200,
    padding: Spacing.two,
  },
  logScroll: { flex: 1 },
  logEmpty: {
    color: '#333',
    fontFamily: 'monospace',
    fontSize: 13,
  },
  logLine: {
    color: Colors.dark.accent,
    fontFamily: 'monospace',
    fontSize: 12,
    lineHeight: 18,
  },
});
