---
name: multimodal-ai-vision-speech-suite
description: >-
  Multimodal AI Vision & Speech Processing Suite: OpenAI Whisper automatic speech recognition, Stable Diffusion generative imagery, Segment Anything (SAM) zero-shot image segmentation, and CLIP zero-shot vision-text embedding.
version: 2.0.0
tags:
  - multimodal
  - whisper
  - speech-to-text
  - stable-diffusion
  - sam
  - clip
  - vision-ai
merged_member_skills:
  - clip (01_Hermes_Skills_Core_Library\mlops\models\clip\SKILL.md)
  - segment-anything-model (01_Hermes_Skills_Core_Library\mlops\models\segment-anything\SKILL.md)
  - stable-diffusion-image-generation (01_Hermes_Skills_Core_Library\mlops\models\stable-diffusion\SKILL.md)
  - whisper (01_Hermes_Skills_Core_Library\mlops\models\whisper\SKILL.md)
---

# Multimodal Ai Vision Speech Suite

> **Master Suite Consolidée :** Regroupe et unifie **4 compétences spécialisées** de l'écosystème Hermes en une référence modulaire et cohérente.


## 🎯 Quand Déclencher cette Master Suite (Triggers)
Cette suite doit être activée dès que l'utilisateur mentionne l'un des mots-clés, frameworks, outils ou objectifs liés aux modules inclus ci-dessous.
Chaque module peut être exécuté individuellement ou orchestré en séquence selon la tâche demandée.

---
## 📋 Vue d'Ensemble & Sommaire des Modules

