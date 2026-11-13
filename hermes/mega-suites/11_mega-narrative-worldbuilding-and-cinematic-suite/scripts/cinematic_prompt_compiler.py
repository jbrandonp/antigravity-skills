"""Cinematic Prompt Compiler for Multi-Model AI Filmmaking.

Inspired by wassermanproductions/slate and lemomo-ai/lemo-opuscar.
Translates screenplay scenes and visual beats into production-ready prompts for:
- Midjourney v6.1 (Concept & Keyframes)
- Runway Gen-3 Alpha & Kling 1.5 (Video generation & camera movement)
- Luma Dream Machine & Minimax Hailuo (Physics-based motion)
- ElevenLabs (Voice direction & audio tags)
- Suno / Udio (Orchestral & diegetic music scoring)
"""

import argparse
import json
import sys
from pathlib import Path
from typing import Any, Dict, List


CAMERA_MOVEMENTS = {
    "dolly_in": "Slow cinematic dolly in towards the subject, increasing dramatic intimacy, steady tracking",
    "tracking": "Lateral tracking shot moving smoothly alongside the character at walking pace",
    "crane_down": "High-angle crane descending gracefully from the canopy to eye level",
    "whip_pan": "Fast whip pan revealing sudden movement in the background, sharp dynamic motion blur",
    "static": "Locked-off tripod shot, zero camera shake, hyper-stable architectural framing",
    "handheld": "Subtle visceral handheld camera movement, slight breathing motion, organic indie film feel",
    "orbit_360": "Smooth 360-degree rotational orbit around the subject, keeping focal point locked",
    "snap_zoom": "Aggressive quick snap zoom focusing sharply on character eyes or key object",
    "trunk_shot": "Extreme low-angle POV shot from inside a container looking up at characters",
}

LIGHTING_SETUPS = {
    "chiaroscuro": "High contrast chiaroscuro lighting, deep textured shadows, piercing directional key light",
    "golden_hour": "Warm low-angle golden hour sunlight, volumetric dust rays, soft amber backlight (3200K)",
    "neon_noir": "Moody cyberpunk neon lighting, rain-slicked specular reflections, vibrant cyan and magenta rim light",
    "overcast": "Soft diffused overcast daylight, flat cinematic shadow roll-off, desaturated cold tones (6500K)",
    "candlelight": "Warm flickering 1800K candlelight, gentle falloff, authentic practical source",
    "rembrandt": "Classic Rembrandt portrait lighting, distinct triangle of light on shadow cheek",
    "venetian_blind": "Hard directional light cutting through Venetian blinds, sharp linear shadow stripes",
    "volumetric_fog": "Dense atmospheric god rays piercing heavy theatrical fog, silhouette backlighting",
}

FILM_STYLES = {
    "deakins": "35mm anamorphic film, Master Prime lenses, naturalistic motivated light, rich Kodak 5219 grain --ar 16:9",
    "fincher": "Clinical razor-sharp digital cinematography, controlled desaturated green-gold palette, precise locked framing",
    "villeneuve": "Brutalist minimalist composition, vast negative space, monolithic scale, atmospheric haze",
    "kubrick": "One-point perspective symmetry, 18mm wide-angle lens, deep depth of field, sterile uncanny atmosphere",
    "wong_kar_wai": "Step-printing motion blur, slow shutter speed, neon emerald and amber palette, melancholic reflections",
    "wes_anderson": "Meticulous symmetrical diorama composition, pastel color-blocked palette, 90-degree snap whip pans",
    "miyazaki": "Studio Ghibli painterly hand-drawn anime aesthetic, lush cumulus clouds, gouache textures, vibrant meadow greens",
    "tarantino": "70s Panavision anamorphic, punchy warm Technicolor saturation, low-angle trunk POV shot",
    "lynch": "Surreal uncanny chiaroscuro, deep crimson velvet shadows, muted midtones, industrial hum atmosphere",
    "moebius": "Jean Giraud Moebius French ligne-claire sci-fi illustration, delicate ink hatching, pastel desert gradient flats",
    "bladerunner2049": "Roger Deakins cinematography, monolithic brutalist architecture, monochromatic amber sandstorm haze",
    "ukiyo_e": "Dynamic Japanese Ukiyo-e woodblock print animation style, crisp ink line work, mineral pigment flats",
    "watercolor": "Dreamy fluid watercolor animation, expressive pigment bleeds, soft paper texture roll-off",
    "adam_curtis": "Raw 16mm archival documentary footage, heavy authentic film emulsion grain, high contrast, stark realism",
    "film_noir": "Classic 1940s black-and-white film noir, heavy silver halide grain, extreme key-to-fill ratio, wet asphalt",
    "retro_anime_90s": "Vintage 1990s cel-shaded cyberpunk anime aesthetic, scanlines, soft chromatic aberration, hand-painted cels",
}


