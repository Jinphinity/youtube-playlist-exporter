# GASP ALS Master Specification & Usage Guide

**Last Updated:** July 2025 (Based on UE 5.6 Update)  
**Project Goal:** To integrate the Advanced Locomotion System (ALS) layering and overlay features into Epic's Game Animation Sample Project (GASP), effectively creating "ALS V5" based on Motion Matching.

---

## 1. Introduction

GASP ALS is a community-driven project initiated to bring the powerful **Layering System** from Caleb Longmire's ALS to Epic's modern **Motion Matching** based GASP.

The core philosophy is to allow developers to layer upper-body states (holding weapons, items, tools) on top of high-quality motion-matching locomotion, without needing unique motion matching databases for every single item.

### Key Features
*   **Locomotion:** Powered by Unreal Engine's Motion Matching (GASP).
*   **Layering System:** ALS-style overlay system using Linked Anim Layers.
*   **Separated States:** Distinction between **Base Stances** (Masculine, Feminine, Injured) and **Overlay Poses** (Rifle, Pistol, Box).
*   **Camera:** UE 5.6 Gameplay Camera System (First Person & Third Person support).
*   **Physics:** Replicated Ragdoll with "Get Up" animations.
*   **Parkour:** Dynamic traversal (mantling/vaulting) on arbitrary geometry.
*   **Architecture:** Distributed as a **Plugin** for easy integration.

---

## 2. Core Concepts & Glossary

### Unreal Engine Concepts
*   **Motion Matching:** The base locomotion system. It continuously searches a database of animations to find the best frame to play based on the character's trajectory and current pose.
*   **Linked Anim Layers:** A system allowing the Animation Blueprint to "link" in other animation graphs. GASP ALS uses this to slot in weapon poses on top of the base locomotion.
*   **Anim Modifiers:** Python or Blueprint scripts that automate tasks in the Animation Editor. In this project, they are used to automatically generate the specific *Curves* needed for the layering system.
*   **Choosers:** A UE 5 feature (Plugin) used to select assets or values based on context. Used here to select the correct Overlay Data Asset without hardcoding switch statements.

### GASP ALS Specific Concepts
*   **Overlay System:** The framework for handling what the character is holding or doing with their upper body.
*   **Base (Stance):** The fundamental style of movement (e.g., Masculine, Feminine, Injured). Controls the lower body and general posture. (Switched via `Q`).
*   **Pose (Overlay):** The item-specific posture (e.g., Rifle, Pistol, Torch). Controls mostly the upper body and hand positions. (Switched via `E`).
*   **Layering Curves:** Specific float curves added to animation sequences (e.g., `Layering_Arm_L`, `Enable_Spine_Rotation`) that tell the AnimGraph how much of the overlay animation to blend over the base locomotion.

---

## 3. Architecture & Systems

### 3.1 The Overlay System
The system is located in the `OverlaySystem` folder (within the Plugin content). It works by blending an **Overlay Pose** on top of the **Base Locomotion**.

**Evolution of the System:**
*   *Early Versions:* Hardcoded Switch on Enum in the Character Blueprint.
*   *Current Version:* Uses **Choosers**. The Character Blueprint asks the Chooser "I have this Enum State (e.g., Rifle), what Data Asset do I need?" and the Chooser returns the correct Animation Blueprint to link.

### 3.2 Hand IK System
The project uses **FABRIK** nodes to ensure hands align properly with weapons.
*   **Logic:** `GetHandIKTransform` function checks the active overlay item.
*   **Item Sockets:** The system looks for sockets on the *Item's* mesh (e.g., a socket named `Hand_L` on a Rifle mesh).
*   **IK Execution:** The AnimGraph moves the hand bone to match that socket's transform. This ensures that even if the base pose breathes or moves, the hand stays locked to the gun barrel.

### 3.3 Camera System
Updated to use the **UE 5.6 Gameplay Camera System**.
*   **Modes:** Supports Third Person (Right/Left Shoulder) and First Person.
*   **Integration:** First Person mode forces the character into "Strafe" mode so the body turns with the camera.
*   **Input:** Keys `2` and `3` toggle camera modes.

### 3.4 Ragdoll & Physics
*   **Replication:** Ragdoll state is replicated to clients.
*   **Recovery:** Includes logic to smooth out the transition from Ragdoll back to Animation ("Get Up" anims), preventing the mesh from teleporting or snapping.
*   **Optimization:** Ticks post-physics to prevent jittering on retargeted characters.

---

## 4. Usage Guide: Adding a New Overlay (Tutorial)

This section consolidates instructions on how to add a new item (e.g., a Katana) to the system.

