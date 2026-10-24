# Blender game animation: tested lessons

The [September 15–19 character review lessons](overlord-character-animation-reviews.md)
consolidate the later Wild Skeleton, Swordsman, Human Archer and Urs feedback.
Use the [batch restart guide](../projects/overlord/animation-workflow/NEXT_BATCH.md)
for current source locations and the distinction between source and engine work.

## Standard turns from approved clips: Urs and the upright roster

The owner approved the Urs turn mechanics and requested them for Human Archer,
Human Swordsman, Skeleton Warrior, Skeleton Archer and Wild Skeleton on
2026-09-18. The standard pack includes Run Turn Left/Right and Idle Turn
Left/Right. These are normally authored from existing approved movement and
carry poses, without purchasing or generating additional motion references.

A readable upright Idle turn is a 90-degree support change: the leading foot
lands farther outward/back, the chest has visibly turned while the trailing foot
is still planted, then that foot follows. The body shifts over the new support.
Keep arms quiet relative to the chest and preserve sword/shield/bow contact.
Simply rotating the whole body while placing the feet close together hides the
turn from the overhead game camera. Keep individual characters' stance and
proportions; preserve a successful existing turn rather than replacing its carry.

Two failures from the Urs work matter when adapting this motion. First, adding
a bell-shaped chest offset to a changing pelvis yaw can make total chest heading
reverse briefly. Define the chest's absolute heading separately and check both
curves for monotonic motion. Second, a knee pole taken directly from a thigh
vector can flip during a wider backward step. Remove its component along the
reference hip-to-ankle axis first, then project that anatomical bend direction
against the current leg axis. Evaluate between keys and check the real sole.
Use continuous tangents through moving intermediate control points, so each
point does not create a stop-and-go hesitation.

The roster implementation retains 45 frames at 30 fps: first landing 21.5625,
trailing lift 27.1875, final landing 40.3125. The chest is about 83 degrees turned
at the first landing; character-scaled model-space retreat is about 24-29 cm.
These numbers describe this delivery, not universal settings. The deform clips
are counter-transformed; a full Blender/engine preview must apply their sampled
heading and planar travel once. Export both in a hashed sidecar with its basis.

Overlord's approved gameplay separately uses fixed 2x footwork, independently
controlled facing and interruptible movement. Urs applies retreat only to the
visual model. Exact world contacts throughout a complete 1x preview do not imply
contact through arbitrary gameplay interruption; retain the game's timing and
navigation rules when delivering source revisions. Source/export evidence and
receiving-agent instructions are in the
[September 18 roster handoff](../projects/overlord/animation-workflow/roster-turns-2026-09-18/HANDOFF.md).

Recorded 2026-09-09 with the owner's explicit request to preserve the successful wolf workflow. Source: the approved Blender project, production scripts, saved QA reports and chat feedback. Tested authoring environment: Blender 5.1.0. Recheck APIs when the installed version changes.

Use the [animation skill](../.claude/skills/blender-game-animation/SKILL.md) to perform the work and the [full workflow](../processes/3d-ai/blender-game-animation.md) for its sequence. The [wolf case study](../projects/overlord/animation-workflow/README.md) indexes the preserved implementation and evidence.

## Starting poses and model comparison for AI motion references

Added 2026-09-12 with the owner's explicit request to preserve the lessons from the
completed Skeleton Warrior reference selection. Follow the maintained
[reference selection process](../processes/3d-ai/animation-reference-selection.md).

The most useful change was to approve the intended opening stance first and
supply that exact image as the starting frame. A rigging A-pose or a generic
character-reference image often led the video model to begin with the wrong pose
or waste time transitioning into Idle. Correct opening images made Idle, Walk
and Attack comparisons more consistent and preserved the low trailing sword.

Seedance 2.5 supplied six of the eight selected Warrior references: Idle, Run,
the take reassigned to Walk, both Attacks and one Death. MiniMax H3 Max supplied
Stun and the other Death. The owner's current recipe for the next character is two
Seedance 2.5 takes plus one MiniMax H3 Max take per motion, explicitly confirmed
after resolving the spoken "H4" label. This observation is scoped to the Warrior
study and can be revised as models and tasks change. Keep exact model identity
explicit; H4 was not tested in this comparison.

