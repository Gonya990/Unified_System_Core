import { useState, useRef } from 'react';
import { StyleSheet, View, TextInput, FlatList, TouchableOpacity, KeyboardAvoidingView, Platform, Keyboard } from 'react-native';
import { SafeAreaView } from 'react-native-safe-area-context';

import { ThemedText } from '@/components/themed-text';
import { ThemedView } from '@/components/themed-view';
import { Colors, Spacing } from '@/constants/theme';

type Message = {
  id: string;
  role: 'user' | 'agent';
  text: string;
  timestamp: number;
};

export default function ChatScreen() {
  const [messages, setMessages] = useState<Message[]>([
    {
      id: '1',
      role: 'agent',
      text: 'Привет! Я Unified Core. Готов управлять системой и серверами.',
      timestamp: Date.now(),
    }
  ]);
  const [inputText, setInputText] = useState('');
  const flatListRef = useRef<FlatList>(null);

  const sendMessage = () => {
    if (!inputText.trim()) return;

    const newUserMsg: Message = {
      id: Date.now().toString(),
      role: 'user',
      text: inputText.trim(),
      timestamp: Date.now(),
    };

    setMessages((prev) => [...prev, newUserMsg]);
    setInputText('');
    Keyboard.dismiss();

    // Mock agent response
    setTimeout(() => {
      const agentMsg: Message = {
        id: (Date.now() + 1).toString(),
        role: 'agent',
        text: 'Принято. Обрабатываю запрос...',
        timestamp: Date.now(),
      };
      setMessages((prev) => [...prev, agentMsg]);
    }, 1000);
  };

  const renderMessage = ({ item }: { item: Message }) => {
    const isUser = item.role === 'user';
    return (
      <View style={[styles.messageRow, isUser ? styles.messageRowUser : styles.messageRowAgent]}>
        <View style={[styles.messageBubble, isUser ? styles.messageBubbleUser : styles.messageBubbleAgent]}>
          <ThemedText style={[styles.messageText, isUser ? styles.messageTextUser : styles.messageTextAgent]}>
            {item.text}
          </ThemedText>
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
      />

      <View style={styles.inputContainer}>
        <TextInput
          style={styles.textInput}
          placeholder="Написать команду..."
          placeholderTextColor="#888"
          value={inputText}
          onChangeText={setInputText}
          multiline
        />
        <TouchableOpacity style={styles.sendButton} onPress={sendMessage} disabled={!inputText.trim()}>
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
    padding: Spacing.four,
    gap: Spacing.three,
  },
  messageRow: {
    flexDirection: 'row',
    marginVertical: 4,
  },
  messageRowUser: {
    justifyContent: 'flex-end',
  },
  messageRowAgent: {
    justifyContent: 'flex-start',
  },
  messageBubble: {
    maxWidth: '80%',
    padding: 12,
    borderRadius: 20,
  },
  messageBubbleUser: {
    backgroundColor: Colors.dark.accent,
    borderBottomRightRadius: 4,
  },
  messageBubbleAgent: {
    backgroundColor: '#2A2A2A',
    borderBottomLeftRadius: 4,
    borderWidth: 1,
    borderColor: '#333',
  },
  messageText: {
    fontSize: 16,
    lineHeight: 22,
  },
  messageTextUser: {
    color: '#000', // Assuming accent is bright (like neon green)
    fontWeight: '500',
  },
  messageTextAgent: {
    color: Colors.dark.text,
  },
  inputContainer: {
    flexDirection: 'row',
    padding: Spacing.four,
    paddingBottom: Platform.OS === 'ios' ? Spacing.five : Spacing.four,
    backgroundColor: '#1A1A1A',
    borderTopWidth: 1,
    borderTopColor: '#333',
    alignItems: 'center',
  },
  textInput: {
    flex: 1,
    backgroundColor: '#000',
    color: '#FFF',
    borderRadius: 20,
    paddingHorizontal: 16,
    paddingTop: 12,
    paddingBottom: 12,
    fontSize: 16,
    maxHeight: 100,
    borderWidth: 1,
    borderColor: '#333',
  },
  sendButton: {
    marginLeft: 12,
    backgroundColor: Colors.dark.accent,
    width: 44,
    height: 44,
    borderRadius: 22,
    alignItems: 'center',
    justifyContent: 'center',
  },
  sendButtonText: {
    color: '#000',
    fontSize: 20,
    fontWeight: 'bold',
  },
});
