# Mathematical Proof Visualization: Sum of Squares ($1^2 + 2^2 + \dots + n^2$)

This repository contains a mathematically perfect 3D Manim animation demonstrating the geometric proof of the Sum of Squares formula:
$$\sum_{k=1}^{n} k^2 = \frac{n(n+1)(2n+1)}{6}$$

Specifically, the animation visualizes how **six identical step-pyramids** perfectly interlock to tile a solid rectangular cuboid of dimensions $n \times (n+1) \times (2n+1)$, proving that the volume of six pyramids matches the volume of the solid cuboid.

---

## File Structure & Paths

All paths specified below are relative to the root of the workspace directory:

- **Source Code**: `./sum_of_squares.py`
  - The finalized Python script containing the Manim animation definition. It builds $n=3$ step-pyramids and implements the exact mathematical transformations.
- **Compiled Output**: `./media/videos/sum_of_squares/1080p60/SumOfSquaresProof.mp4`
  - The high-definition 60 FPS output video of the flawless 3D interlocking reassembly and 360-degree rotation.
- **Dependency Definitions**: `./requirements.txt`
  - The locked dependencies (`manim` and `numpy`) required to execute the rendering script.

---

## Retrospective: What Worked vs. What Didn't

During the iterative refinement of this 3D rendering project on an Apple Silicon (M2 Max) machine, we navigated several challenges:

### 1. What Didn't Work (OpenGL w/ GPU Renderer)
* **Live Window Rendering vs. File Writing**: Executing Manim with the `--renderer=opengl` flag natively uses OpenGL to communicate with hardware GPU cores. However, by default, it renders only to a live display window rather than writing/overwriting the `.mp4` file on disk unless `--write_to_movie` (`-w`) is explicitly passed. In headless or terminal sessions, this led to successful test reports without actually updating the generated movie file, leaving obsolete buggy files on disk.
* **3D Depth Buffer & Transparency Glitches**: Using semi-transparent cubes (`fill_opacity=0.9`) with an OpenGL depth buffer caused severe transparent depth culling artifacts. Without back-to-front rendering order sorting, internal faces of the pyramids rendered directly on top of closer faces, creating escher-like optical illusions that did not resemble a solid cuboid.

### 2. What Worked (CPU Cairo Renderer)
* **Consistent Video Overwriting**: Running the CPU Cairo renderer via:
  ```bash
  manim -qh sum_of_squares.py SumOfSquaresProof
  ```
  reliably compiled and completely overwrote the final `.mp4` file at `./media/videos/sum_of_squares/1080p60/SumOfSquaresProof.mp4` upon every run.
* **Perfect Depth Sorting**: Cairo manages polygon sorting accurately. When combined with 100% solid opacity (`fill_opacity=1.0`) and solid black cube edges (`set_stroke(color=BLACK)`), it delivered a perfectly solid, straight-edged 3D rectangular cuboid.

---

## Setup & Execution

### Prerequisites
Make sure you have `ffmpeg` and LaTeX installed on your system.

### Installation
We recommend using `uv` (a fast Python package installer) to set up your environment:

1. Create a virtual environment:
   ```bash
   uv venv
   ```
2. Activate the virtual environment:
   ```bash
   source venv/bin/activate
   ```
3. Install the dependencies:
   ```bash
   uv pip install -r requirements.txt
   ```

### Running the Animation
To render the final proof video:
```bash
manim -qh sum_of_squares.py SumOfSquaresProof
```
The finished video will compile and be output to `./media/videos/sum_of_squares/1080p60/SumOfSquaresProof.mp4`.
