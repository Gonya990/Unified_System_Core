import json
import os

def fix_package_json(file_path, line_numbers):
    if not os.path.exists(file_path):
        print(f"⚠️ {file_path} not found")
        return
    
    with open(file_path, 'r') as f:
        lines = f.readlines()
    
    # Sort line numbers in descending order to avoid index issues when deleting
    for ln in sorted(line_numbers, reverse=True):
        idx = ln - 1
        if 0 <= idx < len(lines):
            print(f"  → Removing line {ln} from {file_path}")
            lines.pop(idx)
        else:
            print(f"  → Line {ln} out of range for {file_path}")
    
    with open(file_path, 'w') as f:
        f.writelines(lines)

def run_cleanup():
    problems = [
        ("/Users/igorgoncharenko/.antigravity/extensions/henrikdev.ag-quota-1.1.0-universal/package.json", [16, 19, 20]),
        ("/Users/igorgoncharenko/.antigravity/extensions/mechatroner.rainbow-csv-3.24.1/package.json", [23, 24, 25, 26, 27, 28, 30, 31, 32, 33]),
        ("/Users/igorgoncharenko/.antigravity/extensions/ms-kubernetes-tools.vscode-kubernetes-tools-1.3.29-universal/package.json", [28]),
        ("/Users/igorgoncharenko/.antigravity/extensions/ms-toolsai.vscode-jupyter-cell-tags-0.1.9-universal/package.json", [24, 25, 26, 27]),
        ("/Users/igorgoncharenko/.antigravity/extensions/ms-toolsai.vscode-jupyter-slideshow-0.1.6-universal/package.json", [24, 25]),
        ("/Users/igorgoncharenko/.antigravity/extensions/suhaibbinyounis.github-copilot-api-vscode-2.7.0/package.json", [60]),
        ("/Users/igorgoncharenko/.vscode/extensions/ms-toolsai.vscode-jupyter-slideshow-0.1.6/package.json", [24, 25]),
        ("/Users/igorgoncharenko/.vscode/extensions/suhaibbinyounis.github-copilot-api-vscode-2.7.0/package.json", [60]),
        ("/Users/igorgoncharenko/.vscode/extensions/vscjava.vscode-java-test-0.44.0/package.json", [50, 51, 52, 53]),
        # Info level removals
        ("/Users/igorgoncharenko/.antigravity/extensions/1nvitr0.gtm-editor-1.2.0-universal/package.json", [31]),
        ("/Users/igorgoncharenko/.antigravity/extensions/funkyremi.vscode-google-translate-1.5.0/package.json", [20, 21, 22, 23, 24]),
        ("/Users/igorgoncharenko/.antigravity/extensions/lior-chamla.google-fonts-0.0.1/package.json", [15, 16]),
        ("/Users/igorgoncharenko/.antigravity/extensions/msjsdiag.debugger-for-chrome-4.13.0/package.json", [82, 83]),
        ("/Users/igorgoncharenko/.antigravity/extensions/redhat.vscode-yaml-1.19.1-universal/package.json", [42]),
        ("/Users/igorgoncharenko/.antigravity/extensions/techer.open-in-browser-2.0.0-universal/package.json", [21, 22]),
        ("/Users/igorgoncharenko/.antigravity/extensions/vscjava.vscode-java-pack-0.30.5-universal/package.json", [55, 56, 58, 59, 61, 63, 65, 67, 68, 70, 71]),
    ]
    
    for path, lns in problems:
        fix_package_json(path, lns)

if __name__ == "__main__":
    run_cleanup()
