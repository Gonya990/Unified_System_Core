from google.cloud import firestore
try:
    db = firestore.Client(project='unified-core-agent-db')
    doc = db.collection('system_status').document('current').get()
    print(doc.to_dict())
except Exception as e:
    print(e)
