#!/usr/bin/env python3
import os
import sys
import argparse
from pathlib import Path
from dotenv import load_dotenv

# Setup paths
ROOT_DIR = Path(__file__).parent.resolve()
sys.path.append(str(ROOT_DIR))

def run_factory_for_user(username: str):
    user_dir = ROOT_DIR / "users" / username
    if not user_dir.exists():
        print(f"❌ Error: User '{username}' directory not found in {ROOT_DIR}/users/")
        return

    user_env = user_dir / ".env"
    if not user_env.exists():
        print(f"⚠️ Warning: User '{username}' has no .env file. Using global .env.")
        load_dotenv(ROOT_DIR / ".env", override=True)
    else:
        print(f"🔑 Loading credentials for user: {username}")
        load_dotenv(user_env, override=True)

    # Prepare user-specific outputs
    user_output_dir = user_dir / "outputs"
    user_output_dir.mkdir(exist_ok=True, parents=True)
    
    # Update environment to point to user outputs
    os.environ["OUTPUT_DIR_OVERRIDE"] = str(user_output_dir)

    # Import and run the scheduler
    from factory_scheduler import run_weekly_production
    print(f"🏭 --- Starting Factory Hub for User: {username} ---")
    run_weekly_production()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Ideal Factory Hub Manager")
    parser.add_argument("--user", type=str, required=True, help="Username to run the factory for")
    args = parser.parse_args()

    run_factory_for_user(args.user)
