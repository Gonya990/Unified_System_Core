# Ideal Factory Multi-User Guide

This factory supports multiple isolated user accounts. Each user has their own credentials and video storage.

## How to Add a New User

1. **Create User Directory**:
   ```bash
   mkdir -p users/NEW_USER/outputs
   ```

2. **Setup Credentials**:
   Copy `.env` from the root or a template to `users/NEW_USER/.env`.
   Edit the file and update:
   - `INSTAGRAM_SESSION_ID`: Get this from your browser cookies (sessionid).
   - `OPENAI_API_KEY`: Your personal key.
   - `PEXELS_API_KEY`: Your personal key.

3. **Run for User**:
   ```bash
   ./venv/bin/python3 factory_hub.py --user NEW_USER
   ```

4. **Automate**:
   Add a line to `crontab -e`:
   `0 10 * * * cd /root/factory && /root/factory/venv/bin/python3 factory_hub.py --user NEW_USER >> /root/factory/users/NEW_USER/run.log 2>&1`

## Directory Structure
- `factory_hub.py`: Main orchestrator.
- `users/<username>/.env`: Private credentials.
- `users/<username>/outputs/`: Generated videos.
- `users/<username>/factory_run.log`: Execution logs.