Video-conditioned revisions often copied the incorrect sword path. The final
direct edit C repeated B's low release; the opening-plus-pose version D raised
the hand but kept an awkward blade carry and a long hold. More conditioning is
not proof of a better result. The owner ultimately selected the earlier Current
and A attacks. Preserve candidates and let the user's motion choice determine
the final references instead of privileging the latest generation.

The approved reference pack is not a finished animation library. The selected
Walk still needs a small, unspecified slowdown during game authoring, and
precise contact timing and seamless loops still need Blender/engine work.

## Approved animation composition for ground quadrupeds

On 2026-09-10 the owner approved the playable Wolf revision 07 and explicitly asked
to retain its animation composition as the baseline for future quadrupeds.
For creatures that face their travel direction, start with these nine clips:
Idle, Run, Attack, Death, a separate Walk, Turn Left, Turn Right, Run Turn Left
and Run Turn Right. Add strafe only when gameplay actually needs sideways travel
while facing forward. Combat-ready and flavor actions remain optional.

The successful composition depends on its controller connection:

- Drive straight/left/right Run with one normalized phase from actual planar
  distance. Blend by signed steering curvature without restarting the cycle.
- Use authored inward lean and body bend; remove an existing procedural bank
  when it would add the same lean twice.
- Couple planted footwork and code yaw to the same phase and supplied heading
  curve. Use repeatable steps with Idle-compatible endpoints. Repeated Move
  must not restart them; explicit Stop/Hold, combat and lifecycle interruptions
  retain their authority.
- Author Walk as a distinct gait and select it by requested travel pace. Ordinary
  braking must not cause repeated Walk/Run changes. Gameplay owns attack timing;
  animation samples its contact/recovery clock rather than applying damage.

Wolf's accepted step is 45 degrees over 30 frame intervals at 30 fps, repeated
twice for 90 degrees. Its Run keeps the approved artistic 2 m stride; Walk is
0.68 world m per cycle at visual scale 2. These are Wolf calibrations, not values
to copy to every quadruped. Derive gait, step duration, stride, bank and turning
limits from the next creature's anatomy and game behavior. Slower patrol balance
was not part of this approval.