1. **[clip](#module-1-clip)** : OpenAI's model connecting vision and language. Enables zero-shot image classification, image-text matching, and cross-modal retrieval. Trained on 400M image-text pairs. Use for image search, content moderation, or vision-language tasks without fine-tuning. Best for general-purpose image understanding.
2. **[segment-anything-model](#module-2-segment-anything-model)** : Foundation model for image segmentation with zero-shot transfer. Use when you need to segment any object in images using points, boxes, or masks as prompts, or automatically generate all object masks in an image.
3. **[stable-diffusion-image-generation](#module-3-stable-diffusion-image-generation)** : State-of-the-art text-to-image generation with Stable Diffusion models via HuggingFace Diffusers. Use when generating images from text prompts, performing image-to-image translation, inpainting, or building custom diffusion pipelines.
4. **[whisper](#module-4-whisper)** : OpenAI's general-purpose speech recognition model. Supports 99 languages, transcription, translation to English, and language identification. Six model sizes from tiny (39M params) to large (1550M params). Use for speech-to-text, podcast transcription, or multilingual audio processing. Best for robust, multilingual ASR.

---

## Module 1: `clip`

- **Origine :** `01_Hermes_Skills_Core_Library\mlops\models\clip\SKILL.md`
- **Rôle / Objectif :** OpenAI's model connecting vision and language. Enables zero-shot image classification, image-text matching, and cross-modal retrieval. Trained on 400M image-text pairs. Use for image search, content moderation, or vision-language tasks without fine-tuning. Best for general-purpose image understanding.

## CLIP - Contrastive Language-Image Pre-Training

OpenAI's model that understands images from natural language.

### When to use CLIP

**Use when:**
- Zero-shot image classification (no training data needed)
- Image-text similarity/matching
- Semantic image search
- Content moderation (detect NSFW, violence)
- Visual question answering
- Cross-modal retrieval (image→text, text→image)

**Metrics**:
- **25,300+ GitHub stars**
- Trained on 400M image-text pairs
- Matches ResNet-50 on ImageNet (zero-shot)
- MIT License

**Use alternatives instead**:
- **BLIP-2**: Better captioning
- **LLaVA**: Vision-language chat
- **Segment Anything**: Image segmentation

### Quick start

#### Installation

```bash
pip install git+https://github.com/openai/CLIP.git
pip install torch torchvision ftfy regex tqdm
```

#### Zero-shot classification

```python
import torch
import clip
from PIL import Image

## Load model
device = "cuda" if torch.cuda.is_available() else "cpu"
model, preprocess = clip.load("ViT-B/32", device=device)

## Load image
image = preprocess(Image.open("photo.jpg")).unsqueeze(0).to(device)

## Define possible labels
text = clip.tokenize(["a dog", "a cat", "a bird", "a car"]).to(device)

## Compute similarity
with torch.no_grad():
    image_features = model.encode_image(image)
    text_features = model.encode_text(text)

    # Cosine similarity
    logits_per_image, logits_per_text = model(image, text)
    probs = logits_per_image.softmax(dim=-1).cpu().numpy()

## Print results
labels = ["a dog", "a cat", "a bird", "a car"]
for label, prob in zip(labels, probs[0]):
    print(f"{label}: {prob:.2%}")
```

### Available models

```python
## Models (sorted by size)
models = [
    "RN50",           # ResNet-50
    "RN101",          # ResNet-101
    "ViT-B/32",       # Vision Transformer (recommended)
    "ViT-B/16",       # Better quality, slower
    "ViT-L/14",       # Best quality, slowest
]

model, preprocess = clip.load("ViT-B/32")
```

| Model | Parameters | Speed | Quality |
|-------|------------|-------|---------|
| RN50 | 102M | Fast | Good |
| ViT-B/32 | 151M | Medium | Better |
| ViT-L/14 | 428M | Slow | Best |

### Image-text similarity

```python
## Compute embeddings
image_features = model.encode_image(image)
text_features = model.encode_text(text)

## Normalize
image_features /= image_features.norm(dim=-1, keepdim=True)
text_features /= text_features.norm(dim=-1, keepdim=True)

## Cosine similarity
similarity = (image_features @ text_features.T).item()
print(f"Similarity: {similarity:.4f}")
```

### Semantic image search

```python
## Index images
image_paths = ["img1.jpg", "img2.jpg", "img3.jpg"]
image_embeddings = []

for img_path in image_paths:
    image = preprocess(Image.open(img_path)).unsqueeze(0).to(device)
    with torch.no_grad():
        embedding = model.encode_image(image)
        embedding /= embedding.norm(dim=-1, keepdim=True)
    image_embeddings.append(embedding)

image_embeddings = torch.cat(image_embeddings)

## Search with text query
query = "a sunset over the ocean"
text_input = clip.tokenize([query]).to(device)
with torch.no_grad():
    text_embedding = model.encode_text(text_input)
    text_embedding /= text_embedding.norm(dim=-1, keepdim=True)

## Find most similar images
similarities = (text_embedding @ image_embeddings.T).squeeze(0)
top_k = similarities.topk(3)

for idx, score in zip(top_k.indices, top_k.values):
    print(f"{image_paths[idx]}: {score:.3f}")
```

### Content moderation

```python
## Define categories
categories = [
    "safe for work",
    "not safe for work",
    "violent content",
    "graphic content"
]

text = clip.tokenize(categories).to(device)

## Check image
with torch.no_grad():
    logits_per_image, _ = model(image, text)
    probs = logits_per_image.softmax(dim=-1)

## Get classification
max_idx = probs.argmax().item()
max_prob = probs[0, max_idx].item()

print(f"Category: {categories[max_idx]} ({max_prob:.2%})")
```

### Batch processing

```python
## Process multiple images
images = [preprocess(Image.open(f"img{i}.jpg")) for i in range(10)]
images = torch.stack(images).to(device)

with torch.no_grad():
    image_features = model.encode_image(images)
    image_features /= image_features.norm(dim=-1, keepdim=True)

## Batch text
texts = ["a dog", "a cat", "a bird"]
text_tokens = clip.tokenize(texts).to(device)

with torch.no_grad():
    text_features = model.encode_text(text_tokens)
    text_features /= text_features.norm(dim=-1, keepdim=True)

## Similarity matrix (10 images × 3 texts)
similarities = image_features @ text_features.T
print(similarities.shape)  # (10, 3)
```

### Integration with vector databases

```python
## Store CLIP embeddings in Chroma/FAISS
import chromadb

client = chromadb.Client()
collection = client.create_collection("image_embeddings")

## Add image embeddings
for img_path, embedding in zip(image_paths, image_embeddings):
    collection.add(
        embeddings=[embedding.cpu().numpy().tolist()],
        metadatas=[{"path": img_path}],
        ids=[img_path]
    )

## Query with text
query = "a sunset"
text_embedding = model.encode_text(clip.tokenize([query]))
results = collection.query(
    query_embeddings=[text_embedding.cpu().numpy().tolist()],
    n_results=5
)
```

### Best practices

1. **Use ViT-B/32 for most cases** - Good balance
2. **Normalize embeddings** - Required for cosine similarity
3. **Batch processing** - More efficient
4. **Cache embeddings** - Expensive to recompute
5. **Use descriptive labels** - Better zero-shot performance
6. **GPU recommended** - 10-50× faster
7. **Preprocess images** - Use provided preprocess function

### Performance

| Operation | CPU | GPU (V100) |
|-----------|-----|------------|
| Image encoding | ~200ms | ~20ms |
| Text encoding | ~50ms | ~5ms |
| Similarity compute | <1ms | <1ms |

### Limitations

1. **Not for fine-grained tasks** - Best for broad categories
2. **Requires descriptive text** - Vague labels perform poorly
3. **Biased on web data** - May have dataset biases
4. **No bounding boxes** - Whole image only
5. **Limited spatial understanding** - Position/counting weak

### Resources

- **GitHub**: https://github.com/openai/CLIP ⭐ 25,300+
- **Paper**: https://arxiv.org/abs/2103.00020
- **Colab**: https://colab.research.google.com/github/openai/clip/
- **License**: MIT


---

## Module 2: `segment-anything-model`

- **Origine :** `01_Hermes_Skills_Core_Library\mlops\models\segment-anything\SKILL.md`
- **Rôle / Objectif :** Foundation model for image segmentation with zero-shot transfer. Use when you need to segment any object in images using points, boxes, or masks as prompts, or automatically generate all object masks in an image.

## Segment Anything Model (SAM)

Comprehensive guide to using Meta AI's Segment Anything Model for zero-shot image segmentation.

### When to use SAM

**Use SAM when:**
- Need to segment any object in images without task-specific training
- Building interactive annotation tools with point/box prompts
- Generating training data for other vision models
- Need zero-shot transfer to new image domains
- Building object detection/segmentation pipelines
- Processing medical, satellite, or domain-specific images

**Key features:**
- **Zero-shot segmentation**: Works on any image domain without fine-tuning
- **Flexible prompts**: Points, bounding boxes, or previous masks
- **Automatic segmentation**: Generate all object masks automatically
- **High quality**: Trained on 1.1 billion masks from 11 million images
- **Multiple model sizes**: ViT-B (fastest), ViT-L, ViT-H (most accurate)
- **ONNX export**: Deploy in browsers and edge devices

**Use alternatives instead:**
- **YOLO/Detectron2**: For real-time object detection with classes
- **Mask2Former**: For semantic/panoptic segmentation with categories
- **GroundingDINO + SAM**: For text-prompted segmentation
- **SAM 2**: For video segmentation tasks

### Quick start

#### Installation

```bash
## From GitHub
pip install git+https://github.com/facebookresearch/segment-anything.git

## Optional dependencies
pip install opencv-python pycocotools matplotlib

## Or use HuggingFace transformers
pip install transformers
```

#### Download checkpoints

```bash
## ViT-H (largest, most accurate) - 2.4GB
wget https://dl.fbaipublicfiles.com/segment_anything/sam_vit_h_4b8939.pth

## ViT-L (medium) - 1.2GB
wget https://dl.fbaipublicfiles.com/segment_anything/sam_vit_l_0b3195.pth

## ViT-B (smallest, fastest) - 375MB
wget https://dl.fbaipublicfiles.com/segment_anything/sam_vit_b_01ec64.pth
```

#### Basic usage with SamPredictor

```python
import numpy as np
from segment_anything import sam_model_registry, SamPredictor

## Load model
sam = sam_model_registry["vit_h"](checkpoint="sam_vit_h_4b8939.pth")
sam.to(device="cuda")

## Create predictor
predictor = SamPredictor(sam)

## Set image (computes embeddings once)
image = cv2.imread("image.jpg")
image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
predictor.set_image(image)

## Predict with point prompts
input_point = np.array([[500, 375]])  # (x, y) coordinates
input_label = np.array([1])  # 1 = foreground, 0 = background

masks, scores, logits = predictor.predict(
    point_coords=input_point,
    point_labels=input_label,
    multimask_output=True  # Returns 3 mask options
)

## Select best mask
best_mask = masks[np.argmax(scores)]
```

#### HuggingFace Transformers

```python
import torch
from PIL import Image
from transformers import SamModel, SamProcessor

## Load model and processor
model = SamModel.from_pretrained("facebook/sam-vit-huge")
processor = SamProcessor.from_pretrained("facebook/sam-vit-huge")
model.to("cuda")

## Process image with point prompt
image = Image.open("image.jpg")
input_points = [[[450, 600]]]  # Batch of points

inputs = processor(image, input_points=input_points, return_tensors="pt")
inputs = {k: v.to("cuda") for k, v in inputs.items()}

## Generate masks
with torch.no_grad():
    outputs = model(**inputs)

## Post-process masks to original size
masks = processor.image_processor.post_process_masks(
    outputs.pred_masks.cpu(),
    inputs["original_sizes"].cpu(),
    inputs["reshaped_input_sizes"].cpu()
)
```

### Core concepts

#### Model architecture

```
SAM Architecture:
┌─────────────────┐     ┌─────────────────┐     ┌─────────────────┐
│  Image Encoder  │────▶│ Prompt Encoder  │────▶│  Mask Decoder   │
│     (ViT)       │     │ (Points/Boxes)  │     │ (Transformer)   │
└─────────────────┘     └─────────────────┘     └─────────────────┘
        │                       │                       │
   Image Embeddings      Prompt Embeddings         Masks + IoU
   (computed once)       (per prompt)             predictions
```

#### Model variants

| Model | Checkpoint | Size | Speed | Accuracy |
|-------|------------|------|-------|----------|
| ViT-H | `vit_h` | 2.4 GB | Slowest | Best |
| ViT-L | `vit_l` | 1.2 GB | Medium | Good |
| ViT-B | `vit_b` | 375 MB | Fastest | Good |

#### Prompt types

| Prompt | Description | Use Case |
|--------|-------------|----------|
| Point (foreground) | Click on object | Single object selection |
| Point (background) | Click outside object | Exclude regions |
| Bounding box | Rectangle around object | Larger objects |
| Previous mask | Low-res mask input | Iterative refinement |

### Interactive segmentation

#### Point prompts

```python
## Single foreground point
input_point = np.array([[500, 375]])
input_label = np.array([1])

masks, scores, logits = predictor.predict(
    point_coords=input_point,
    point_labels=input_label,
    multimask_output=True
)

## Multiple points (foreground + background)
input_points = np.array([[500, 375], [600, 400], [450, 300]])
input_labels = np.array([1, 1, 0])  # 2 foreground, 1 background

masks, scores, logits = predictor.predict(
    point_coords=input_points,
    point_labels=input_labels,
    multimask_output=False  # Single mask when prompts are clear
)
```

#### Box prompts

```python
## Bounding box [x1, y1, x2, y2]
input_box = np.array([425, 600, 700, 875])

masks, scores, logits = predictor.predict(
    box=input_box,
    multimask_output=False
)
```

#### Combined prompts

```python
## Box + points for precise control
masks, scores, logits = predictor.predict(
    point_coords=np.array([[500, 375]]),
    point_labels=np.array([1]),
    box=np.array([400, 300, 700, 600]),
    multimask_output=False
)
```

#### Iterative refinement

```python
## Initial prediction
masks, scores, logits = predictor.predict(
    point_coords=np.array([[500, 375]]),
    point_labels=np.array([1]),
    multimask_output=True
)

## Refine with additional point using previous mask
masks, scores, logits = predictor.predict(
    point_coords=np.array([[500, 375], [550, 400]]),
    point_labels=np.array([1, 0]),  # Add background point
    mask_input=logits[np.argmax(scores)][None, :, :],  # Use best mask
    multimask_output=False
)
```

### Automatic mask generation

#### Basic automatic segmentation

```python
from segment_anything import SamAutomaticMaskGenerator

## Create generator
mask_generator = SamAutomaticMaskGenerator(sam)

## Generate all masks
masks = mask_generator.generate(image)

## Each mask contains:
## - segmentation: binary mask
## - bbox: [x, y, w, h]
## - area: pixel count
## - predicted_iou: quality score
## - stability_score: robustness score
## - point_coords: generating point
```

#### Customized generation

```python
mask_generator = SamAutomaticMaskGenerator(
    model=sam,
    points_per_side=32,          # Grid density (more = more masks)
    pred_iou_thresh=0.88,        # Quality threshold
    stability_score_thresh=0.95,  # Stability threshold
    crop_n_layers=1,             # Multi-scale crops
    crop_n_points_downscale_factor=2,
    min_mask_region_area=100,    # Remove tiny masks
)

masks = mask_generator.generate(image)
```

#### Filtering masks

```python
## Sort by area (largest first)
masks = sorted(masks, key=lambda x: x['area'], reverse=True)

## Filter by predicted IoU
high_quality = [m for m in masks if m['predicted_iou'] > 0.9]

## Filter by stability score
stable_masks = [m for m in masks if m['stability_score'] > 0.95]
```

### Batched inference

#### Multiple images

```python
## Process multiple images efficiently
images = [cv2.imread(f"image_{i}.jpg") for i in range(10)]

all_masks = []
for image in images:
    predictor.set_image(image)
    masks, _, _ = predictor.predict(
        point_coords=np.array([[500, 375]]),
        point_labels=np.array([1]),
        multimask_output=True
    )
    all_masks.append(masks)
```

#### Multiple prompts per image

```python
## Process multiple prompts efficiently (one image encoding)
predictor.set_image(image)

## Batch of point prompts
points = [
    np.array([[100, 100]]),
    np.array([[200, 200]]),
    np.array([[300, 300]])
]

all_masks = []
for point in points:
    masks, scores, _ = predictor.predict(
        point_coords=point,
        point_labels=np.array([1]),
        multimask_output=True
    )
    all_masks.append(masks[np.argmax(scores)])
```

### ONNX deployment

#### Export model

```bash
python scripts/export_onnx_model.py \
    --checkpoint sam_vit_h_4b8939.pth \
    --model-type vit_h \
    --output sam_onnx.onnx \
    --return-single-mask
```

#### Use ONNX model

```python
import onnxruntime

## Load ONNX model
ort_session = onnxruntime.InferenceSession("sam_onnx.onnx")

## Run inference (image embeddings computed separately)
masks = ort_session.run(
    None,
    {
        "image_embeddings": image_embeddings,
        "point_coords": point_coords,
        "point_labels": point_labels,
        "mask_input": np.zeros((1, 1, 256, 256), dtype=np.float32),
        "has_mask_input": np.array([0], dtype=np.float32),
        "orig_im_size": np.array([h, w], dtype=np.float32)
    }
)
```

### Common workflows

#### Workflow 1: Annotation tool

```python
import cv2

## Load model
predictor = SamPredictor(sam)
predictor.set_image(image)

def on_click(event, x, y, flags, param):
    if event == cv2.EVENT_LBUTTONDOWN:
        # Foreground point
        masks, scores, _ = predictor.predict(
            point_coords=np.array([[x, y]]),
            point_labels=np.array([1]),
            multimask_output=True
        )
        # Display best mask
        display_mask(masks[np.argmax(scores)])
```

#### Workflow 2: Object extraction

```python
def extract_object(image, point):
    """Extract object at point with transparent background."""
    predictor.set_image(image)

    masks, scores, _ = predictor.predict(
        point_coords=np.array([point]),
        point_labels=np.array([1]),
        multimask_output=True
    )

    best_mask = masks[np.argmax(scores)]

    # Create RGBA output
    rgba = np.zeros((image.shape[0], image.shape[1], 4), dtype=np.uint8)
    rgba[:, :, :3] = image
    rgba[:, :, 3] = best_mask * 255

    return rgba
```

#### Workflow 3: Medical image segmentation

```python
## Process medical images (grayscale to RGB)
medical_image = cv2.imread("scan.png", cv2.IMREAD_GRAYSCALE)
rgb_image = cv2.cvtColor(medical_image, cv2.COLOR_GRAY2RGB)

predictor.set_image(rgb_image)

## Segment region of interest
masks, scores, _ = predictor.predict(
    box=np.array([x1, y1, x2, y2]),  # ROI bounding box
    multimask_output=True
)
```

### Output format

#### Mask data structure

```python
## SamAutomaticMaskGenerator output
{
    "segmentation": np.ndarray,  # H×W binary mask
    "bbox": [x, y, w, h],        # Bounding box
    "area": int,                 # Pixel count
    "predicted_iou": float,      # 0-1 quality score
    "stability_score": float,    # 0-1 robustness score
    "crop_box": [x, y, w, h],    # Generation crop region
    "point_coords": [[x, y]],    # Input point
}
```

#### COCO RLE format

```python
from pycocotools import mask as mask_utils

## Encode mask to RLE
rle = mask_utils.encode(np.asfortranarray(mask.astype(np.uint8)))
rle["counts"] = rle["counts"].decode("utf-8")

## Decode RLE to mask
decoded_mask = mask_utils.decode(rle)
```

### Performance optimization

#### GPU memory

```python
## Use smaller model for limited VRAM
sam = sam_model_registry["vit_b"](checkpoint="sam_vit_b_01ec64.pth")

## Process images in batches
## Clear CUDA cache between large batches
torch.cuda.empty_cache()
```

#### Speed optimization

```python
## Use half precision
sam = sam.half()

## Reduce points for automatic generation
mask_generator = SamAutomaticMaskGenerator(
    model=sam,
    points_per_side=16,  # Default is 32
)

## Use ONNX for deployment
## Export with --return-single-mask for faster inference
```

### Common issues

| Issue | Solution |
|-------|----------|
| Out of memory | Use ViT-B model, reduce image size |
| Slow inference | Use ViT-B, reduce points_per_side |
| Poor mask quality | Try different prompts, use box + points |
| Edge artifacts | Use stability_score filtering |
| Small objects missed | Increase points_per_side |

### References

- **[Advanced Usage](references/advanced-usage.md)** - Batching, fine-tuning, integration
- **[Troubleshooting](references/troubleshooting.md)** - Common issues and solutions

### Resources

- **GitHub**: https://github.com/facebookresearch/segment-anything
- **Paper**: https://arxiv.org/abs/2304.02643
- **Demo**: https://segment-anything.com
- **SAM 2 (Video)**: https://github.com/facebookresearch/segment-anything-2
- **HuggingFace**: https://huggingface.co/facebook/sam-vit-huge


---

## Module 3: `stable-diffusion-image-generation`

- **Origine :** `01_Hermes_Skills_Core_Library\mlops\models\stable-diffusion\SKILL.md`
- **Rôle / Objectif :** State-of-the-art text-to-image generation with Stable Diffusion models via HuggingFace Diffusers. Use when generating images from text prompts, performing image-to-image translation, inpainting, or building custom diffusion pipelines.

## Stable Diffusion Image Generation

Comprehensive guide to generating images with Stable Diffusion using the HuggingFace Diffusers library.

### When to use Stable Diffusion

**Use Stable Diffusion when:**
- Generating images from text descriptions
- Performing image-to-image translation (style transfer, enhancement)
- Inpainting (filling in masked regions)
- Outpainting (extending images beyond boundaries)
- Creating variations of existing images
- Building custom image generation workflows

**Key features:**
- **Text-to-Image**: Generate images from natural language prompts
- **Image-to-Image**: Transform existing images with text guidance
- **Inpainting**: Fill masked regions with context-aware content
- **ControlNet**: Add spatial conditioning (edges, poses, depth)
- **LoRA Support**: Efficient fine-tuning and style adaptation
- **Multiple Models**: SD 1.5, SDXL, SD 3.0, Flux support

**Use alternatives instead:**
- **DALL-E 3**: For API-based generation without GPU
- **Midjourney**: For artistic, stylized outputs
- **Imagen**: For Google Cloud integration
- **Leonardo.ai**: For web-based creative workflows

### Quick start

#### Installation

```bash
pip install diffusers transformers accelerate torch
pip install xformers  # Optional: memory-efficient attention
```

#### Basic text-to-image

```python
from diffusers import DiffusionPipeline
import torch

## Load pipeline (auto-detects model type)
pipe = DiffusionPipeline.from_pretrained(
    "stable-diffusion-v1-5/stable-diffusion-v1-5",
    torch_dtype=torch.float16
)
pipe.to("cuda")

## Generate image
image = pipe(
    "A serene mountain landscape at sunset, highly detailed",
    num_inference_steps=50,
    guidance_scale=7.5
).images[0]

image.save("output.png")
```

#### Using SDXL (higher quality)

```python
from diffusers import AutoPipelineForText2Image
import torch

pipe = AutoPipelineForText2Image.from_pretrained(
    "stabilityai/stable-diffusion-xl-base-1.0",
    torch_dtype=torch.float16,
    variant="fp16"
)
pipe.to("cuda")

## Enable memory optimization
pipe.enable_model_cpu_offload()

image = pipe(
    prompt="A futuristic city with flying cars, cinematic lighting",
    height=1024,
    width=1024,
    num_inference_steps=30
).images[0]
```

### Architecture overview

#### Three-pillar design

Diffusers is built around three core components:

```
Pipeline (orchestration)
├── Model (neural networks)
│   ├── UNet / Transformer (noise prediction)
│   ├── VAE (latent encoding/decoding)
│   └── Text Encoder (CLIP/T5)
└── Scheduler (denoising algorithm)
```

#### Pipeline inference flow

```
Text Prompt → Text Encoder → Text Embeddings
                                    ↓
Random Noise → [Denoising Loop] ← Scheduler
                      ↓
               Predicted Noise
                      ↓
              VAE Decoder → Final Image
```

### Core concepts

#### Pipelines

Pipelines orchestrate complete workflows:

| Pipeline | Purpose |
|----------|---------|
| `StableDiffusionPipeline` | Text-to-image (SD 1.x/2.x) |
| `StableDiffusionXLPipeline` | Text-to-image (SDXL) |
| `StableDiffusion3Pipeline` | Text-to-image (SD 3.0) |
| `FluxPipeline` | Text-to-image (Flux models) |
| `StableDiffusionImg2ImgPipeline` | Image-to-image |
| `StableDiffusionInpaintPipeline` | Inpainting |

#### Schedulers

Schedulers control the denoising process:

| Scheduler | Steps | Quality | Use Case |
|-----------|-------|---------|----------|
| `EulerDiscreteScheduler` | 20-50 | Good | Default choice |
| `EulerAncestralDiscreteScheduler` | 20-50 | Good | More variation |
| `DPMSolverMultistepScheduler` | 15-25 | Excellent | Fast, high quality |
| `DDIMScheduler` | 50-100 | Good | Deterministic |
| `LCMScheduler` | 4-8 | Good | Very fast |
| `UniPCMultistepScheduler` | 15-25 | Excellent | Fast convergence |

#### Swapping schedulers

```python
from diffusers import DPMSolverMultistepScheduler

## Swap for faster generation
pipe.scheduler = DPMSolverMultistepScheduler.from_config(
    pipe.scheduler.config
)

## Now generate with fewer steps
image = pipe(prompt, num_inference_steps=20).images[0]
```

### Generation parameters

#### Key parameters

| Parameter | Default | Description |
|-----------|---------|-------------|
| `prompt` | Required | Text description of desired image |
| `negative_prompt` | None | What to avoid in the image |
| `num_inference_steps` | 50 | Denoising steps (more = better quality) |
| `guidance_scale` | 7.5 | Prompt adherence (7-12 typical) |
| `height`, `width` | 512/1024 | Output dimensions (multiples of 8) |
| `generator` | None | Torch generator for reproducibility |
| `num_images_per_prompt` | 1 | Batch size |

#### Reproducible generation

```python
import torch

generator = torch.Generator(device="cuda").manual_seed(42)

image = pipe(
    prompt="A cat wearing a top hat",
    generator=generator,
    num_inference_steps=50
).images[0]
```

#### Negative prompts

```python
image = pipe(
    prompt="Professional photo of a dog in a garden",
    negative_prompt="blurry, low quality, distorted, ugly, bad anatomy",
    guidance_scale=7.5
).images[0]
```

### Image-to-image

Transform existing images with text guidance:

```python
from diffusers import AutoPipelineForImage2Image
from PIL import Image

pipe = AutoPipelineForImage2Image.from_pretrained(
    "stable-diffusion-v1-5/stable-diffusion-v1-5",
    torch_dtype=torch.float16
).to("cuda")

init_image = Image.open("input.jpg").resize((512, 512))

image = pipe(
    prompt="A watercolor painting of the scene",
    image=init_image,
    strength=0.75,  # How much to transform (0-1)
    num_inference_steps=50
).images[0]
```

### Inpainting

Fill masked regions:

```python
from diffusers import AutoPipelineForInpainting
from PIL import Image

pipe = AutoPipelineForInpainting.from_pretrained(
    "runwayml/stable-diffusion-inpainting",
    torch_dtype=torch.float16
).to("cuda")

image = Image.open("photo.jpg")
mask = Image.open("mask.png")  # White = inpaint region

result = pipe(
    prompt="A red car parked on the street",
    image=image,
    mask_image=mask,
    num_inference_steps=50
).images[0]
```

### ControlNet

Add spatial conditioning for precise control:

```python
from diffusers import StableDiffusionControlNetPipeline, ControlNetModel
import torch

## Load ControlNet for edge conditioning
controlnet = ControlNetModel.from_pretrained(
    "lllyasviel/control_v11p_sd15_canny",
    torch_dtype=torch.float16
)

pipe = StableDiffusionControlNetPipeline.from_pretrained(
    "stable-diffusion-v1-5/stable-diffusion-v1-5",
    controlnet=controlnet,
    torch_dtype=torch.float16
).to("cuda")

## Use Canny edge image as control
control_image = get_canny_image(input_image)

image = pipe(
    prompt="A beautiful house in the style of Van Gogh",
    image=control_image,
    num_inference_steps=30
).images[0]
```

#### Available ControlNets

| ControlNet | Input Type | Use Case |
|------------|------------|----------|
| `canny` | Edge maps | Preserve structure |
| `openpose` | Pose skeletons | Human poses |
| `depth` | Depth maps | 3D-aware generation |
| `normal` | Normal maps | Surface details |
| `mlsd` | Line segments | Architectural lines |
| `scribble` | Rough sketches | Sketch-to-image |

### LoRA adapters

Load fine-tuned style adapters:

```python
from diffusers import DiffusionPipeline

pipe = DiffusionPipeline.from_pretrained(
    "stable-diffusion-v1-5/stable-diffusion-v1-5",
    torch_dtype=torch.float16
).to("cuda")

## Load LoRA weights
pipe.load_lora_weights("path/to/lora", weight_name="style.safetensors")

## Generate with LoRA style
image = pipe("A portrait in the trained style").images[0]

## Adjust LoRA strength
pipe.fuse_lora(lora_scale=0.8)

## Unload LoRA
pipe.unload_lora_weights()
```

#### Multiple LoRAs

```python
## Load multiple LoRAs
pipe.load_lora_weights("lora1", adapter_name="style")
pipe.load_lora_weights("lora2", adapter_name="character")

## Set weights for each
pipe.set_adapters(["style", "character"], adapter_weights=[0.7, 0.5])

image = pipe("A portrait").images[0]
```

### Memory optimization

#### Enable CPU offloading

```python
## Model CPU offload - moves models to CPU when not in use
pipe.enable_model_cpu_offload()

## Sequential CPU offload - more aggressive, slower
pipe.enable_sequential_cpu_offload()
```

#### Attention slicing

```python
## Reduce memory by computing attention in chunks
pipe.enable_attention_slicing()

## Or specific chunk size
pipe.enable_attention_slicing("max")
```

#### xFormers memory-efficient attention

```python
## Requires xformers package
pipe.enable_xformers_memory_efficient_attention()
```

#### VAE slicing for large images

```python
## Decode latents in tiles for large images
pipe.enable_vae_slicing()
pipe.enable_vae_tiling()
```

### Model variants

#### Loading different precisions

```python
## FP16 (recommended for GPU)
pipe = DiffusionPipeline.from_pretrained(
    "model-id",
    torch_dtype=torch.float16,
    variant="fp16"
)

## BF16 (better precision, requires Ampere+ GPU)
pipe = DiffusionPipeline.from_pretrained(
    "model-id",
    torch_dtype=torch.bfloat16
)
```

#### Loading specific components

```python
from diffusers import UNet2DConditionModel, AutoencoderKL

## Load custom VAE
vae = AutoencoderKL.from_pretrained("stabilityai/sd-vae-ft-mse")

## Use with pipeline
pipe = DiffusionPipeline.from_pretrained(
    "stable-diffusion-v1-5/stable-diffusion-v1-5",
    vae=vae,
    torch_dtype=torch.float16
)
```

### Batch generation

Generate multiple images efficiently:

```python
## Multiple prompts
prompts = [
    "A cat playing piano",
    "A dog reading a book",
    "A bird painting a picture"
]

images = pipe(prompts, num_inference_steps=30).images

## Multiple images per prompt
images = pipe(
    "A beautiful sunset",
    num_images_per_prompt=4,
    num_inference_steps=30
).images
```

### Common workflows

#### Workflow 1: High-quality generation

```python
from diffusers import StableDiffusionXLPipeline, DPMSolverMultistepScheduler
import torch

## 1. Load SDXL with optimizations
pipe = StableDiffusionXLPipeline.from_pretrained(
    "stabilityai/stable-diffusion-xl-base-1.0",
    torch_dtype=torch.float16,
    variant="fp16"
)
pipe.to("cuda")
pipe.scheduler = DPMSolverMultistepScheduler.from_config(pipe.scheduler.config)
pipe.enable_model_cpu_offload()

## 2. Generate with quality settings
image = pipe(
    prompt="A majestic lion in the savanna, golden hour lighting, 8k, detailed fur",
    negative_prompt="blurry, low quality, cartoon, anime, sketch",
    num_inference_steps=30,
    guidance_scale=7.5,
    height=1024,
    width=1024
).images[0]
```

#### Workflow 2: Fast prototyping

```python
from diffusers import AutoPipelineForText2Image, LCMScheduler
import torch

## Use LCM for 4-8 step generation
pipe = AutoPipelineForText2Image.from_pretrained(
    "stabilityai/stable-diffusion-xl-base-1.0",
    torch_dtype=torch.float16
).to("cuda")

## Load LCM LoRA for fast generation
pipe.load_lora_weights("latent-consistency/lcm-lora-sdxl")
pipe.scheduler = LCMScheduler.from_config(pipe.scheduler.config)
pipe.fuse_lora()

## Generate in ~1 second
image = pipe(
    "A beautiful landscape",
    num_inference_steps=4,
    guidance_scale=1.0
).images[0]
```

### Common issues

**CUDA out of memory:**
```python
## Enable memory optimizations
pipe.enable_model_cpu_offload()
pipe.enable_attention_slicing()
pipe.enable_vae_slicing()

## Or use lower precision
pipe = DiffusionPipeline.from_pretrained(model_id, torch_dtype=torch.float16)
```

**Black/noise images:**
```python
## Check VAE configuration
## Use safety checker bypass if needed
pipe.safety_checker = None

## Ensure proper dtype consistency
pipe = pipe.to(dtype=torch.float16)
```

**Slow generation:**
```python
## Use faster scheduler
from diffusers import DPMSolverMultistepScheduler
pipe.scheduler = DPMSolverMultistepScheduler.from_config(pipe.scheduler.config)

## Reduce steps
image = pipe(prompt, num_inference_steps=20).images[0]
```

### References

- **[Advanced Usage](references/advanced-usage.md)** - Custom pipelines, fine-tuning, deployment
- **[Troubleshooting](references/troubleshooting.md)** - Common issues and solutions

### Resources

- **Documentation**: https://huggingface.co/docs/diffusers
- **Repository**: https://github.com/huggingface/diffusers
- **Model Hub**: https://huggingface.co/models?library=diffusers
- **Discord**: https://discord.gg/diffusers


---

## Module 4: `whisper`

- **Origine :** `01_Hermes_Skills_Core_Library\mlops\models\whisper\SKILL.md`
- **Rôle / Objectif :** OpenAI's general-purpose speech recognition model. Supports 99 languages, transcription, translation to English, and language identification. Six model sizes from tiny (39M params) to large (1550M params). Use for speech-to-text, podcast transcription, or multilingual audio processing. Best for robust, multilingual ASR.

## Whisper - Robust Speech Recognition

OpenAI's multilingual speech recognition model.

### When to use Whisper

**Use when:**
- Speech-to-text transcription (99 languages)
- Podcast/video transcription
- Meeting notes automation
- Translation to English
- Noisy audio transcription
- Multilingual audio processing

**Metrics**:
- **72,900+ GitHub stars**
- 99 languages supported
- Trained on 680,000 hours of audio
- MIT License

**Use alternatives instead**:
- **AssemblyAI**: Managed API, speaker diarization
- **Deepgram**: Real-time streaming ASR
- **Google Speech-to-Text**: Cloud-based

### Quick start

#### Installation

```bash
## Requires Python 3.8-3.11
pip install -U openai-whisper

## Requires ffmpeg
## macOS: brew install ffmpeg
## Ubuntu: sudo apt install ffmpeg
## Windows: choco install ffmpeg
```

#### Basic transcription

```python
import whisper

## Load model
model = whisper.load_model("base")

## Transcribe
result = model.transcribe("audio.mp3")

## Print text
print(result["text"])

## Access segments
for segment in result["segments"]:
    print(f"[{segment['start']:.2f}s - {segment['end']:.2f}s] {segment['text']}")
```

### Model sizes

```python
## Available models
models = ["tiny", "base", "small", "medium", "large", "turbo"]

## Load specific model
model = whisper.load_model("turbo")  # Fastest, good quality
```

| Model | Parameters | English-only | Multilingual | Speed | VRAM |
|-------|------------|--------------|--------------|-------|------|
| tiny | 39M | ✓ | ✓ | ~32x | ~1 GB |
| base | 74M | ✓ | ✓ | ~16x | ~1 GB |
| small | 244M | ✓ | ✓ | ~6x | ~2 GB |
| medium | 769M | ✓ | ✓ | ~2x | ~5 GB |
| large | 1550M | ✗ | ✓ | 1x | ~10 GB |
| turbo | 809M | ✗ | ✓ | ~8x | ~6 GB |

**Recommendation**: Use `turbo` for best speed/quality, `base` for prototyping

### Transcription options

#### Language specification

```python
## Auto-detect language
result = model.transcribe("audio.mp3")

## Specify language (faster)
result = model.transcribe("audio.mp3", language="en")

## Supported: en, es, fr, de, it, pt, ru, ja, ko, zh, and 89 more
```

#### Task selection

```python
## Transcription (default)
result = model.transcribe("audio.mp3", task="transcribe")

## Translation to English
result = model.transcribe("spanish.mp3", task="translate")
## Input: Spanish audio → Output: English text
```

#### Initial prompt

```python
## Improve accuracy with context
result = model.transcribe(
    "audio.mp3",
    initial_prompt="This is a technical podcast about machine learning and AI."
)

## Helps with:
## - Technical terms
## - Proper nouns
## - Domain-specific vocabulary
```

#### Timestamps

```python
## Word-level timestamps
result = model.transcribe("audio.mp3", word_timestamps=True)

for segment in result["segments"]:
    for word in segment["words"]:
        print(f"{word['word']} ({word['start']:.2f}s - {word['end']:.2f}s)")
```

#### Temperature fallback

```python
## Retry with different temperatures if confidence low
result = model.transcribe(
    "audio.mp3",
    temperature=(0.0, 0.2, 0.4, 0.6, 0.8, 1.0)
)
```

### Command line usage

```bash
## Basic transcription
whisper audio.mp3

## Specify model
whisper audio.mp3 --model turbo

## Output formats
whisper audio.mp3 --output_format txt     # Plain text
whisper audio.mp3 --output_format srt     # Subtitles
whisper audio.mp3 --output_format vtt     # WebVTT
whisper audio.mp3 --output_format json    # JSON with timestamps

## Language
whisper audio.mp3 --language Spanish

## Translation
whisper spanish.mp3 --task translate
```

### Batch processing

```python
import os

audio_files = ["file1.mp3", "file2.mp3", "file3.mp3"]

for audio_file in audio_files:
    print(f"Transcribing {audio_file}...")
    result = model.transcribe(audio_file)

    # Save to file
    output_file = audio_file.replace(".mp3", ".txt")
    with open(output_file, "w") as f:
        f.write(result["text"])
```

### Real-time transcription

```python
## For streaming audio, use faster-whisper
## pip install faster-whisper

from faster_whisper import WhisperModel

model = WhisperModel("base", device="cuda", compute_type="float16")

## Transcribe with streaming
segments, info = model.transcribe("audio.mp3", beam_size=5)

for segment in segments:
    print(f"[{segment.start:.2f}s -> {segment.end:.2f}s] {segment.text}")
```

### GPU acceleration

```python
import whisper

## Automatically uses GPU if available
model = whisper.load_model("turbo")

## Force CPU
model = whisper.load_model("turbo", device="cpu")

## Force GPU
model = whisper.load_model("turbo", device="cuda")

## 10-20× faster on GPU
```

### Integration with other tools

#### Subtitle generation

```bash
## Generate SRT subtitles
whisper video.mp4 --output_format srt --language English

## Output: video.srt
```

#### With LangChain

```python
from langchain.document_loaders import WhisperTranscriptionLoader

loader = WhisperTranscriptionLoader(file_path="audio.mp3")
docs = loader.load()

## Use transcription in RAG
from langchain_chroma import Chroma
from langchain_openai import OpenAIEmbeddings

vectorstore = Chroma.from_documents(docs, OpenAIEmbeddings())
```

#### Extract audio from video

```bash
## Use ffmpeg to extract audio
ffmpeg -i video.mp4 -vn -acodec pcm_s16le audio.wav

## Then transcribe
whisper audio.wav
```

### Best practices

1. **Use turbo model** - Best speed/quality for English
2. **Specify language** - Faster than auto-detect
3. **Add initial prompt** - Improves technical terms
4. **Use GPU** - 10-20× faster
5. **Batch process** - More efficient
6. **Convert to WAV** - Better compatibility
7. **Split long audio** - <30 min chunks
8. **Check language support** - Quality varies by language
9. **Use faster-whisper** - 4× faster than openai-whisper
10. **Monitor VRAM** - Scale model size to hardware

### Performance

| Model | Real-time factor (CPU) | Real-time factor (GPU) |
|-------|------------------------|------------------------|
| tiny | ~0.32 | ~0.01 |
| base | ~0.16 | ~0.01 |
| turbo | ~0.08 | ~0.01 |
| large | ~1.0 | ~0.05 |

*Real-time factor: 0.1 = 10× faster than real-time*

### Language support

Top-supported languages:
- English (en)
- Spanish (es)
- French (fr)
- German (de)
- Italian (it)
- Portuguese (pt)
- Russian (ru)
- Japanese (ja)
- Korean (ko)
- Chinese (zh)

Full list: 99 languages total

### Limitations

1. **Hallucinations** - May repeat or invent text
2. **Long-form accuracy** - Degrades on >30 min audio
3. **Speaker identification** - No diarization
4. **Accents** - Quality varies
5. **Background noise** - Can affect accuracy
6. **Real-time latency** - Not suitable for live captioning

### Resources

- **GitHub**: https://github.com/openai/whisper ⭐ 72,900+
- **Paper**: https://arxiv.org/abs/2212.04356
- **Model Card**: https://github.com/openai/whisper/blob/main/model-card.md
- **Colab**: Available in repo
- **License**: MIT


---
