import io
import os
import threading

import torch
from fastapi import FastAPI
from fastapi.responses import Response
from pydantic import BaseModel
from PIL import Image
from diffusers import StableDiffusionXLPipeline


class GenerateRequest(BaseModel):
    prompt: str
    negative_prompt: str | None = None
    width: int = 1080
    height: int = 1920
    steps: int = 25
    guidance: float = 7.0
    seed: int | None = None


class SDXLServer:
    def __init__(self):
        self.model_id = os.getenv("SDXL_MODEL_ID", "stabilityai/stable-diffusion-xl-base-1.0")
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        self.pipe = StableDiffusionXLPipeline.from_pretrained(
            self.model_id,
            torch_dtype=torch.float16 if self.device == "cuda" else torch.float32,
            use_safetensors=True,
        )
        if self.device == "cuda":
            self.pipe.to(self.device)
        self.pipe.set_progress_bar_config(disable=True)
        self.lock = threading.Lock()

    @torch.inference_mode()
    def generate(self, req: GenerateRequest) -> bytes:
        width = 8 * (req.width // 8)
        height = 8 * (req.height // 8)
        generator = None
        if req.seed is not None:
            generator = torch.Generator(self.device).manual_seed(req.seed)

        result = self.pipe(
            prompt=req.prompt,
            negative_prompt=req.negative_prompt,
            width=width,
            height=height,
            num_inference_steps=req.steps,
            guidance_scale=req.guidance,
            generator=generator,
        )
        img: Image.Image = result.images[0]
        buf = io.BytesIO()
        img.save(buf, format="JPEG", quality=95, subsampling=0)
        return buf.getvalue()


app = FastAPI(title="SDXL Server")
_server = SDXLServer()


@app.get("/")
def health():
    return {"status": "ok", "model": _server.model_id}


@app.post("/generate")
def generate(req: GenerateRequest):
    with _server.lock:
        img_bytes = _server.generate(req)
    return Response(content=img_bytes, media_type="image/jpeg")


if __name__ == "__main__":
    import uvicorn

    host = os.getenv("SDXL_HOST", "0.0.0.0")
    port = int(os.getenv("SDXL_PORT", "8188"))
    uvicorn.run(app, host=host, port=port, log_level="info")
