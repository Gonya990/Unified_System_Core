#!/bin/bash
set -e

PROJECT_ROOT="/Users/igorgoncharenko/Documents/Unified_System_Core/Projects/Content_Factory"
SRC_DIR="$PROJECT_ROOT/src"

echo "🏭 Setting up Content Factory Production Environment (Attempt 2)..."

# 1. Setup Wav2Lip (Fixing bad download)
echo "👄 Setting up Wav2Lip..."
WAV2LIP_DIR="$SRC_DIR/lip_sync/Wav2Lip"
mkdir -p "$WAV2LIP_DIR/checkpoints"

# Delete bad file if small
find "$WAV2LIP_DIR/checkpoints" -name "*.pth" -size -1k -delete

if [ ! -f "$WAV2LIP_DIR/checkpoints/wav2lip_gan.pth" ]; then
    echo "   ⬇️ Downloading Wav2Lip GAN Model (via git lfs repo)..."
    # Clone a repo that has the weights
    if [ ! -d "tmp_wav2lip_weights" ]; then
        git clone https://huggingface.co/camenduru/Wav2Lip tmp_wav2lip_weights
    fi
    cp tmp_wav2lip_weights/checkpoints/wav2lip_gan.pth "$WAV2LIP_DIR/checkpoints/"
    rm -rf tmp_wav2lip_weights
    echo "   ✓ Wav2Lip weights installed."
else
    echo "   ✓ Wav2Lip weights appear valid."
fi

# 2. Setup LivePortrait (Fixing bad download)
echo "🎬 Setting up LivePortrait..."
LIVE_PORTRAIT_DIR="$SRC_DIR/live_portrait"
LP_WEIGHTS_DIR="$LIVE_PORTRAIT_DIR/pretrained_weights"
mkdir -p "$LP_WEIGHTS_DIR"

# Delete bad files if small
find "$LP_WEIGHTS_DIR" -name "*.pth" -size -1k -delete
find "$LP_WEIGHTS_DIR" -name "*.onnx" -size -1k -delete

if [ ! -f "$LP_WEIGHTS_DIR/appearance_feature_extractor.pth" ]; then
    echo "   ⬇️ Downloading LivePortrait Weights (via git lfs)..."
    
    if [ ! -d "tmp_live_portrait_weights" ]; then
        git clone https://huggingface.co/KwaiVGI/LivePortrait tmp_live_portrait_weights
    fi
    
    # Move files
    cp tmp_live_portrait_weights/pretrained_weights/*.pth "$LP_WEIGHTS_DIR/"
    
    # Move insightface folder
    mkdir -p "$LP_WEIGHTS_DIR/insightface/models/buffalo_l"
    cp -r tmp_live_portrait_weights/pretrained_weights/insightface/models/buffalo_l/* "$LP_WEIGHTS_DIR/insightface/models/buffalo_l/"
    
    rm -rf tmp_live_portrait_weights
    echo "   ✓ LivePortrait weights installed."
else
    echo "   ✓ LivePortrait weights appear valid."
fi

echo "✅ Environment Setup Complete!"
