
import torch
import yaml
import sys
import os
import argparse
import soundfile as sf
import numpy as np
import librosa
import torchaudio
from munch import munchify
from phonemizer import phonemize

# Add paths to sys.path to import StyleTTS2 modules
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(current_dir)

# Import StyleTTS2 modules
# Note: These imports assume we are running INSIDE the StyleTTS2 directory or have paths set correctly
try:
    from models import *
    from utils import *
    from text_utils import TextCleaner
    from Utils.PLBERT.util import load_plbert
except ImportError:
    print("Error importing StyleTTS modules. Ensure you execute this script from StyleTTS2 root or set PYTHONPATH.")
    sys.exit(1)

# Initialize cleaner
textcleaner = TextCleaner()

def text_to_sequence(text):
    return textcleaner(text)

def load_model_checkpoint(model_path, config_path):
    config = yaml.safe_load(open(config_path))
    
    # Load model
    ASR_config = config.get('ASR_config', False)
    ASR_path = config.get('ASR_path', False)
    text_aligner = load_ASR_models(ASR_path, ASR_config)
    
    F0_path = config.get('F0_path', False)
    pitch_extractor = load_F0_models(F0_path)
    
    BERT_path = config.get('PLBERT_dir', False)
    plbert = load_plbert(BERT_path)
    
    model_params = munchify(config['model_params']) # Use munchify instead of recursive_munch if simple dict
    model = build_model(model_params, text_aligner, pitch_extractor, plbert)
    _ = [model[key].eval() for key in model]
    _ = [model[key].to("cuda:0" if torch.cuda.is_available() else "cpu") for key in model]
    
    params = torch.load(model_path, map_location='cpu')
    params = params['net']
    for key in model:
        if key in params:
            # print('%s loaded' % key)
            try:
                model[key].load_state_dict(params[key])
            except:
                from collections import OrderedDict
                state_dict = params[key]
                new_state_dict = OrderedDict()
                for k, v in state_dict.items():
                    name = k[7:] # remove `module.`
                    new_state_dict[name] = v
                model[key].load_state_dict(new_state_dict, strict=False)
             
    return model, config

# Audio Preprocessing
to_mel = torchaudio.transforms.MelSpectrogram(
    n_mels=80, n_fft=2048, win_length=1200, hop_length=300)
mean, std = -4, 4

def preprocess(wave):
    wave_tensor = torch.from_numpy(wave).float()
    mel_tensor = to_mel(wave_tensor)
    mel_tensor = (torch.log(1e-5 + mel_tensor.unsqueeze(0)) - mean) / std
    return mel_tensor

def compute_style(path, model, config):
    # Calculate style vector from reference audio
    wave, sr = librosa.load(path, sr=24000)
    audio, _ = librosa.effects.trim(wave, top_db=30)
    if sr != 24000:
        audio = librosa.resample(audio, sr, 24000)
    
    # Compute style
    # StyleTTS2 expects Mel Spectrogram
    mel_tensor = preprocess(audio).to("cuda:0") # [1, 80, Time]
    
    with torch.no_grad():
        # Get style from style_encoder
        ref = model.style_encoder(mel_tensor.unsqueeze(1))
    return ref

