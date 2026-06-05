const admin = require('firebase-admin');
admin.initializeApp({ projectId: 'unified-core-agent-db' });
const db = admin.firestore();
async function run() {
  console.log('📱 Phone: Sending message to Agent...');
  const docRef = await db.collection('chats').add({
    text: 'Hello from the simulated phone! How are you?',
    sender: 'user',
    processed: false,
    createdAt: admin.firestore.FieldValue.serverTimestamp()
  });
  console.log('📱 Phone: Message sent! Waiting for reply...');
  
  // Listen for agent replies
  db.collection('chats').where('sender', '==', 'agent').onSnapshot(snap => {
    snap.docChanges().forEach(change => {
      if (change.type === 'added') {
        console.log('\n🤖 Agent Reply:', change.doc.data().text);
        process.exit(0);
      }
    });
  });
}
run();