def compile_shot(
    shot_id: str,
    subject: str,
    action: str,
    camera_move: str = "dolly_in",
    lighting: str = "chiaroscuro",
    style: str = "deakins",
    voice_text: str = "",
    bgm_mood: str = "tense orchestral",
) -> Dict[str, Any]:
    """Compile a complete multi-model prompt package for a single shot."""
    cam_desc = CAMERA_MOVEMENTS.get(camera_move, CAMERA_MOVEMENTS["dolly_in"])
    light_desc = LIGHTING_SETUPS.get(lighting, LIGHTING_SETUPS["chiaroscuro"])
    style_desc = FILM_STYLES.get(style, FILM_STYLES["deakins"])

    # Midjourney Keyframe
    mj_prompt = (
        f"Cinematic film still, {subject}, {action}. {light_desc}. {style_desc} --style raw --v 6.1"
    )

    # Runway / Kling Video Prompt
    video_prompt = (
        f"{cam_desc}. {subject} {action}. {light_desc}, atmospheric perspective, 8k resolution, cinematic color grade."
    )

    # ElevenLabs Direction
    audio_prompt = ""
    if voice_text:
        audio_prompt = f'[Tone: Whispered tension, gravelly voice, hesitant pacing, 0.4s pauses between words]: "{voice_text}"'

    # Suno BGM Prompt
    bgm_prompt = f"Dark ambient cinematic underscore, {bgm_mood}, cello drone, subtle sub-bass thud at 40Hz, no drums, tempo 65 BPM."

    return {
        "shot_id": shot_id,
        "subject": subject,
        "action": action,
        "camera_movement": camera_move,
        "lighting": lighting,
        "style": style,
        "prompts": {
            "midjourney_v6": mj_prompt,
            "runway_kling_video": video_prompt,
            "elevenlabs_voice": audio_prompt,
            "suno_bgm": bgm_prompt,
        },
    }


def main():
    parser = argparse.ArgumentParser(description="Multi-Model Cinematic Prompt Compiler (Slate Engine)")
    parser.add_argument("--shot-id", default="SHOT_01", help="Identifier for the shot")
    parser.add_argument("--subject", required=True, help="Main subject or character")
    parser.add_argument("--action", required=True, help="Action happening in the scene")
    parser.add_argument("--camera", default="dolly_in", choices=list(CAMERA_MOVEMENTS.keys()), help="Camera movement style")
    parser.add_argument("--lighting", default="chiaroscuro", choices=list(LIGHTING_SETUPS.keys()), help="Lighting mood")
    parser.add_argument("--style", default="deakins", choices=list(FILM_STYLES.keys()), help="Cinematographic aesthetic style")
    parser.add_argument("--dialogue", default="", help="Optional character dialogue for ElevenLabs")
    parser.add_argument("--bgm", default="tense orchestral", help="BGM mood descriptor for Suno/Udio")
    parser.add_argument("--json", action="store_true", help="Output results in JSON format")
    args = parser.parse_args()

    result = compile_shot(
        shot_id=args.shot_id,
        subject=args.subject,
        action=args.action,
        camera_move=args.camera,
        lighting=args.lighting,
        style=args.style,
        voice_text=args.dialogue,
        bgm_mood=args.bgm,
    )

    if args.json:
        print(json.dumps(result, indent=2, ensure_ascii=False))
    else:
        print("\n" + "=" * 70)
        print(f"🎬 CINEMATIC PROMPT COMPILER — {result['shot_id']}")
        print("=" * 70)
        print(f"Style Reference     : {result['style'].upper()}")
        print(f"Camera Movement     : {result['camera_movement']}")
        print(f"Lighting Setup      : {result['lighting']}")
        print("-" * 70)
        print("\n📸 [1. Midjourney v6.1 Keyframe Prompt]:")
        print(f"   {result['prompts']['midjourney_v6']}")
        print("\n🎥 [2. Runway Gen-3 / Kling 1.5 Video Prompt]:")
        print(f"   {result['prompts']['runway_kling_video']}")
        if result['prompts']['elevenlabs_voice']:
            print("\n🎙️ [3. ElevenLabs Audio Direction]:")
            print(f"   {result['prompts']['elevenlabs_voice']}")
        print("\n🎵 [4. Suno / Udio BGM Score Prompt]:")
        print(f"   {result['prompts']['suno_bgm']}")
        print("=" * 70 + "\n")


if __name__ == "__main__":
    main()
