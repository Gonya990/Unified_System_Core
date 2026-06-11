/**
 * SystemStore — Global State (Zustand)
 * Single source of truth for UnifiedCoreMobile.
 * Tracks: chat, services, smart home devices, system status.
 */
import { create } from 'zustand';

// ─── Types ────────────────────────────────────────────────────────────────────

export type MessageRole = 'user' | 'agent' | 'system';

export interface ChatMessage {
  id: string;
  role: MessageRole;
  text: string;
  timestamp: number;
  status?: 'sending' | 'delivered' | 'error';
}

export type ServiceStatus = 'online' | 'offline' | 'warning' | 'unknown';

export interface ServiceInfo {
  id: string;
  name: string;
  status: ServiceStatus;
  lastChecked?: number;
  detail?: string;
}

export type HADomain = 'light' | 'switch' | 'climate' | 'sensor' | 'binary_sensor' | 'script' | 'scene' | 'media_player';

export interface HAEntity {
  entity_id: string;
  friendly_name: string;
  state: string;
  domain: HADomain;
  attributes?: Record<string, unknown>;
  lastUpdated?: number;
}

export type SystemMode = 'normal' | 'scrubber' | 'emergency';

// ─── Store Interface ──────────────────────────────────────────────────────────

interface SystemState {
  // ── Connection
  connected: boolean;
  backendHost: string;
  setConnected: (v: boolean) => void;

  // ── System Mode (Normal / Scrubber / Emergency)
  mode: SystemMode;
  setMode: (m: SystemMode) => void;

  // ── Chat
  messages: ChatMessage[];
  isTyping: boolean;
  addMessage: (msg: ChatMessage) => void;
  updateMessageStatus: (id: string, status: ChatMessage['status']) => void;
  setTyping: (v: boolean) => void;
  clearChat: () => void;

  // ── Services
  services: ServiceInfo[];
  setServices: (s: ServiceInfo[]) => void;
  updateService: (id: string, update: Partial<ServiceInfo>) => void;

  // ── Smart Home
  haEntities: HAEntity[];
  haOnline: boolean;
  setHAEntities: (entities: HAEntity[]) => void;
  setHAOnline: (v: boolean) => void;
  updateHAEntity: (entity_id: string, state: string, attributes?: Record<string, unknown>) => void;

  // ── Scrubber
  scrubberActive: boolean;
  scrubberLogs: string[];
  setScrubberActive: (v: boolean) => void;
  addScrubberLog: (log: string) => void;
  clearScrubberLogs: () => void;
}

// ─── Store Implementation ─────────────────────────────────────────────────────

export const useSystemStore = create<SystemState>((set) => ({
  // ── Connection
  connected: false,
  backendHost: 'igor-gaming',
  setConnected: (v) => set({ connected: v }),

  // ── Mode
  mode: 'normal',
  setMode: (m) => set({ mode: m }),

  // ── Chat
  messages: [
    {
      id: 'boot',
      role: 'agent',
      text: '⚡ UNIFIED CORE ONLINE\nПодключаюсь к igor-gaming...',
      timestamp: Date.now(),
      status: 'delivered',
    },
  ],
  isTyping: false,
  addMessage: (msg) =>
    set((s) => ({ messages: [...s.messages, msg] })),
  updateMessageStatus: (id, status) =>
    set((s) => ({
      messages: s.messages.map((m) => (m.id === id ? { ...m, status } : m)),
    })),
  setTyping: (v) => set({ isTyping: v }),
  clearChat: () =>
    set({
      messages: [
        {
          id: 'boot',
          role: 'agent',
          text: '⚡ Чат очищен. Система готова.',
          timestamp: Date.now(),
          status: 'delivered',
        },
      ],
    }),

  // ── Services
  services: [
    { id: 'ha',       name: 'Home Assistant', status: 'unknown' },
    { id: 'n8n',      name: 'N8N',            status: 'unknown' },
    { id: 'docker',   name: 'Docker Node',    status: 'unknown' },
    { id: 'github',   name: 'GitHub Sync',    status: 'unknown' },
    { id: 'firebase', name: 'Firestore DB',   status: 'online'  },
    { id: 'ai_core',  name: 'AI Core',        status: 'unknown' },
    { id: 'bybit',    name: 'Bybit Bot',      status: 'unknown' },
  ],
  setServices: (services) => set({ services }),
  updateService: (id, update) =>
    set((s) => ({
      services: s.services.map((srv) =>
        srv.id === id ? { ...srv, ...update, lastChecked: Date.now() } : srv
      ),
    })),

  // ── Smart Home
  haEntities: [],
  haOnline: false,
  setHAEntities: (haEntities) => set({ haEntities }),
  setHAOnline: (v) => set({ haOnline: v }),
  updateHAEntity: (entity_id, state, attributes) =>
    set((s) => ({
      haEntities: s.haEntities.map((e) =>
        e.entity_id === entity_id
          ? { ...e, state, attributes: attributes ?? e.attributes, lastUpdated: Date.now() }
          : e
      ),
    })),

  // ── Scrubber
  scrubberActive: false,
  scrubberLogs: [],
  setScrubberActive: (v) => set({ scrubberActive: v }),
  addScrubberLog: (log) =>
    set((s) => ({
      scrubberLogs: [`[${new Date().toISOString()}] ${log}`, ...s.scrubberLogs].slice(0, 500),
    })),
  clearScrubberLogs: () => set({ scrubberLogs: [] }),
}));
