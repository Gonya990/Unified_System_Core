import io
import os
import threading

import torch
from einops import rearrange
from fastapi import FastAPI
from fastapi.responses import Response
from pydantic import BaseModel
from PIL import Image

from flux.sampling import denoise, get_noise, get_schedule, prepare, unpack
from flux.util import embed_watermark, load_ae, load_clip, load_flow_model
from flux.modules.conditioner import HFEmbedder


class GenerateRequest(BaseModel):
    prompt: str
    width: int = 1080
    height: int = 1920
    num_steps: int = 4
    guidance: float = 3.5
    seed: int | None = None


class FluxServer:
    def __init__(self):
        self.model_name = os.getenv("FLUX_MODEL", "flux-schnell")
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        self.is_schnell = self.model_name == "flux-schnell"

        t5_model = os.getenv("FLUX_T5_MODEL", "google/t5-v1_1-large")
        self.t5 = HFEmbedder(
            t5_model,
            max_length=256 if self.is_schnell else 512,
            torch_dtype=torch.bfloat16,
        ).to(self.device)
        self.clip = load_clip(self.device)
        self.model = load_flow_model(self.model_name, device=self.device)
        self.ae = load_ae(self.model_name, device=self.device)

        self.lock = threading.Lock()

    @torch.inference_mode()
    def generate(self, req: GenerateRequest) -> bytes:
        width = 16 * (req.width // 16)
        height = 16 * (req.height // 16)

        seed = req.seed
        if seed is None:
            seed = torch.Generator(device="cpu").seed()

        x = get_noise(
            1,
            height,
            width,
            device=self.device,
            dtype=torch.bfloat16,
            seed=seed,
        )
        timesteps = get_schedule(
            req.num_steps,
            x.shape[-1] * x.shape[-2] // 4,
            shift=(not self.is_schnell),
        )
        inp = prepare(t5=self.t5, clip=self.clip, img=x, prompt=req.prompt)
        x = denoise(self.model, **inp, timesteps=timesteps, guidance=req.guidance)
        x = unpack(x.float(), height, width)
        with torch.autocast(device_type=self.device.type, dtype=torch.bfloat16):
            x = self.ae.decode(x)

        x = x.clamp(-1, 1)
        x = embed_watermark(x.float())
        x = rearrange(x[0], "c h w -> h w c")
        img = Image.fromarray((127.5 * (x + 1.0)).cpu().byte().numpy())

        buf = io.BytesIO()
        img.save(buf, format="JPEG", quality=95, subsampling=0)
        return buf.getvalue()


app = FastAPI(title="Flux.1 Schnell Server")
_server = FluxServer()


@app.get("/")
def health():
    return {"status": "ok", "model": _server.model_name}


@app.post("/generate")
def generate(req: GenerateRequest):
    with _server.lock:
        img_bytes = _server.generate(req)
    return Response(content=img_bytes, media_type="image/jpeg")


if __name__ == "__main__":
    import uvicorn

    host = os.getenv("FLUX_HOST", "0.0.0.0")
    port = int(os.getenv("FLUX_PORT", "8081"))
    uvicorn.run(app, host=host, port=port, log_level="info")
