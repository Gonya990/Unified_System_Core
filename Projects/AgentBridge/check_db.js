const admin = require('firebase-admin');
admin.initializeApp({ projectId: 'unified-core-agent-db' });
const db = admin.firestore();
db.collection('chats').get().then(snap => {
  console.log('--- CHATS ---');
  if (snap.empty) {
    console.log('No messages in the database.');
  }
  snap.forEach(doc => console.log(doc.id, doc.data()));
  console.log('-------------');
  process.exit(0);
}).catch(e => {
  console.error('Error:', e);
  process.exit(1);
});
