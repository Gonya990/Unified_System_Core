/**
 * ============================================================================
 * SOVEREIGN COPYRIGHT & INTELLECTUAL PROPERTY NOTICE
 * ============================================================================
 * 
 * Copyright (c) 2026 Igor Goncharenko. All rights reserved.
 * 
 * This software, including its associated logic, architectures, and algorithms,
 * is the exclusive, sovereign property of Igor Goncharenko. It is strictly
 * prohibited to copy, modify, distribute, or use this code, in whole or in
 * part, without explicit, physically verified, written authorization.
 * 
 * Cryptographic signatures and access patterns are actively monitored.
 * Unauthorized access constitutes a violation of international cyber law.
 * ============================================================================
 */

const admin = require('firebase-admin');
const { GoogleGenAI } = require('@google/genai');

admin.initializeApp({
  projectId: "unified-core-agent-db"
});

const db = admin.firestore();
const ai = new GoogleGenAI({}); // Needs GEMINI_API_KEY environment variable

console.log("Agent Bridge is listening for new messages...");

db.collection('chats')
  .where('sender', '==', 'user')
  .where('processed', '==', false)
  .onSnapshot(snapshot => {
  snapshot.docChanges().forEach(async (change) => {
    if (change.type === 'added') {
      const doc = change.doc;
      const msg = doc.data();
      console.log(`New message: ${msg.text}`);
      
      // Mark as processed immediately so we don't process it twice
      await doc.ref.update({ processed: true });
      
      try {
        const response = await ai.models.generateContent({
            model: 'gemini-2.5-flash',
            contents: `You are the Unified Core Orchestrator. The user sent you a message from their mobile app. Respond helpfully.\nUser says: ${msg.text}`,
        });

        await db.collection('chats').add({
          text: response.text,
          sender: 'agent',
          createdAt: admin.firestore.FieldValue.serverTimestamp()
        });
        console.log("Agent replied.");
      } catch(err) {
        console.error("Error generating response:", err);
      }
    }
  });
});
