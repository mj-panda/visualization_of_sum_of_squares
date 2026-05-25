# Technical Specification: 3D Proof-Without-Words Animation for Sum of Squares

## 1. Objective & Scene Setup
* **Target Engine:** Manim (Community Edition)
* **Class Name:** `SumOfSquaresProof`
* **Camera Configuration:** Initialize the scene in a 3D environment. Set default orientation to `phi = 70 * DEGREES`, `theta = -30 * DEGREES` to give a clear volumetric perspective.
* **Variable Definition:** Set a global parameter $N = 4$ for the visualization scale.

---

## 2. Component Design & Object Generation
Create a parameter-driven factory method `get_pyramid(color_gradient_list)` that constructs a single jagged pyramid representing $\sum_{k=1}^{N} k^2$.

* **Block Primitive:** Use `Cube(side_length=1.0)`. Set stroke thickness to `1.5` with a darker shade of the base color to ensure definition between interlocking block edges.
* **Layer Loops:** For each layer $k$ from $1$ to $N$:
  * Generate a grid of cubes spanning $i \in [0, k-1]$ and $j \in [0, k-1]$.
  * Position each cube at 3D coordinate $(j, -i, -k)$. 
  * *Rationale:* This anchors the top corner of every pyramid copy strictly at the local origin $(0,0,-1)$, creating a predictable pivot point for subsequent transformations.
* **Color Schemes:** Instantiate three distinct copies with high-contrast color palettes:
  * **Pyramid A:** Deep Blue to Cyan gradient (`BLUE_E` to `BLUE_A`)
  * **Pyramid B:** Emerald to Mint gradient (`GREEN_E` to `GREEN_A`)
  * **Pyramid C:** Crimson to Coral gradient (`RED_E` to `RED_A`)

---

## 3. Transformation and Interlocking Logic (Phase Mappings)
To form the final $N \times (N+1) \times (N + \frac{1}{2})$ rectangular cuboid, the script must execute the following sequential spatial states:

### State 1: Initial Spawning
* **Pyramid A:** Positioned at center-left (`SHIFT(LEFT * 4)`).
* **Pyramid B:** Positioned at center (`SHIFT(ORIGIN)`).
* **Pyramid C:** Positioned at center-right (`SHIFT(RIGHT * 4)`).
* *Action:* Fade all three structures in simultaneously over 2 seconds.

### State 2: Preparation for Interlocking (Rotation)
Before translation, Pyramids B and C must reorient to complement the stepped facets of Pyramid A:
* **Pyramid A:** Remains static.
* **Pyramid B Transformation:** Rotate $180^\circ$ around the X-axis, followed by a $90^\circ$ rotation around the Z-axis.
* **Pyramid C Transformation:** Rotate $90^\circ$ around the Y-axis, followed by a $180^\circ$ rotation around the Z-axis.

### State 3: Final Assembly (Translation)
Animate the smooth sliding of the structures into a unified, tight rectangular block at the center of the screen (`ORIGIN`):
* **Pyramid A Target:** Move to `ORIGIN`.
* **Pyramid B Target:** Shift by vector offsets exactly matching the inverted dimensions so its ceiling steps interlock with Pyramid A's floor steps.
* **Pyramid C Target:** Shift diagonally into the remaining wedge-shaped void along the side of the combined A-B structure.
* *Action:* Use `self.play(MoveToTarget(...))` with a `linear` or `smooth` rate modifier over 3 seconds to show the parts fitting perfectly without clipping.

---

## 4. UI Overlays & Camera Choreography
* **Static Text Elements:** Use `.fix_in_frame()` to lock a 2D mathematical overlay in the Upper Left corner:
  * Line 1: `MathTex(r"\sum_{k=1}^{N} k^2")`
  * Line 2 (Delayed Reveal): `MathTex(r"= \frac{N(N+1)(2N+1)}{6}")`
* **Dimension Labels:** Once the blocks are unified into a solid rectangular cuboid, spawn 3D `Line` braces or text labels showing the dimensions of the final box edges:
  * Base Width = $N$
  * Base Length = $N + 1$
  * Height = $2N + 1$ (Note: Representing the full combined height cleanly before dividing by 6 mathematically).
* **Camera Orbit:** Conclude the scene by executing a continuous camera rotation: `self.camera.animate.set_euler_angles(theta=150 * DEGREES, run_time=6, rate_func=linear)`. This ensures the AI generates an animation that proves there are zero empty spaces or overlap anomalies in the combined architecture.
