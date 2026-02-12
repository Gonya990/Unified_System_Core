
from instagrapi import Client

session_id = "3067810412%3AgGUbeJqEAlSX38%3A3%3AAYgICnRRIlDpFXEXsFjjFeZGWgKQuG7nARTbygsm_Q"

print("🕵️ Testing Simple Session ID Login...")
cl = Client()
try:
    cl.login_by_sessionid(session_id)
    print(f"✅ Logged in! User ID: {cl.user_id}")
    print(f"🎉 Account: {cl.username}")

    # Save properly for future use
    cl.dump_settings('/home/gonya/Unified_System_Core/Projects/Content_Factory/src/uploaders/.credentials/insta_session.json')
    print("💾 Settings saved to .credentials/")

except Exception as e:
    print(f"❌ Failed: {e}")
