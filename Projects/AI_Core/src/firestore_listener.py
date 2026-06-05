import asyncio
import logging
import threading
import time

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger("FirestoreListener")

# Local AI Core imports
from config_manager import ConfigManager
from firestore_db import get_db
from inference_client import InferenceClient

# Initialize Core Components
config = ConfigManager()
inference = InferenceClient(config)
db = get_db()

# Ensure Firestore is actually used
if not db.use_firestore:
    logger.error("Firestore is not enabled or credentials are missing.")
    logger.error("Cannot start Firestore Listener.")
    exit(1)


def process_message_async(doc_id, data):
    async def _process():
        try:
            user_text = data.get('text', '')
            user_id = data.get('user_id', config.get("ADMIN_ID", "admin"))

            logger.info(f"[iOS Listener] Processing message from {user_id}: {user_text}")

            # Update Firestore history for the user (Memory)
            db.add_message(user_id, "user", user_text)
            history = db.get_history(user_id, limit=10)

            # Generate response via AI Core Inference
            # Convert history to InferenceClient format if needed
            # InferenceClient usually maintains its own history or takes context
            context = "\n".join([f"{msg['role']}: {msg['content']}" for msg in history])

            prompt = f"Conversation History:\n{context}\n\nRespond to the last message."

            logger.info("Generating response...")
            response_text = await inference.complete(prompt)

            # Save AI response to Memory
            db.add_message(user_id, "assistant", response_text)

            # Send response back to iOS App via Firestore
            from google.cloud import firestore
            db.db.collection('chats').add({
                'text': response_text,
                'sender': 'agent',
                'createdAt': firestore.SERVER_TIMESTAMP,
                'replyTo': doc_id,
                'user_id': user_id
            })

            logger.info(f"[iOS Listener] Responded to {user_id}")

        except Exception as e:
            logger.error(f"[iOS Listener] Error processing message {doc_id}: {e}")

    # Run in a new event loop for this thread
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(_process())
    loop.close()


def on_snapshot(col_snapshot, changes, read_time):
    for change in changes:
        if change.type.name == 'ADDED':
            doc = change.document
            data = doc.to_dict()

            # Only process if not already processed
            if data.get('sender') == 'user' and not data.get('processed', False):
                logger.info(f"Detected new message: {doc.id}")

                # Mark as processed immediately to prevent duplicate processing
                doc.reference.update({'processed': True})

                # Spawn a thread to handle the inference so we don't block the listener
                threading.Thread(target=process_message_async, args=(doc.id, data)).start()


def main():
    logger.info("Starting iOS App Firestore Listener...")

    # Watch the chats collection
    col_query = db.db.collection('chats') \
        .where('sender', '==', 'user') \
        .where('processed', '==', False)

    col_watch = col_query.on_snapshot(on_snapshot)

    logger.info("Listening for new iOS messages in real-time...")

    try:
        # Keep the main thread alive
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        logger.info("Shutting down Firestore Listener.")

if __name__ == '__main__':
    main()
