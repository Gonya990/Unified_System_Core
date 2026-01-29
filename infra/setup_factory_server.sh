#!/bin/bash
# Server Setup Script for Ideal Factory

echo "🚀 Installing system dependencies..."
apt-get update && apt-get install -y ffmpeg rsync python3-venv

echo "📁 Creating directory structure..."
mkdir -p /root/factory/assets
mkdir -p /root/factory/users/template/outputs

echo "🐍 Setting up virtual environment..."
cd /root/factory
python3 -m venv venv
./venv/bin/pip install requests python-dotenv openai instagrapi moviepy pillow pydantic numpy

echo "🩹 Applying instagrapi monkeypatch..."
python3 -c "
path = '/root/factory/venv/lib/python3.13/site-packages/instagrapi/types.py'
with open(path, 'r') as f: content = f.read()
content = content.replace('from typing import Dict, List, Optional, Union', 'from typing import Any, Dict, List, Optional, Union')
content = content.replace('reusable_text_info: Optional[dict] = None', 'reusable_text_info: Optional[Any] = None')
with open(path, 'w') as f: f.write(content)
"

echo "✅ Server setup complete!"
