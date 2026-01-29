#!/usr/bin/env python3
"""
OpenAI MCP Server (Updated for OpenAI v2 API)
MCP сервер OpenAI (обновлен для OpenAI v2 API)
"""

import json
import os
from http.server import BaseHTTPRequestHandler, HTTPServer

from dotenv import load_dotenv
from openai import OpenAI

# Load environment
load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

class MCPHandler(BaseHTTPRequestHandler):
    def do_POST(self):
        content_length = int(self.headers.get('Content-Length', 0))
        body = self.rfile.read(content_length)

        try:
            request = json.loads(body.decode('utf-8'))
        except Exception:
            request = {}

        method = request.get('method', 'unknown')

        if method == 'chat':
            response = self.handle_chat(request.get('params', {}))
        elif method == 'models':
            response = self.handle_models()
        elif method == 'test':
            response = {'status': 'success', 'message': 'Server is running'}
        else:
            response = {'error': f'Unknown method: {method}'}

        self.send_response(200)
        self.send_header('Content-Type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()
        self.wfile.write(json.dumps(response, ensure_ascii=False).encode('utf-8'))

    def handle_chat(self, params):
        try:
            message = params.get('message', '')
            model = params.get('model', 'gpt-4o-mini')

            completion = client.chat.completions.create(
                model=model,
                messages=[{"role": "user", "content": message}]
            )

            return {
                'status': 'success',
                'response': completion.choices[0].message.content,
                'model': completion.model,
                'tokens': {
                    'prompt': completion.usage.prompt_tokens,
                    'completion': completion.usage.completion_tokens,
                    'total': completion.usage.total_tokens
                }
            }
        except Exception as e:
            return {'status': 'error', 'error': str(e)}

    def handle_models(self):
        try:
            models = client.models.list()
            model_list = [model.id for model in models.data]
            return {
                'status': 'success',
                'models': model_list,
                'count': len(model_list)
            }
        except Exception as e:
            return {'status': 'error', 'error': str(e)}

    def log_message(self, format, *args):
        # Suppress default logging
        pass

if __name__ == '__main__':
    print("╔══════════════════════════════════════════════════════════════╗")
    print("║   OpenAI MCP Server v2 | MCP Сервер OpenAI v2               ║")
    print("╚══════════════════════════════════════════════════════════════╝")
    print()

    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        print("⚠️  WARNING: OPENAI_API_KEY not set in .env file")
        print("⚠️  ПРЕДУПРЕЖДЕНИЕ: OPENAI_API_KEY не установлен в файле .env")
        exit(1)
    else:
        print(f"✅ API key loaded | API ключ загружен ({len(api_key)} chars)")

    # Test connection
    print("🔍 Testing OpenAI connection | Тестирование подключения к OpenAI...")
    try:
        models = client.models.list()
        print(f"✅ Connected! Found {len(models.data)} models | Подключено! Найдено {len(models.data)} моделей")
    except Exception as e:
        print(f"❌ Connection failed | Ошибка подключения: {str(e)}")
        print()
        print("Common issues | Частые проблемы:")
        print("  1. Invalid API key | Неверный API ключ")
        print("  2. No billing method | Не добавлен способ оплаты")
        print("  3. Key not activated yet | Ключ еще не активирован")
        print()
        exit(1)

    print()
    print("🚀 Starting server on http://127.0.0.1:8766")
    print("🚀 Запуск сервера на http://127.0.0.1:8766")
    print()
    print("Press Ctrl+C to stop | Нажмите Ctrl+C для остановки")
    print()

    server = HTTPServer(('127.0.0.1', 8766), MCPHandler)

    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\n🛑 Server stopped | Сервер остановлен")
