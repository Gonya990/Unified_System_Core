/**
 * UNIFIED CORE — Chat Screen (LIVE)
 * 
 * Real-time AI chat via Firestore Relay → igor-gaming AI Core.
 * No Telegram required. Firestore is the command bus.
 */
import { useState, useRef, useEffect, useCallback } from 'react';
import {
  StyleSheet,
  View,
  TextInput,
  FlatList,
  TouchableOpacity,
  KeyboardAvoidingView,
  Platform,
  Keyboard,
  ActivityIndicator,
  Animated,
} from 'react-native';
import { SafeAreaView } from 'react-native-safe-area-context';

import { ThemedText } from '@/components/themed-text';
import { ThemedView } from '@/components/themed-view';
import { Colors, Spacing } from '@/constants/theme';
import { useSystemStore, ChatMessage } from '@/store/systemStore';
import {
  sendChatMessage,
  subscribeToResponses,
  BackendResponse,
} from '@/services/firestoreRelay';

export default function ChatScreen() {
  const { messages, isTyping, addMessage, updateMessageStatus, setTyping } =
    useSystemStore();
  const [inputText, setInputText] = useState('');
  const flatListRef = useRef<FlatList>(null);
  const typingOpacity = useRef(new Animated.Value(0)).current;

  // ── Subscribe to backend responses ────────────────────────────────────────
  useEffect(() => {
    const unsub = subscribeToResponses((response: BackendResponse) => {
      setTyping(false);
      const agentMsg: ChatMessage = {
        id: `resp_${response.id ?? Date.now()}`,
        role: 'agent',
        text: response.text,
        timestamp: Date.now(),
        status: 'delivered',
      };
      addMessage(agentMsg);
    });

    return () => unsub();
  }, []);

  // ── Typing indicator animation ─────────────────────────────────────────────
  useEffect(() => {
    if (isTyping) {
      Animated.loop(
        Animated.sequence([
          Animated.timing(typingOpacity, { toValue: 1, duration: 600, useNativeDriver: true }),
          Animated.timing(typingOpacity, { toValue: 0.2, duration: 600, useNativeDriver: true }),
        ])
      ).start();
    } else {
      typingOpacity.setValue(0);
    }
  }, [isTyping]);

  // ── Send message ───────────────────────────────────────────────────────────
  const sendMessage = useCallback(async () => {
    const text = inputText.trim();
    if (!text) return;

    const localId = `user_${Date.now()}`;
    const userMsg: ChatMessage = {
      id: localId,
      role: 'user',
      text,
      timestamp: Date.now(),
      status: 'sending',
    };

    addMessage(userMsg);
    setInputText('');
    Keyboard.dismiss();
    setTyping(true);

    try {
      await sendChatMessage(text);
      updateMessageStatus(localId, 'delivered');
    } catch (err) {
      updateMessageStatus(localId, 'error');
      setTyping(false);
      const errMsg: ChatMessage = {
        id: `err_${Date.now()}`,
        role: 'system',
        text: '⚠️ Нет связи с igor-gaming. Проверь соединение.',
        timestamp: Date.now(),
        status: 'delivered',
      };
      addMessage(errMsg);
    }
  }, [inputText]);

  // ── Render message ─────────────────────────────────────────────────────────
  const renderMessage = ({ item }: { item: ChatMessage }) => {
    const isUser = item.role === 'user';
    const isSystem = item.role === 'system';
    const isSending = item.status === 'sending';
    const isError = item.status === 'error';

    return (
      <View style={[styles.messageRow, isUser ? styles.rowUser : styles.rowAgent]}>
        {!isUser && (
          <View style={styles.agentAvatar}>
            <ThemedText style={styles.agentAvatarText}>⚡</ThemedText>
          </View>
        )}
        <View
          style={[
            styles.bubble,
            isUser && styles.bubbleUser,
            isSystem && styles.bubbleSystem,
            !isUser && !isSystem && styles.bubbleAgent,
            isError && styles.bubbleError,
          ]}
        >
          <ThemedText
            style={[
              styles.bubbleText,
              isUser && styles.bubbleTextUser,
              isSystem && styles.bubbleTextSystem,
            ]}
          >
            {item.text}
          </ThemedText>
          {isSending && (
            <ActivityIndicator
              size="small"
              color={Colors.dark.accent}
              style={styles.sendingIndicator}
            />
          )}
        </View>
      </View>
    );
  };

  return (
    <KeyboardAvoidingView
      style={styles.container}
      behavior={Platform.OS === 'ios' ? 'padding' : undefined}
      keyboardVerticalOffset={Platform.OS === 'ios' ? 90 : 0}
    >
      <FlatList
        ref={flatListRef}
        data={messages}
        keyExtractor={(item) => item.id}
        renderItem={renderMessage}
        contentContainerStyle={styles.chatContainer}
        onContentSizeChange={() => flatListRef.current?.scrollToEnd({ animated: true })}
        onLayout={() => flatListRef.current?.scrollToEnd({ animated: true })}
        ListFooterComponent={
          isTyping ? (
            <Animated.View style={[styles.typingRow, { opacity: typingOpacity }]}>
              <View style={styles.agentAvatar}>
                <ThemedText style={styles.agentAvatarText}>⚡</ThemedText>
              </View>
              <View style={styles.typingBubble}>
                <ThemedText style={styles.typingText}>igor-gaming обрабатывает...</ThemedText>
              </View>
            </Animated.View>
          ) : null
        }
      />

      <View style={styles.inputContainer}>
        <TextInput
          style={styles.textInput}
          placeholder="Команда или запрос..."
          placeholderTextColor="#555"
          value={inputText}
          onChangeText={setInputText}
          multiline
          onSubmitEditing={sendMessage}
          returnKeyType="send"
        />
        <TouchableOpacity
          style={[styles.sendButton, !inputText.trim() && styles.sendButtonDisabled]}
          onPress={sendMessage}
          disabled={!inputText.trim()}
          activeOpacity={0.7}
        >
          <ThemedText style={styles.sendButtonText}>➔</ThemedText>
        </TouchableOpacity>
      </View>
    </KeyboardAvoidingView>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: Colors.dark.background,
  },
  chatContainer: {
    padding: Spacing.three,
    gap: Spacing.two,
    paddingBottom: Spacing.four,
  },
  messageRow: {
    flexDirection: 'row',
    marginVertical: 2,
    alignItems: 'flex-end',
    gap: 8,
  },
  rowUser: {
    justifyContent: 'flex-end',
  },
  rowAgent: {
    justifyContent: 'flex-start',
  },
  agentAvatar: {
    width: 28,
    height: 28,
    borderRadius: 14,
    backgroundColor: '#00ff9d15',
    borderWidth: 1,
    borderColor: '#00ff9d40',
    alignItems: 'center',
    justifyContent: 'center',
    marginBottom: 2,
  },
  agentAvatarText: {
    fontSize: 14,
  },
  bubble: {
    maxWidth: '78%',
    paddingHorizontal: Spacing.three,
    paddingVertical: Spacing.two + 2,
    borderRadius: 18,
    flexDirection: 'row',
    alignItems: 'center',
    gap: 8,
  },
  bubbleUser: {
    backgroundColor: Colors.dark.accent,
    borderBottomRightRadius: 4,
  },
  bubbleAgent: {
    backgroundColor: '#1A1A1A',
    borderBottomLeftRadius: 4,
    borderWidth: 1,
    borderColor: '#2A2A2A',
  },
  bubbleSystem: {
    backgroundColor: '#ff9900' + '20',
    borderWidth: 1,
    borderColor: '#ff990040',
    borderRadius: 12,
  },
  bubbleError: {
    backgroundColor: Colors.dark.danger + '20',
    borderColor: Colors.dark.danger + '40',
  },
  bubbleText: {
    fontSize: 15,
    lineHeight: 22,
    color: Colors.dark.text,
    flexShrink: 1,
  },
  bubbleTextUser: {
    color: '#000',
    fontWeight: '500',
  },
  bubbleTextSystem: {
    color: '#ff9900',
    fontSize: 13,
  },
  sendingIndicator: {
    marginLeft: 4,
  },
  typingRow: {
    flexDirection: 'row',
    alignItems: 'flex-end',
    gap: 8,
    paddingVertical: 4,
  },
  typingBubble: {
    backgroundColor: '#1A1A1A',
    paddingHorizontal: Spacing.three,
    paddingVertical: 10,
    borderRadius: 18,
    borderBottomLeftRadius: 4,
    borderWidth: 1,
    borderColor: '#00ff9d30',
  },
  typingText: {
    color: Colors.dark.accent,
    fontSize: 13,
    fontWeight: '600',
    letterSpacing: 0.5,
  },
  inputContainer: {
    flexDirection: 'row',
    padding: Spacing.three,
    paddingBottom: Platform.OS === 'ios' ? Spacing.five : Spacing.three,
    backgroundColor: '#111',
    borderTopWidth: 1,
    borderTopColor: '#1E1E1E',
    alignItems: 'center',
    gap: 10,
  },
  textInput: {
    flex: 1,
    backgroundColor: '#000',
    color: '#FFF',
    borderRadius: 22,
    paddingHorizontal: 18,
    paddingTop: 12,
    paddingBottom: 12,
    fontSize: 15,
    maxHeight: 120,
    borderWidth: 1,
    borderColor: '#2A2A2A',
    fontFamily: Platform.OS === 'ios' ? 'Menlo' : 'monospace',
  },
  sendButton: {
    backgroundColor: Colors.dark.accent,
    width: 46,
    height: 46,
    borderRadius: 23,
    alignItems: 'center',
    justifyContent: 'center',
    shadowColor: Colors.dark.accent,
    shadowOpacity: 0.4,
    shadowRadius: 8,
    shadowOffset: { width: 0, height: 0 },
  },
  sendButtonDisabled: {
    backgroundColor: '#222',
    shadowOpacity: 0,
  },
  sendButtonText: {
    color: '#000',
    fontSize: 20,
    fontWeight: 'bold',
  },
});