Evidence: 58 focused runtime assertions passed and 279 sampled poses fit the
renderer bounds before chat acceptance. Visual approval does not establish
perfect planted world contacts: Wolf's native scale-2 Run stride is 1.05 m,
distinct from the retained artistic 2 m calibration; terrain foot IK is absent.
See the [approved contract](../projects/overlord/animation-workflow/quadruped-locomotion.md)
and [runtime review](../projects/overlord/logs/wolf_locomotion_07.html#runtime).

## Rig failures can look like weight failures

Wolf Run folded its hind legs around frames 14-16. The thigh/shin solve approached an extreme fold during high paw recovery. Stable weights alone could not solve it. Correcting the hock trajectory and maintaining usable hip-to-hock separation restored the knee bend. Diagnose the evaluated bones and control trajectories before repainting a mesh whose bones already collapse.

The wolf's structure used two-bone foreleg IK and two-bone thigh/shin IK toward a hock helper under the hind paw control. A separate hock/paw section retained the digitigrade shape. This is a successful structure for this anatomy, not evidence that every quadruped needs the same rig.

Quarter-frame evaluation caught between-key problems that integer poses could miss. After the run refinements, the measured maximum knee bend in that QA's convention was about 117.44 degrees, compared with an earlier near-fold of about 175 degrees. These numbers describe this rig and diagnostic convention; they are not general biological limits.

## Automatic weights need anatomical cleanup

Heat weights were useful for the initial bind. The important corrections were opposite-side limb leakage, shoulder influence into the mane, torso transition bands, jaw/beard separation and disconnected details. Teeth need rigid assignment to the correct upper/lower mouth bone; nearest-surface weighting alone can put a tooth on the wrong moving part.

The nearly symmetric wolf mesh allowed limited mirrored averaging. Match surface counterparts within a tolerance; do not force symmetry across asymmetric geometry. Mild topology smoothing improved transitions, followed by pruning to four influences and normalization. Check again after pruning because a vertex can lose its last useful influence.

The final source mesh had 9,209 welded vertices and 17,835 triangles. glTF used 23,663 vertices because of seams. A higher export vertex count did not imply duplicated character geometry.

## Paw origin is not the floor contact

The paw controller or ankle can be above the sole. Check deformed sole geometry when correcting penetration. Wolf used a small run clearance to cover nonlinear IK interpolation around landing. Choose clearance relative to asset size and inspect it visually; copying millimetre values to a much larger or smaller character can cause floating or sinking.

## Gait asymmetry and body response come after stability

After the collapse was fixed, the owner requested a leading/trailing relationship between the hind legs. The final offsets were 3.6 source frames for rear feet and 2.6 for forefeet at 24 fps. The rear offset is 150 ms. It broke the simultaneous rear-paw bounce while retaining the run cycle.

The upper body used a periodic damped spring response with support/flight forcing. It was allowed to settle over repeated cycles before sampling. Spine/chest response, partial head compensation and delayed tail motion added weight without breaking the repeating cycle. This was procedural secondary animation, not a rigid-body simulation or captured animal biomechanics.

## Reference reconstruction and game motion are separate deliverables

A single camera cannot recover hidden limbs or depth exactly. Preserve reference-guided pose/timing decisions and label inferred motion. Subsequent requested improvements may intentionally depart from the video.

The full Attack and Death were kept. Separate shorter game actions removed long waits while preserving the approved motion. Attack returned to its loaded starting stance so repeated swings could connect. Short Death began with support loss and ended after the impact/settle; corpse lifetime was left to gameplay.

## Count time intervals, not included samples

The attack's frames 0-51 contain 52 samples but 51 time intervals. At 30 fps, duration is 1.7 seconds. Contact at relative frame 39 is 1.3 seconds, or 39/51 = 0.7647058824. FBX reimport displayed 1-52 while preserving that timing. A suffix such as `c39` records the zero-relative contact sample, not a guaranteed absolute importer timeline number.

When cadence is changed to T seconds, scaling the full clip uses speed `1.7/T` and contact time `T*39/51` for this attack. Another attack needs its own event fraction. The user approved the wolf contact in the 75-80% range; do not universalize it across the roster.

The final exports were resampled to 30 fps. Merely setting a scene from 24 to 30 fps would shorten the source loops. The approved durations were preserved: Idle 2.5 s and Run 0.833333 s.

## Playback limits are independent of the selected action

The user's Loop boundary complaint was a real usability problem: a short scene or preview range made longer actions hard to inspect with Play. Removing a marker alone does not solve it. Inspect scene range, preview range, action range and NLA strip settings separately.

The successful solution combined per-clip PLAY scenes with an installed Wolf Action Playback helper that synchronizes selected action range and fps. The helper was scoped to this project rather than rewriting every Blender scene. Native scenes provide a fallback without that add-on.

Blender 5.1 details observed in this project:

- Bind the appropriate action slot explicitly when assigning an action to a copied rig; an action name alone did not establish correct evaluation in all copies.
- Keep copied IK targets local to the copied rig.
- Retain otherwise unused playback scenes with fake users so the saved library survives reopening.
- Use supported pose/selection APIs; assumptions about older bone selection properties failed.

These are version-specific implementation lessons. Check current local APIs before adapting the helper.

## Bake evaluated motion and compare geometry

The author rig had 38 bones, while the game file had 28 and no constraints. The bake retained Root and Body even though they were non-deforming, because they carry the hierarchy and local body motion. Removing all non-deforming bones indiscriminately would lose required transforms.

The export comparison sampled evaluated geometry from the author and reimported clips. Common coordinates and a correspondence that handles seam duplicates are necessary. A raw vertex-index comparison can report false differences after a legitimate format conversion.

The final four-clip handoff was copied to another directory, then both FBX and GLB were reimported in clean scenes. Twenty-one sample poses per format matched within 0.000001 m. Measured maximum differences were approximately 0.0000005615 m for FBX and 0.0000007611 m for GLB. Separate source checks covered interpolation, ground contact and loop seams.

## Texture validation needs actual image loading

The source had one original 4096 x 4096 JPEG base-color image. Export extracted those packed bytes without recompression. FBX used a relative external texture and GLB embedded it. No normal or roughness texture was generated.

Two QA false alarms were fixed in the validator:

1. A packed glTF image reported `has_data=False` before pixel access. Force pixel loading and inspect dimensions/bytes before declaring it broken.
2. Blender's glTF importer generated a BoneShape helper mesh. Count armature-skinned character meshes and inspect the GLB's raw mesh/skin lists before reporting an extra exported character mesh.

The copied-folder test matters: a file can look correct only because Blender resolves a texture from its old working directory. Verify that the external path points inside the copy.

## Keep execution and archives honest

### Blender MCP fallback on the owner's workstation

Confirmed by the owner on 2026-09-14: the regular Blender MCP is enabled and configured to start automatically with Blender. If the Higgsfield Blender connection drops, try the regular Blender MCP before asking him to reconnect anything. If necessary, preserve unsaved work, restart Blender, and reconnect through the regular MCP. Inspect the actual open file and confirm the desired review scene after reconnecting; a connected default startup scene is not the animation review file.

Use the currently exposed regular MCP tools first. A historical raw-socket `execute_code` helper is not interchangeable with every Blender MCP server: in this session it timed out while the exposed `execute_blender_code` tool worked immediately. Verify the active server/protocol rather than assuming the old helper still applies.

The interactive Blender bridge did not preserve Python globals between calls. Long calls could time out while Blender continued. Saved scripts, logs and inspection of running processes avoided duplicate work. Background `--factory-startup` runs isolated export checks from third-party add-ons.

An early archive script can replace a rig, clear weights or rebuild actions. The retained script snapshots document the method; they were not converted into a dependency-free one-command tool. Input geometry, saved intermediates and exact stage matter. Do not rerun the one-time folder migration on the organized output.

Root remained stationary in the wolf's game clips; Body supplied local lunge and collapse. This supports controller-driven RTS movement. The engine still needs its own prefab, material, scale, Animator and combat checks. Record completed Blender/export validation separately from completed Unity integration and from the owner's explicit visual approval.

## Artistic polish and technical fidelity answer different questions

Added 2026-09-11 with the owner's request to study Mariel Cartwright's [Skullgirls talk](https://www.youtube.com/watch?v=Mw0h9WmBlsw) and improve the workflow. The [timestamped analysis](../projects/overlord/animation-workflow/skullgirls-polish.md) records source coverage; the [new polish pass](../processes/3d-ai/game-animation-polish.md) is our proposed 3D/RTS application, not a new production result.

A reliable rig, grounded feet and a faithful export do not establish that a strike reads strongly. Add a separate normal-speed assessment from the actual game camera: pose separation, body loading, release contrast, visible contact and usable recovery. Judge these before increasing detail. Dense samples preserve the authored motion; they cannot supply missing emphasis.

Keep authored poses, pose exposure, timeline fps, bake density and the gameplay clock distinct. Do not translate fewer sprite drawings into sparse runtime keys or a shorter locked cadence. An emphasized pose need not become a static pause: ongoing compression can preserve the silhouette while preparing a sharp release. Delayed secondary motion should explain a change in the leading mass, not add independent wobble everywhere.

Observed Scorpid revision-06 evidence: the user enlarged 176 mesh vertices; the subsequent attack pulse produced approximately 2.05–2.09 times the new distal base width at contact. The 1.6-second cadence and frame-37 event were preserved. Neutral scale keys prevented carryover into other actions, and the nonuniform pulse survived copied-folder FBX/GLB comparisons. These measurements support this implementation, not a universal scale factor. [Attack checks](../projects/overlord/scorpid-animation-06/qa/attack_validation_06.json).

The wider mesh initially penetrated the floor in Death even though its curves were unchanged. Correcting only Tail.11 rotation restored approximately 4 mm of clearance; the remaining Death channels and timing stayed intact. Mesh edits therefore require checks of deformed surfaces across affected clips, not only a curve-preservation assertion. [Clearance evidence](../projects/overlord/scorpid-animation-06/qa/death_geometry_clearance_06.json).

## Partial Actions can inherit transforms when switching clips

Adding fully keyed Swordsman Idle/Stun exposed an existing omission: older Actions had no finger channels, so switching from the new curled-hand pose left those rotations active. A fresh FBX export/reimport comparison caught approximately 100 mm of finger displacement, despite unchanged legacy keyframe fingerprints. Capture the approved default transforms, add constant channels only where a legacy Action lacks them, and preserve every existing keyed curve. Verify the old poses after first evaluating the new Action, then repeat portable export comparison. Do not assume an unkeyed channel resets when an Action changes. The Swordsman evidence is in `ArtSource/Characters/HumanSwordsman/Source/Animation/IdleStun01/action_defaults.json`.

Overshoot must agree with the game's actual contact event. A striking surface that crosses the target early creates a mismatch even if the pose looks stronger. Hitstop also needs its own engine contract; do not hide extra delays in a clip or freeze an entire RTS simulation as an incidental art change. Neither overshoot experiments nor hitstop were implemented by this research task.

## Warrior review: reach, grip and elbow planes

Observed 2026-09-12 during the first Skeleton Warrior motion review. A grounded
foot and zero loop seam error did not prevent a crouched-looking gait. Raising
the pelvis alone overreached the legs. Shortening the Run stride while preserving
cadence, then solving a reachable pelvis height, reduced mean stance knee bend
from 61.4 to 28.8 degrees. Update stride-distance metadata whenever this changes;
the revised 1.5 m / 0.6 s Run needs 1.4x sampling for 3.5 m/s at visual scale 1.

Inspect the actual hand and handle in close-up. The first finger curl used an
axis that swept the grouped fingers along the sword instead of around the hilt.
Correct palm-relative curl and an editable prop-bone offset seated the grip.
For attack repairs, preserve the successful torso and support curves, expand
the hand's wind-up path and choose the elbow's anatomical bend plane explicitly.
Do not try to fix a cramped arm path by increasing IK iterations.

In Blender 5.1, `Bone.vector` used parent-relative head/tail coordinates in this
rig. The armature-space rest direction needed by the orientation calculation is
`bone.tail_local - bone.head_local`. Mixing them rotated the shield and shoulder
plate incorrectly despite plausible matrix arithmetic. Verify vectors against
inspected joint positions. A rigid shoulder shell can follow an independent
bone with partial arm swing rather than inheriting the humerus's full axial twist.

Key neutral defaults in every action for controls introduced during a revision.
Unkeyed shoulder poses carried from Stun into other actions on the author rig,
while separate playback copies started neutral. Comparing the copies exposed
the mismatch; explicit default keys restored all 24 comparisons. Ordinary Play
must also be exercised after changing actions on the same rig: correct per-scene
ranges alone do not cover that workflow. Evidence is retained in
`projects/overlord/skeleton-animation/warrior-animation-01/revision-02/` and the
canonical Skeletons `Review/ArmPosture02/` folder. Artistic approval remains separate.

## Clarify rotation against a demonstrated pose; do not translate the joint

The revision-02 Warrior arm was rejected: "elbow inward" had been interpreted
as a medial pole direction, pulling the elbow into the ribs. The owner meant an
ordinary hanging arm with the palm facing forward. He supplied a live unsaved
pose, which was captured from its actual Blender process and saved as a separate
backup before closing that window. The saved original file would have missed it.

Revision 03 copies the captured local shoulder, humerus, forearm and hand pose.
It uses editable FK sword-arm keys and a larger outside attack lift with torso
turn. Feet and the shield arm keep their existing controls. Preserve successful
strike poses while repairing preparation; confirm connected joints through
interpolated frames. Reset unused FK transforms before sampling an IK baseline:
otherwise pose state from another action can change the evaluated elbow roll.
Tag all playback rigs and meshes for dependency updates after changing shared
constraints or weights; a stale shoulder-plate evaluation initially disagreed
with identical pose data until refreshed. All 24 comparisons then passed.

The captured pose matches within floating-point error, 3,020 other curves are
unchanged, and the two contact matrices match within 0.00002 armature units.
These checks support the correction; the owner still needs to judge its motion.
Evidence: `projects/overlord/skeleton-animation/warrior-animation-01/revision-03/`.


## Human mocap substitutes must preserve the approved source contract

On 2026-09-13 the owner rejected Human Mocap revision 01: replacing a skeleton
with a human did not authorize a frontal camera, wider stance, smaller props
or rewritten motion prompts. A later acceptance of the shown human was not a
reason to discard the original matching requirement. Revision 02 restores the
three original per-motion poses and elevated isometric view, preserves original
models/settings/media roles, and records only anatomy substitutions as a prompt
diff. In particular, Stun originally used an identity image, not a start frame.

When editing a pose with a second human identity reference, the image model can
copy that second image's camera and stance. Check actual output joint positions,
props and view against the original before launching the video batch. Reject
front-view drift and remaining skeletal hands/feet. Same prompts still produce
different choreography; distinguish source parity, sampled visual inspection,
user motion selection and a successful mocap extraction. Evidence is in
`projects/overlord/skeleton-animation/human-mocap-02/`.


## Decide reference authoring versus human mocap before choosing the camera

The owner's follow-up on 2026-09-13: normally try the animation on the actual
character first, choose the motions that work, then optionally regenerate the
selected finals on a human for mocap. Human-first generation is equally available
when that better serves the task. Remind him of both options and ask which route
he wants if the session has not settled it: human for mocap, or character motion
reference for GPT/animation authoring. Do not turn this reminder into repeated
approval requests after the route has already been chosen.

The camera angle is a separate open choice from the starting body pose. It should
serve the intended downstream use; three-quarter/isometric is not mandatory.
The previous correction preserved the original camera because that specific task
was to reproduce the selected references with only the performer replaced.
That does not establish a universal mocap camera. A new camera experiment is
valid when explicitly chosen and labelled; silently changing the camera during
a matched transfer was the error.

Human Mocap revision 02 used the same coral/teal human in three source-matched
poses, original full-sized equipment, anatomy-only prompt edits, original winning
models/settings and two takes per eight sources. Stun kept its original identity
image role. Sixteen outputs were generated and inspected through sampled frames;
QuickMagic extraction and Mixamo-compatible FBX delivery remain untested. A human
version may help when a service does not recognize a stylized skeleton, but this
run does not prove capture quality. Test the chosen service/view on a selected
clip before relying on the full batch. The maintained recipe is in
[animation reference selection](../processes/3d-ai/animation-reference-selection.md).

## Turn exits need a matching gait phase, not only a longer blend

The owner accepted the Urs result and made it the upright-unit integration standard
on September 18, 2026. Resuming a background Run phase can swap the leading foot
after a partly completed turn. Match the currently visible feet/knees to a baked
Run/Walk pose, then advance by distance. Calibrate and verify once per character
rig/clip set; rebuild when sources change. The [maintained standard](overlord-upright-locomotion.md)
covers scope, current rollout, performance and review checks. Animals are a
separate case, and the current Urs movement parameters are not global defaults.

## Dryad: rooted waves and donor intake

September 24, 2026. Use the [tested exact-ID Mixamo downloader](mixamo-animation-acquisition.md)
before requesting another manual download. Source previews alone are insufficient,
but local absence does not mean the FBX cannot be retrieved.

Dryad's Mixamo-named `RightUpLeg` is a lower trunk, not a human leg. Keep roots
planted during body sway by compensating both its inherited orientation and pivot
translation. Check actual deformed branch surfaces, including separate root meshes;
bone tips alone missed underground geometry. Use fixed per-chain limits over a
whole cycle instead of frame-by-frame clipping, which can introduce a visible hitch.

The original brief prohibited new bones/weights. The owner's later request for
movement in the previously rigid lower roots authorized an additive extension:
15 three-bone chains and `base` weights only. Original rest bones, body/leaf skin,
geometry and UVs stayed unchanged. Do not generalize that exception to other rigs.

For arm retargeting between different rest inclinations, calibrate the rest-axis
correction once. Recomputing shortest-arc aim per frame can flip roll around an
opposite direction. When the donor itself has unsuitable abrupt gestures, use its
main poses with a smooth path as authorized; do not disguise a bad retarget by
blindly filtering all channels. Verify the resulting anatomy in Blender.

A cast can remain one Action with explicit preparation, a repeatable internal
channel and release. Match the channel endpoints and test its actual preview
range. In Blender, enable `use_preview_range` before setting its bounds: enabling
it afterward can reset a requested nonzero start. Dryad uses 40–87 with closure 88;
these numbers are character-specific, not a universal cast timing.
