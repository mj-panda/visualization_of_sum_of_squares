# Technical Specification: 3D Proof-Without-Words Animation for Sum of Squares

## 1. Objective & Scene Setup
* **Target Engine:** Manim (Community Edition)
* **Class Name:** `SumOfSquaresProof`
* **Renderer Configuration:** Use the default CPU-based **Cairo** renderer (without `--renderer=opengl`) to ensure perfect 3D depth-sorting culling and reliable output movie generation on disk.
* **Camera Configuration:** Initialize the scene in a 3D environment. Set default orientation to `phi = 70 * DEGREES`, `theta = -30 * DEGREES` to give a clear volumetric perspective.
* **Variable Definition:** Set a global parameter $N = 3$ (or $N = 4$) for the visualization scale.

---

## 2. Component Design & Object Generation
Create a parameter-driven factory method `get_base_pyramid()` that constructs a single corner-aligned stepped pyramid representing $\sum_{k=1}^{N} k^2$.

* **Block Primitive:** Use `Cube(side_length=1.0)`. 
  * Enforce **`fill_opacity=1.0`** to eliminate transparency depth-sorting glitches in 3D.
  * Set a solid black stroke border (`color=BLACK`, `width=2.0`, `opacity=1.0`) to cleanly distinguish individual block divisions.
* **Pyramid Coordinates:** For each layer $k$ from $1$ to $N$:
  * Generate a grid of cubes spanning $i \in [0, k-1]$ and $j \in [0, k-1]$.
  * Position each cube at 3D integer coordinate $(j, i, k-1)$.
* **Color Scheme:** Use 6 distinct, vibrant, high-contrast colors to easily visualize the 6 individual interlocking pyramids:
  * `RED_E`, `BLUE_E`, `GREEN_E`, `YELLOW_E`, `PURPLE_E`, `ORANGE`

---

## 3. Transformation and Interlocking Logic (Exact Cover Partition)
To form a mathematically flawless, 100% solid, gap-free $N \times (N+1) \times (2N+1)$ rectangular cuboid, the script executes a perfect spatial tiling partition. 

### Exact Coordinate Mappings (for $N=3$):
The 6 step-pyramids are created directly in their final tight interlocking configurations by applying specific $3 \times 3$ rotation matrices and discrete coordinate offsets derived from an exact-cover backtracking solver:

1. **Pyramid 1 (Red)**: Rotation: `[[-1, 0, 0], [0, -1, 0], [0, 0, 1]]`, Offset: `(0, 1, 4)`
2. **Pyramid 2 (Blue)**: Rotation: `[[1, 0, 0], [0, 0, 1], [0, -1, 0]]`, Offset: `(0, 1, 0)`
3. **Pyramid 3 (Green)**: Rotation: `[[0, 1, 0], [1, 0, 0], [0, 0, -1]]`, Offset: `(0, 0, 0)`
4. **Pyramid 4 (Yellow)**: Rotation: `[[0, -1, 0], [0, 0, -1], [1, 0, 0]]`, Offset: `(0, 0, 4)`
5. **Pyramid 5 (Purple)**: Rotation: `[[0, 0, -1], [-1, 0, 0], [0, 1, 0]]`, Offset: `(0, 1, 3)`
6. **Pyramid 6 (Orange)**: Rotation: `[[0, 0, 1], [0, 1, 0], [-1, 0, 0]]`, Offset: `(0, 0, 1)`

### Animation States:
1. **State 1: Single Pyramid**: Spawn the first corner-aligned step pyramid at the origin to establish the geometry.
2. **State 2: Radial Separation (Explosion)**: Duplicate the pyramid 5 times. Center the entire unified $6$-pyramid block at `ORIGIN` and scale it down to `0.35` so the entire assembly fits on screen. Explode all 6 pyramids radially outward by a controlled distance of `2.2` units so they start visibly separated but fully contained inside the camera frame.
3. **State 3: Slow Assembly**: Animate all 6 pyramids simultaneously flying into their mathematically perfect interlocking target coordinates using `self.play(*[MoveToTarget(p) ...])` over a slow, clear **8.0 seconds** run time.

---

## 4. UI Overlays & Camera Choreography
* **Formula Overlay**: Lock a 2D mathematical formula in the Upper Left corner:
  * `\sum_{k=1}^{n} k^2 = \frac{n(n+1)(2n+1)}{6}`
  * Fix this to the frame (`self.add_fixed_in_frame_mobjects(...)`) so it does not move in 3D space.
* **Cinematic 360 Spin**: Once the blocks interlock into the unified solid box, rotate the camera in a full 360-degree circle (`theta = self.camera.get_theta() + 360 * DEGREES`) over a **10-second** duration with a linear rate modifier. This physically showcases the flawlessly packed, gap-free, and straight-edged solid cuboid from all angles.

