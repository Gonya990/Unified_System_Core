import json
import re

def categorize(name, description, topics):
    text = f"{name} {description or ''} {' '.join(topics)}".lower()
    
    categories = {
        "AI/Agents": ["agent", "ai", "llm", "gpt", "rag", "openai", "claude", "chatbot", "mcp", "machine-learning", "multi-agent", "embeddings", "vector-search", "neural", "antigravity", "codex", "genai", "generative-ai"],
        "DevOps/Infra": ["devops", "kubernetes", "k8s", "docker", "terraform", "ansible", "monitoring", "observability", "cloud", "ci", "cd", "paas", "gitops", "infrastructure", "sre", "prometheus", "grafana", "nixos", "nix", "jenkins", "argocd", "helm", "serverless"],
        "Security/Privacy": ["security", "privacy", "encryption", "e2ee", "vulnerability", "penetration-testing", "hacking", "infosec", "auth", "identity", "zero-trust", "honeypot", "exploit", "cve", "firewall", "leak", "phishing", "malicious", "pentest"],
        "Development Tools": ["cli", "developer-tools", "editor", "framework", "api", "npm", "rust", "python", "javascript", "typescript", "testing", "documentation", "debugger", "linter", "formatter", "ide", "vscode", "neovim", "git", "bash", "shell", "regex"],
        "Knowledge Management/Notes": ["note-taking", "knowledge-base", "notion", "obsidian", "pkm", "wiki", "notes-app", "zettelkasten", "notebook", "evernote"],
        "Data/Databases": ["database", "vector-database", "sql", "nosql", "analytics", "data-engineering", "etl", "elasticsearch", "clickhouse", "mongodb", "postgres", "redis", "warehouse", "olap", "bigdata"],
        "Multimedia/Social": ["video", "photo", "music", "image", "spotify", "youtube", "iptv", "social-media", "streaming", "restoration", "upscaling", "stable-diffusion", "inpainting", "gallery"],
        "Productivity/Self-Hosted": ["productivity", "self-hosted", "dashboard", "crm", "project-management", "home-server", "homelab", "automation", "erp", "cms", "ecommerce", "accounting", "invoicing", "budgeting", "kanban", "task-manager"],
        "Education/Resources": ["awesome", "awesome-list", "tutorial", "roadmap", "course", "interview", "learning", "certification", "cheatsheet", "handbook", "books", "reference"],
        "Networking/Communication": ["vpn", "wireguard", "ssh", "sip", "voip", "whatsapp", "discord", "matrix", "bridge", "tunnel", "networking", "http", "proxy", "nat", "tailscale"]
    }
    
    matched_cats = []
    for cat, keywords in categories.items():
        if any(re.search(r'\b' + re.escape(k) + r'\b', text) for k in keywords):
            matched_cats.append(cat)
            
    if not matched_cats:
        return "Miscellaneous"
    # Return the first match or prioritize
    return matched_cats[0]

output = {}

with open('/home/kosta/.local/share/opencode/tool-output/tool_bb7c545e90014PA4uhNYstRQ2T', 'r') as f:
    lines = f.readlines()
    for line in lines[6:]:  # Skip headers
        try:
            repo = json.loads(line)
            url = repo.get('url')
            desc = repo.get('description') or "No description provided."
            # Trim description to 1 sentence
            desc = desc.split('. ')[0].split('? ')[0].split('! ')[0]
            if not desc.endswith(('.', '?', '!')):
                desc += '.'
            
            topics = repo.get('topics', [])
            cat = categorize(repo.get('name'), repo.get('description'), topics)
            
            if cat not in output:
                output[cat] = []
            
            tags = ", ".join(topics) if topics else "no tags"
            entry = f"[{url}]({desc}) > {tags}"
            output[cat].append(entry)
        except:
            continue

for cat in sorted(output.keys()):
    print(f"## {cat}")
    for entry in output[cat]:
        print(entry)
    print()
