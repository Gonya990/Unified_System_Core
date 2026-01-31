#!/bin/bash
set -e

PROJECT_ROOT="/Users/igorgoncharenko/Documents/Unified_System_Core/Projects/Content_Factory"
SRC_DIR="$PROJECT_ROOT/src"

echo "🏭 Setting up Content Factory Production Environment..."

# 1. Setup Wav2Lip
echo "👄 Setting up Wav2Lip..."
WAV2LIP_DIR="$SRC_DIR/lip_sync/Wav2Lip"
mkdir -p "$WAV2LIP_DIR/checkpoints"

if [ ! -d "$WAV2LIP_DIR/.git" ]; then
    echo "   Cloning Wav2Lip..."
    # Remove if empty or partial
    rm -rf "$WAV2LIP_DIR"
    git clone https://github.com/Rudrabha/Wav2Lip.git "$WAV2LIP_DIR"
else
    echo "   ✓ Wav2Lip repo exists."
fi

# Download Wav2Lip GAN Model (Better quality)
if [ ! -f "$WAV2LIP_DIR/checkpoints/wav2lip_gan.pth" ]; then
    echo "   ⬇️ Downloading Wav2Lip GAN Model..."
    curl -L -o "$WAV2LIP_DIR/checkpoints/wav2lip_gan.pth" "https://huggingface.co/camenduru/Wav2Lip/resolve/main/wav2lip_gan.pth"
else
    echo "   ✓ Wav2Lip weights exist."
fi

# 2. Setup LivePortrait
echo "🎬 Setting up LivePortrait..."
LIVE_PORTRAIT_DIR="$SRC_DIR/live_portrait"
mkdir -p "$LIVE_PORTRAIT_DIR"

if [ ! -d "$LIVE_PORTRAIT_DIR/.git" ]; then
    echo "   Cloning LivePortrait..."
    rm -rf "$LIVE_PORTRAIT_DIR" 
    git clone https://github.com/KwaiVGI/LivePortrait.git "$LIVE_PORTRAIT_DIR"
else
    echo "   ✓ LivePortrait repo exists."
fi

# Download LivePortrait Weights
LP_WEIGHTS_DIR="$LIVE_PORTRAIT_DIR/pretrained_weights"
mkdir -p "$LP_WEIGHTS_DIR"

if [ ! -f "$LP_WEIGHTS_DIR/appearance_feature_extractor.pth" ]; then
    echo "   ⬇️ Downloading LivePortrait Weights..."
    BASE_URL="https://huggingface.co/KwaiVGI/LivePortrait/resolve/main/pretrained_weights"
    
    curl -L -o "$LP_WEIGHTS_DIR/appearance_feature_extractor.pth" "$BASE_URL/appearance_feature_extractor.pth"
    curl -L -o "$LP_WEIGHTS_DIR/motion_extractor.pth" "$BASE_URL/motion_extractor.pth"
    curl -L -o "$LP_WEIGHTS_DIR/spade_generator.pth" "$BASE_URL/spade_generator.pth"
    curl -L -o "$LP_WEIGHTS_DIR/warping_module.pth" "$BASE_URL/warping_module.pth"
    
    mkdir -p "$LP_WEIGHTS_DIR/insightface/models/buffalo_l"
    curl -L -o "$LP_WEIGHTS_DIR/insightface/models/buffalo_l/2d106det.onnx" "https://huggingface.co/KwaiVGI/LivePortrait/resolve/main/pretrained_weights/insightface/models/buffalo_l/2d106det.onnx"
    curl -L -o "$LP_WEIGHTS_DIR/insightface/models/buffalo_l/det_10g.onnx" "https://huggingface.co/KwaiVGI/LivePortrait/resolve/main/pretrained_weights/insightface/models/buffalo_l/det_10g.onnx"
else
    echo "   ✓ LivePortrait weights exist."
fi

echo "✅ Environment Setup Complete!"
