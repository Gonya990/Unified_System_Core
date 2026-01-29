# Make.com Setup Guide: WhatsApp Digital Assistant

Follow these steps to connect your WhatsApp Business account to your
Unified Core Bridge Server.

## 1. Meta Developer Portal

Before starting in Make.com, ensure you have:

1. **WhatsApp Business API** configured in your Meta App.
2. Your **Phone Number ID**.
3. Your **WhatsApp Business Account ID**.
4. Created a **Permanent System User Access Token** (Essential for long-term use).

---

## 2. Make.com Scenario Setup

### Step 2.1: Trigger - WhatsApp Business Cloud

1. Create a new scenario and add the **WhatsApp Business Cloud** module.
2. Choose current trigger: **Watch Events**.
3. Create a connection using your Phone Number ID, Account ID, and System User Token.
4. Copy the **Webhook URL** and **Verify Token** provided by Make.com.
5. Go back to Meta Portal -> WhatsApp -> Configuration and paste these values.
6. **Subscribe** to the `messages` field in the webhook settings.

### Step 2.2: Forwarding to Bridge Server (HTTP)

1. Add the **HTTP** module: **Make a request**.
2. **URL**: `http://YOUR_SERVER_IP:8090/webhook/lead`
3. **Method**: `POST`.
4. **Headers**:
    - `Authorization`: `Bearer unified-secret-2026`
5. **Body Type**: `Raw`.
6. **Content Type**: `JSON (application/json)`.
7. **Request Content**:

    ```json
    {
      "name": "{{contacts[].profile.name}}",
      "phone": "{{messages[].from}}",
      "message": "{{messages[].text.body}}",
      "timestamp": "{{messages[].timestamp}}",
      "message_id": "{{messages[].id}}"
    }
    ```

### Step 2.3: Storage - Google Sheets

1. Add the **Google Sheets** module: **Add a Row**.
2. Select your spreadsheet (e.g., "AI Leads CRM").
3. Map the columns to the data from the WhatsApp module.

---

## 3. Testing

1. Click **Run once** in Make.com.
2. Send a test message to your WhatsApp Business number.
3. Check the `bridge_server.py` logs (you should see `"Received lead from..."`).
4. Verify the analysis returned by the AI is visible in Make.com execution logs.
