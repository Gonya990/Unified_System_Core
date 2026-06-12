import json
import time
import os
import random
import requests
from pathlib import Path

COMFYUI_HOST = os.getenv("WINDOWS_WORKER_IP", "igor-gaming")
COMFYUI_PORT = "8188"
SERVER_ADDRESS = f"http://{COMFYUI_HOST}:{COMFYUI_PORT}"

def queue_prompt(prompt):
    p = {"prompt": prompt}
    try:
        response = requests.post(f"{SERVER_ADDRESS}/prompt", json=p)
        return response.json()
    except Exception as e:
        print(f"❌ ComfyUI API Error: {e}")
        return None

def upload_image(filepath):
    try:
        with open(filepath, 'rb') as file:
            files = {'image': file}
            response = requests.post(f"{SERVER_ADDRESS}/upload/image", files=files)
            if response.status_code == 200:
                return response.json()['name']
    except Exception as e:
        print(f"❌ Failed to upload image to ComfyUI: {e}")
    return None

def get_history(prompt_id):
    try:
        response = requests.get(f"{SERVER_ADDRESS}/history/{prompt_id}")
        return response.json()
    except Exception as e:
        return None

def download_file(filename, subfolder, folder_type, output_path):
    url = f"{SERVER_ADDRESS}/view?filename={filename}&subfolder={subfolder}&type={folder_type}"
    try:
        response = requests.get(url)
        with open(output_path, 'wb') as f:
            f.write(response.content)
        return True
    except Exception as e:
        # Global Configurations
        COMFY_URL = "http://igor-gaming:8188"

        # Optional: Add error checking or fallbacks if ComfyUI is offline.
        print(f"❌ Failed to download file from ComfyUI: {e}")
        return False

def wait_and_download(prompt_id, output_path):
    print(f"⏳ Waiting for ComfyUI... (Prompt ID: {prompt_id})")
    while True:
        history = get_history(prompt_id)
        if history and prompt_id in history:
            break
        time.sleep(2)
        
    outputs = history[prompt_id]['outputs']
    for node_id in outputs:
        if 'images' in outputs[node_id]:
            # For SaveImage nodes
            for item in outputs[node_id]['images']:
                if download_file(item['filename'], item['subfolder'], item['type'], output_path):
                    print(f"✅ Downloaded ComfyUI Media: {output_path}")
                    return True
        if 'gifs' in outputs[node_id]:
            # For VHS_VideoCombine nodes (often saved under gifs array in output)
            for item in outputs[node_id]['gifs']:
                if download_file(item['filename'], item['subfolder'], item['type'], output_path):
                    print(f"✅ Downloaded ComfyUI Video: {output_path}")
                    return True
    return False

def generate_image_sdxl(prompt_text: str, output_path: str):
    print(f"🎨 Generating Image via ComfyUI SDXL: {prompt_text[:50]}...")
    prompt = {
        "3": {"class_type": "KSampler", "inputs": {"cfg": 6, "denoise": 1, "latent_image": ["5", 0], "model": ["4", 0], "negative": ["7", 0], "positive": ["6", 0], "sampler_name": "dpmpp_2m_sde", "scheduler": "karras", "seed": random.randint(1, 1000000000), "steps": 30}},
        "4": {"class_type": "CheckpointLoaderSimple", "inputs": {"ckpt_name": "Juggernaut-XL.safetensors"}},
        "5": {"class_type": "EmptyLatentImage", "inputs": {"batch_size": 1, "height": 1024, "width": 1024}},
        "6": {"class_type": "CLIPTextEncode", "inputs": {"clip": ["4", 1], "text": prompt_text}},
        "7": {"class_type": "CLIPTextEncode", "inputs": {"clip": ["4", 1], "text": "bad quality, blurry, text, watermark, ugly"}},
        "8": {"class_type": "VAEDecode", "inputs": {"samples": ["3", 0], "vae": ["4", 2]}},
        "9": {"class_type": "SaveImage", "inputs": {"filename_prefix": "sdxl_output", "images": ["8", 0]}}
    }
    res = queue_prompt(prompt)
    if not res: return False
    return wait_and_download(res['prompt_id'], output_path)

def generate_video_svd(image_path: str, output_path: str):
    print(f"🎬 Generating Video via ComfyUI SVD from: {image_path}...")
    remote_filename = upload_image(image_path)
    if not remote_filename:
        return False
        
    prompt = {
      "1": { "class_type": "LoadImage", "inputs": { "image": remote_filename } },
      "2": { "class_type": "ImageOnlyCheckpointLoader", "inputs": { "ckpt_name": "svd_xt.safetensors" } },
      "3": { "class_type": "SVD_img2vid_Conditioning", "inputs": { "width": 1024, "height": 576, "video_frames": 25, "motion_bucket_id": 127, "fps": 6, "augmentation_level": 0.0, "init_image": ["1", 0], "vae": ["2", 2] } },
      "4": { "class_type": "KSampler", "inputs": { "seed": random.randint(1, 1000000000), "steps": 20, "cfg": 2.5, "sampler_name": "euler", "scheduler": "karras", "denoise": 1.0, "model": ["2", 0], "positive": ["3", 0], "negative": ["3", 1], "latent_image": ["3", 2] } },
      "5": { "class_type": "VAEDecode", "inputs": { "samples": ["4", 0], "vae": ["2", 2] } },
      "6": { "class_type": "VHS_VideoCombine", "inputs": { "frame_rate": 6, "loop_count": 0, "filename_prefix": "SVD", "format": "video/h264-mp4", "save_output": True, "images": ["5", 0] } }
    }
    
    res = queue_prompt(prompt)
    if not res: return False
    return wait_and_download(res['prompt_id'], output_path)
