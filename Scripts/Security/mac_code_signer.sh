#!/bin/bash
# Signs all project artifacts with Apple Developer ID
# Usage: ./mac_code_signer.sh "Developer ID Application: Name (ID)"

IDENTITY="${1:-Developer ID Application: Igor Goncharenko (DW65K3AAUJ)}"
PROJECT_ROOT="$(cd "$(dirname "$0")/../.." && pwd)"

echo "🔐 Starting Code Signing Process..."
echo "👤 Identity: $IDENTITY"
echo "📂 Root: $PROJECT_ROOT"

# Check if identity exists
if ! security find-identity -v -p codesigning | grep -q "DW65K3AAUJ"; then
    echo "❌ Error: Certificate '$IDENTITY' not found in Keychain."
    echo "👉 Please install your Apple Developer Certificate first."
    echo "   1. Download the certificate (.cer) from developer.apple.com"
    echo "   2. Double-click to install into Keychain Access"
    echo "   3. Ensure you have the private key (which you seem to have in unique files)"
    echo ""
    echo "Current valid identities:"
    security find-identity -v -p codesigning
    exit 1
fi

# Find and sign files
# Targeting: Executables, Python scripts, Shell scripts, Shared Libs
# Excludes git, venv, node_modules to save time and avoid errors
find "$PROJECT_ROOT" \
    -type f \
    \( -name "*.py" -o -name "*.sh" -o -name "*.so" -o -name "*.dylib" -o -perm +111 \) \
    -not -path "*/.git/*" \
    -not -path "*/venv/*" \
    -not -path "*/.venv/*" \
    -not -path "*/env/*" \
    -not -path "*/.env/*" \
    -not -path "*/.agent/*" \
    -not -path "*/node_modules/*" \
    | while read -r FILE; do
        # Sign if it is a script (has shebang) or a binary (Mach-O)
        if head -n1 "$FILE" | grep -q "^#!" || file "$FILE" | grep -q "Mach-O"; then
             echo "✍️  Signing: $FILE"
             # Use --force to overwrite existing signatures
             # --options runtime enables Hardened Runtime (required for notarization)
             # --timestamp includes a secure timestamp
             codesign --force --sign "$IDENTITY" --options runtime --timestamp "$FILE" || echo "⚠️ Failed to sign $FILE"
        fi
    done

echo "✅ Signing complete."
