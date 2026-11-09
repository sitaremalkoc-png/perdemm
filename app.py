import random
import gradio as gr
import spaces
import torch
from PIL import Image
from diffusers import QwenImageEditPlusPipeline

MODEL_ID = "Qwen/Qwen-Image-Edit-2509"
DEVICE = "cuda" if torch.cuda.is_available() else "cpu"
DTYPE = torch.bfloat16 if DEVICE == "cuda" else torch.float32

pipe = QwenImageEditPlusPipeline.from_pretrained(MODEL_ID, torch_dtype=DTYPE).to(DEVICE)
if DEVICE == "cuda" and hasattr(spaces, "aoti_blocks_load"):
    try:
        spaces.aoti_blocks_load(pipe.transformer, "zerogpu-aoti/Qwen-Image", variant="fa3")
    except Exception as exc:
        print(f"AOTI optimization not applied: {exc}")
pipe.set_progress_bar_config(disable=True)

@spaces.GPU(duration=300)
def generate(room: Image.Image, fabric: Image.Image, prompt: str, seed: int = 0, steps: int = 20):
    if room is None or fabric is None:
        raise gr.Error("Oda ve kumaş fotoğrafı birlikte gerekli.")
    room = room.convert("RGB")
    fabric = fabric.convert("RGB")
    seed = int(seed) if int(seed) >= 0 else random.randint(0, 2**31 - 1)
    generator = torch.Generator(device=DEVICE).manual_seed(seed)
    result = pipe(
        image=[room, fabric],
        prompt=prompt,
        negative_prompt="blurry, distorted room, altered furniture, changed architecture, text, watermark",
        true_cfg_scale=3.5,
        num_inference_steps=max(8, min(30, int(steps))),
        guidance_scale=1.0,
        generator=generator,
        num_images_per_prompt=1,
    ).images[0]
    return result

with gr.Blocks(title="Perde AI Studio - Private Model Gateway") as demo:
    gr.Markdown("# Perde AI Studio\nÖzel perde görselleştirme modeli")
    with gr.Row():
        room = gr.Image(type="pil", label="Oda fotoğrafı")
        fabric = gr.Image(type="pil", label="Kumaş referansı")
    prompt = gr.Textbox(label="Tasarım talimatı", lines=5)
    with gr.Row():
        seed = gr.Number(value=0, precision=0, label="Seed")
        steps = gr.Slider(8, 30, value=20, step=1, label="Adım sayısı")
    output = gr.Image(type="pil", label="Sonuç")
    button = gr.Button("Perdeyi oluştur", variant="primary")
    button.click(generate, [room, fabric, prompt, seed, steps], output, api_name="generate")

demo.queue(default_concurrency_limit=1).launch()