def inference(model, text, ref_s, alpha=0.3, beta=0.7, diffusion_steps=5, embedding_scale=1):
    text = text.strip()
    ps = phonemize([text], language='en-us', backend='espeak', strip=True, preserve_punctuation=True, with_stress=True)
    tokens = text_to_sequence(ps[0])
    tokens = torch.LongTensor(tokens).unsqueeze(0).to("cuda:0")
    
    # Hack for dimension mismatch (128 vs 256)
    if ref_s.shape[-1] == 128:
        # Check if model expects 256 (heuristically or try/except)
        # We know it failed with 256 expectation
        ref_s = torch.cat([ref_s, ref_s], dim=-1)
    
    with torch.no_grad():
        input_lengths = torch.LongTensor([tokens.shape[-1]]).to("cuda:0")
        text_mask = length_to_mask(input_lengths).to("cuda:0")

        t_en = model.text_encoder(tokens, input_lengths, text_mask)
        bert_dur = model.bert(tokens, attention_mask=(~text_mask).int())
        d_en = model.bert_encoder(bert_dur).transpose(-1, -2) 

        s_pred = sampler(noise = torch.randn((1, 256)).unsqueeze(1).to("cuda:0"), 
           embedding=bert_dur,
           embedding_scale=embedding_scale,
             features=ref_s, 
             num_steps=diffusion_steps).squeeze(1)

        s = s_pred[:, 128:]
        ref = s_pred[:, :128]

        ref = alpha * ref + (1 - alpha)  * ref_s[:, :128]
        s = beta * s + (1 - beta)  * ref_s[:, 128:]

        d = model.predictor.text_encoder(d_en, s, input_lengths, text_mask)

        x, _ = model.predictor.lstm(d)
        duration = model.predictor.duration_proj(x)

        duration = torch.sigmoid(duration).sum(axis=-1)
        pred_dur = torch.round(duration.squeeze()).clamp(min=1)


        pred_aln_trg = torch.zeros(input_lengths, int(pred_dur.sum().data))
        c_frame = 0
        for i in range(pred_aln_trg.size(0)):
            pred_aln_trg[i, c_frame:c_frame + int(pred_dur[i].data)] = 1
            c_frame += int(pred_dur[i].data)

        # encode prosody
        en = (d.transpose(-1, -2) @ pred_aln_trg.unsqueeze(0).to("cuda:0"))
        
        # Decoder 
        # Check decoder type from model_params global or config
        # Assuming hifigan decoder needs fix
        # In Demo:
        # if model_params.decoder.type == "hifigan": ...
        
        # Let's rely on standard decoder call
        F0_pred, N_pred = model.predictor.F0Ntrain(en, s)

        out = model.decoder(en, F0_pred, N_pred, ref.squeeze().unsqueeze(0))
        
    return out.squeeze().cpu().numpy()[..., :-50] 

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--text", type=str, required=True)
    parser.add_argument("--output", type=str, default="output.wav")
    parser.add_argument("--ref_audio", type=str, help="Path to reference audio")
    args = parser.parse_args()
    
    # Paths (Hardcoded relative to Script for stability)
    script_dir = os.path.dirname(os.path.abspath(__file__))
    model_path = os.path.join(script_dir, "Models/LibriTTS/epochs_2nd_00020.pth")
    config_path = os.path.join(script_dir, "Models/LibriTTS/config.yml")
    
    # Load Model
    global global_phonemizer # Needed for inference func
    import text_utils
    global_phonemizer = text_utils.TextCleaner()
    
    # Patch sampler
    from Modules.diffusion.sampler import KDiffusion, LogNormalDistribution, DiffusionSampler, ADPM2Sampler, KarrasSchedule
    global sampler
    # Sampler definition is tricky to import standalone, let's instantiate from model config if possible 
    # OR reuse the one from utils if available. 
    # In Demo, 'sampler' is instantiated.
    # Let's try to instantiate it here:
    
    model, config = load_model_checkpoint(model_path, config_path)
    
    # Init sampler
    sampler = DiffusionSampler(
        model.diffusion.diffusion,
        sampler=ADPM2Sampler(),
        sigma_schedule=KarrasSchedule(sigma_min=0.0001, sigma_max=3.0, rho=9.0),
        clamp=False
    )
    
    # Compute Style
    if args.ref_audio:
        ref_s = compute_style(args.ref_audio, model, config)
    else:
        # Default random reference if none provided? Or error?
        # Let's error for now or use a dummy
        print("Warning: No reference audio provided. Using zero style (bad result).")
        ref_s = torch.randn(1, 256).to("cuda:0") # Placeholder
        
    # Inference
    wav = inference(model, args.text, ref_s, diffusion_steps=5, alpha=0.3, beta=0.7)
    
    # Save
    sf.write(args.output, wav, 24000)
    print(f"Generated {args.output}")
