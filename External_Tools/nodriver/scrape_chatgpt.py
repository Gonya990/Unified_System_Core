import json
import logging
import os
import subprocess
import sys
import time

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

NDC_PATH = "./ndc"  # Assuming running from nodriver dir
OUTPUT_FILE = os.path.abspath(
    os.path.join(os.getcwd(), "../../Scripts/openai_data_integration/data/raw/conversations.json")
)


def run_ndc_js(js_code):
    """Runs JS in the browser via ndc and returns the result."""
    try:
        # Run ndc using current python interpreter to ensure deps are found
        # NDC_PATH is just "ndc", we assume it's in CWD
        cmd = [sys.executable, "ndc", "js", js_code]

        result = subprocess.run(cmd, capture_output=True, text=True, env={**os.environ, "SOCKET_TIMEOUT": "30"})

        logger.info(
            f"NDC EXEC: {js_code[:50]}... | Return: {result.returncode} | Stdout: {result.stdout.strip()} | Stderr: {result.stderr.strip()}"
        )

        if result.returncode != 0:
            logger.error(f"NDC JS Error: {result.stderr}")
            return None

        # Output is usually JSON lines. The last line is usually the result.
        # Or it's a single JSON object.
        lines = result.stdout.strip().splitlines()
        for line in reversed(lines):
            try:
                data = json.loads(line)
                if "result" in data:
                    return data["result"]
                if "error" in data:
                    logger.error(f"JS Execution Error: {data['error']}")
                    return None
            except json.JSONDecodeError:
                continue
        return None
    except Exception as e:
        logger.error(f"Error executing NDC JS: {e}")
        return None


def run_ndc_cmd(cmd, arg=None):
    """Runs a generic ndc command."""
    args = [sys.executable, "ndc", cmd]
    if arg:
        args.append(arg)

    try:
        result = subprocess.run(args, capture_output=True, text=True, env={**os.environ, "SOCKET_TIMEOUT": "30"})
        return result.stdout
    except Exception as e:
        logger.error(f"Error executing NDC {cmd}: {e}")
        return None


def get_sidebar_links():
    """Extracts chat links using JS."""
    logger.info("Extracting sidebar links...")

    # Scroll sidebar
    scroll_js = "document.querySelector('nav') ? (document.querySelector('nav').scrollTop = document.querySelector('nav').scrollHeight) : 'no nav'"

    for _ in range(3):
        try:
            run_ndc_js(scroll_js)
            time.sleep(1)
        except:
            pass

    # Extract ALL links - simple JS to avoid quoting hell (pipe separated)
    # We get href and text. Filter for /c/ in python.
    hrefs_js = "Array.from(document.querySelectorAll('a')).map(a => a.href).join('|')"
    titles_js = (
        "Array.from(document.querySelectorAll('a')).map(a => a.innerText.replace('|', '').replace('\\n', '')).join('|')"
    )

    hrefs_res = run_ndc_js(hrefs_js)
    titles_res = run_ndc_js(titles_js)

    # Extract values
    # run_ndc_js returns the inner value if it finds "result"
    if isinstance(hrefs_res, str):
        href_str = hrefs_res
    else:
        href_str = ""

    if isinstance(titles_res, str):
        title_str = titles_res
    else:
        title_str = ""

    if not href_str:
        logger.warning(f"No hrefs found. Res type: {type(hrefs_res)}")
        return []

    href_list = href_str.split("|")
    title_list = title_str.split("|")

    links = []
    # Zip longest? No, should be same length
    for i in range(len(href_list)):
        h = href_list[i]
        t = title_list[i] if i < len(title_list) else "No Title"

        if "/c/" in h:
            links.append({"href": h.replace("https://chatgpt.com", ""), "title": t.strip()})

    logger.info(f"Filtered {len(links)} chat links using pipe method.")
    return links


def get_chat_messages():
    """Extracts messages."""
    time.sleep(2)

    roles_js = "Array.from(document.querySelectorAll('div[data-message-author-role]')).map(el => el.getAttribute('data-message-author-role')).join('|')"
    content_js = "Array.from(document.querySelectorAll('div[data-message-author-role]')).map(el => el.innerText.replace('|', '').replace('\\n', ' ')).join('|')"

    roles_res = run_ndc_js(roles_js)
    content_res = run_ndc_js(content_js)

    if isinstance(roles_res, str):
        roles_str = roles_res
    else:
        roles_str = ""

    if isinstance(content_res, str):
        content_str = content_res
    else:
        content_str = ""

    if not roles_str:
        return []

    roles = roles_str.split("|")
    contents = content_str.split("|")

    msgs = []
    for r, c in zip(roles, contents):
        msgs.append({"role": r, "content": c})

    return msgs


def main():
    logger.info("Starting scraper via NDC...")

    # Check connection
    status = run_ndc_cmd("status")
    logger.info(f"NDC Status: {status}")
    if not status:
        logger.error("Could not connect to NDC/Daemon.")
        return

    # Force navigation
    logger.info("Navigating to ChatGPT root...")
    run_ndc_cmd("goto", "https://chatgpt.com")
    time.sleep(5)

    # Check window size
    size_js = "JSON.stringify({width: window.innerWidth, height: window.innerHeight})"
    size_res = run_ndc_js(size_js)
    logger.info(f"Window Size: {size_res}")

    # Extract ALL links
    all_links_js = "JSON.stringify(Array.from(document.querySelectorAll('a')).map(a => a.href))"
    all_links_res = run_ndc_js(all_links_js)
    logger.info(f"All Links sample: {str(all_links_res)[:500]}")

    links = get_sidebar_links()

    unique_links = {l["href"]: l for l in links}.values()
    links = list(unique_links)
    logger.info(f"Found {len(links)} unique chats.")

    all_data = []

    # Process
    limit = 50
    for i, link in enumerate(links[:limit]):
        url = "https://chatgpt.com" + link["href"]
        logger.info(f"[{i + 1}/{len(links)}] Visiting {url}")

        # Navigate
        run_ndc_cmd("goto", url)

        # Extract
        msgs = get_chat_messages()

        chat_obj = {"title": link["title"], "conversation_id": link["href"].split("/")[-1], "messages": msgs}
        all_data.append(chat_obj)

        # Save every 5
        if i % 5 == 0:
            os.makedirs(os.path.dirname(OUTPUT_FILE), exist_ok=True)
            with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
                json.dump(all_data, f, ensure_ascii=False, indent=2)

    # Final Save
    os.makedirs(os.path.dirname(OUTPUT_FILE), exist_ok=True)
    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        json.dump(all_data, f, ensure_ascii=False, indent=2)

    logger.info("Scraping complete.")


if __name__ == "__main__":
    main()
