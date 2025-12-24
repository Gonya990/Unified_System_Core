# Browser Skills

> **Location:** `.agent/skills/browser/`  
> **CLI:** `ndc` (requires running daemon)

## Quick Reference

### Navigation

```bash
ndc goto "https://example.com"    # Open URL
ndc url                           # Get current URL
ndc title                         # Get page title
```

### Interaction

```bash
ndc click "Button Text"           # Click by visible text
ndc clicksel "button.submit"      # Click by CSS selector
ndc fill "input[name=q]" "text"   # Fill input field
ndc type "input" "text" 50        # Type with 50ms delay
ndc scroll down 500               # Scroll down 500px
```

### Content

```bash
ndc screenshot /tmp/s.png         # Save screenshot
ndc text ".header"                # Get element text
ndc html                          # Get page HTML
ndc js "document.title"           # Execute JavaScript
```

### Tabs

```bash
ndc tabs                          # List tabs
ndc newtab "https://..."          # New tab with URL
ndc switchtab 1                   # Switch to tab index 1
ndc closetab 0                    # Close tab index 0
```

### Waiting

```bash
ndc wait ".loaded" 10             # Wait for element (10s timeout)
```

### Daemon

```bash
ndc status                        # Check daemon status
ndc stop                          # Stop daemon
```

## Common Flows

### Google Search

```bash
ndc goto "https://google.com"
ndc fill "textarea[name=q]" "search query"
ndc click "Google Search"
ndc wait "div#search"
ndc screenshot
```

### Form Login

```bash
ndc goto "https://site.com/login"
ndc fill "input[name=email]" "user@example.com"
ndc fill "input[name=password]" "password"
ndc click "Sign In"
ndc wait ".dashboard"
```

## Setup

```bash
# 1. Start Chrome with debugging
./start_chrome.sh

# 2. Start daemon
./start_daemon.sh

# 3. Use ndc commands
ndc status
```

## Path

```
/Users/macbook/Documents/Unified_System/Agent_Context/Knowledge_Base/Sessions/nodriver_implementation/ndc
```