### Step 1: Prepare Animations (Poses)
You need static poses (single frame animations) or loopable animations for the state.
*   **Required Poses:** Idle, Walk, Run, Sprint, Aim (if applicable).
*   *Note:* You can reuse poses. For example, `Relaxed` and `Ready` states might share the same `Idle` pose but use different additives.

### Step 2: Apply Anim Modifiers (Curves)
The system relies on curves to know *what* to blend.
1.  Open your Pose Animation.
2.  Window -> Anim Modifiers.
3.  Add the **`CreateLayeringCurves`** modifier.
4.  Right-click and "Apply Modifier".
5.  **Tune the Curves:**
    *   `Layering_Arm_L` / `Layering_Arm_R`: Set to `1.0` to fully override the arm with your pose. Set lower (e.g., `0.5`) to blend.
    *   `Layering_Spine`: Controls how much the spine is affected.
    *   `Enable_Spine_Rotation`: Set to `1.0` if this pose should allow Aim Offsets (looking up/down/left/right) to rotate the spine. Usually `0` for Idle, `1.0` for Aiming.
    *   `Additive_...`: Controls if the momentum from the base locomotion (walking bobbing) applies to the overlay.
    *   **Cleanup:** Remove curves you don't need. *Example:* If your Idle pose shouldn't affect the legs, delete the `Layering_Legs` curves.

### Step 3: Create the Overlay Data Asset & Blueprint
Instead of creating a full AnimBP from scratch, you inherit from the system's base.
1.  Go to `OverlaySystem/Overlays`.
2.  Create a Child Blueprint of `ABP_Overlay_Base` (or `Complex` if you need Aiming states).
3.  Name it (e.g., `ABP_Overlay_Katana`).
4.  In the Class Defaults/Details of this new ABP, assign your Poses (Idle, Walk, Run) to the corresponding slots.

### Step 4: Register the Overlay
1.  **Enum:** Open the Overlay Enumeration (in Blueprints) and add `Katana`.
2.  **Data Asset:** Create a Data Asset for your overlay (referencing your new ABP and the Mesh to spawn).
3.  **Chooser:** Open the `OverlayChooser` table. Add a row:
    *   Input: `Enum == Katana`
    *   Output: Your new `Data Asset`.

### Step 5: Sockets & Attachment
1.  Open the Character Skeleton.
2.  Add a Socket to the hand (e.g., `Overlay_Socket_Katana`).
3.  Position it correctly using a preview mesh.
4.  In your Data Asset (from Step 4), specify this socket name as the attachment point.

---

## 5. Configuration Options

### Base vs. Pose
*   **Base (Q):** Sets the global character style.
    *   *Options:* Masculine, Feminine, Injured.
    *   *Effect:* Changes the "Input Base Pose" into the blending engine.
*   **Pose (E):** Sets the specific item handling.
    *   *Options:* Rifle, Pistol, Box, Torch.
    *   *Effect:* Changes the "Overlay Pose" layer.

### Curve Reference
| Curve Name | Default | Description |
| :--- | :--- | :--- |
| `Layering_Arm_L` | 0.0 - 1.0 | Blends the left arm pose. |
| `Layering_Arm_R` | 0.0 - 1.0 | Blends the right arm pose. |
| `Layering_Spine` | 0.0 - 1.0 | Blends the spine pose. |
| `Layering_Head` | 0.0 - 1.0 | Blends the head rotation. |
| `Enable_Spine_Rotation` | 0.0 / 1.0 | Enables Aim Offset affecting the spine (Look at camera). |
| `Hand_IK_L` | 0.0 / 1.0 | Enables IK for the left hand (snaps to weapon socket). |

---

## 6. Installation (Plugin Method)

As of the latest version, GASP ALS is a Plugin.

1.  **Download:** Get the `GASP` folder from the GitHub release/repo.
2.  **Copy:** Place it in your project's `Plugins/` folder.
3.  **Config:** Merge the provided configuration files (DefaultEngine.ini, etc.) with your project's config to ensure collision channels and input bindings are set up correctly.
4.  **Enable:** Launch Unreal, go to Plugins, and ensure GASP is enabled.

---

## 7. Known Issues & Notes
*   **Retargeting:** Poses from the original ALS (UE4 mannequin) might not perfectly align with the UE5 mannequin, causing slight hand offsets. The IK system mitigates this, but custom poses are recommended for production.
*   **First Person:** The First Person camera is a starting point. It forces "Strafe" mode. It is not a fully-featured FPS framework (no viewmodel arm meshes, uses full body mesh).
*   **Support:** This is a free, community-maintained project. Support is handled via the Community Discord.
