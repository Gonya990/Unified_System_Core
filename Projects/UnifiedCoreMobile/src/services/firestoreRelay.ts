/**
 * Firestore Relay Service — Command Bus
 * 
 * Architecture: Mobile → Firestore → igor-gaming (AI_Core listener) → Firestore → Mobile
 * 
 * Collections:
 *   mobile_commands/{id}   — commands from mobile to backend
 *   mobile_responses/{id}  — responses from backend to mobile
 *   ha_commands/{id}       — Home Assistant control commands
 *   system_status          — live system state from igor-gaming
 */
import {
  collection,
  doc,
  addDoc,
  onSnapshot,
  query,
  orderBy,
  limit,
  serverTimestamp,
  Timestamp,
  updateDoc,
} from 'firebase/firestore';
import { db, deviceUserId } from '@/firebaseConfig';

// ─── Types ────────────────────────────────────────────────────────────────────

export type CommandType =
  | 'chat'          // AI conversation
  | 'ha_control'    // Home Assistant action
  | 'system_cmd'    // System command (restart, sync, etc.)
  | 'scrubber'      // Data scrubbing request
  | 'status_check'; // Request system status

export interface MobileCommand {
  id?: string;
  type: CommandType;
  payload: Record<string, unknown>;
  sessionId: string;
  deviceId: string | null;
  timestamp?: Timestamp;
  status: 'pending' | 'processing' | 'done' | 'error';
}

export interface BackendResponse {
  id?: string;
  commandId: string;
  text: string;
  type: 'text' | 'ha_result' | 'system_result' | 'scrubber_result' | 'error';
  timestamp?: Timestamp;
  metadata?: Record<string, unknown>;
}

export interface SystemStatus {
  ha_online: boolean;
  ai_core_alive: boolean;
  services: Record<string, 'online' | 'offline' | 'warning'>;
  last_update: Timestamp | null;
  uptime_seconds: number;
  active_agents: string[];
}

// ─── Session ──────────────────────────────────────────────────────────────────

const SESSION_ID = `mobile_${Date.now()}_${Math.random().toString(36).slice(2, 8)}`;

export function getSessionId() {
  return SESSION_ID;
}

// ─── Send Command ──────────────────────────────────────────────────────────────

/**
 * Send a command from mobile to the backend via Firestore relay.
 * Returns the command document ID (used to match the response).
 */
export async function sendCommand(
  type: CommandType,
  payload: Record<string, unknown>
): Promise<string> {
  const command: Omit<MobileCommand, 'id'> = {
    type,
    payload,
    sessionId: SESSION_ID,
    deviceId: deviceUserId,
    timestamp: serverTimestamp() as Timestamp,
    status: 'pending',
  };

  const ref = await addDoc(collection(db, 'mobile_commands'), command);
  return ref.id;
}

/**
 * Send a chat message to AI Core.
 */
export async function sendChatMessage(text: string): Promise<string> {
  return sendCommand('chat', { message: text });
}

/**
 * Send a Home Assistant control command.
 * @param action - 'turn_on' | 'turn_off' | 'toggle' | 'set_temperature' | 'activate_scene'
 * @param entityId - HA entity_id
 * @param extra - extra params (e.g. temperature)
 */
export async function sendHACommand(
  action: string,
  entityId: string,
  extra?: Record<string, unknown>
): Promise<string> {
  return sendCommand('ha_control', { action, entity_id: entityId, ...extra });
}

/**
 * Send a system command (restart service, sync github, etc.)
 */
export async function sendSystemCommand(cmd: string): Promise<string> {
  return sendCommand('system_cmd', { command: cmd });
}

/**
 * Request a system status refresh from igor-gaming.
 */
export async function requestStatusRefresh(): Promise<string> {
  return sendCommand('status_check', { session: SESSION_ID });
}

/**
 * Run a Scrubber analysis pass.
 */
export async function runScrubber(target: string, options?: Record<string, unknown>): Promise<string> {
  return sendCommand('scrubber', { target, options: options ?? {} });
}

// ─── Listen for Responses ─────────────────────────────────────────────────────

/**
 * Subscribe to backend responses for this session.
 * Calls onResponse for each new response from igor-gaming.
 * Returns unsubscribe function.
 */
export function subscribeToResponses(
  onResponse: (response: BackendResponse) => void
): () => void {
  const q = query(
    collection(db, 'mobile_responses'),
    orderBy('timestamp', 'desc'),
    limit(50)
  );

  const seen = new Set<string>();

  const unsub = onSnapshot(q, (snapshot) => {
    snapshot.docChanges().forEach((change) => {
      if (change.type === 'added') {
        const data = change.doc.data() as BackendResponse;
        const id = change.doc.id;
        // Only process new responses for our session, avoid duplicates
        if (!seen.has(id) && data.commandId) {
          seen.add(id);
          onResponse({ ...data, id });
        }
      }
    });
  });

  return unsub;
}

/**
 * Subscribe to live system status from igor-gaming.
 * igor-gaming writes to Firestore doc 'system_status/current' periodically.
 * Returns unsubscribe function.
 */
export function subscribeToSystemStatus(
  onStatus: (status: SystemStatus) => void
): () => void {
  const docRef = doc(db, 'system_status', 'current');

  const unsub = onSnapshot(docRef, (snap) => {
    if (snap.exists()) {
      onStatus(snap.data() as SystemStatus);
    }
  });

  return unsub;
}

/**
 * Subscribe to Home Assistant entity states.
 * igor-gaming writes HA states to Firestore 'ha_states/{entity_id}'.
 */
export function subscribeToHAStates(
  onStates: (states: Array<{ entity_id: string; state: string; attributes: Record<string, unknown> }>) => void
): () => void {
  const q = query(collection(db, 'ha_states'), limit(200));

  const unsub = onSnapshot(q, (snapshot) => {
    const states = snapshot.docs.map((d) => ({
      entity_id: d.id,
      ...d.data(),
    })) as Array<{ entity_id: string; state: string; attributes: Record<string, unknown> }>;
    onStates(states);
  });

  return unsub;
}
