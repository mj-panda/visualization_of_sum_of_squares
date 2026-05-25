import os
os.environ["TEXMFCNF"] = "/opt/homebrew/Cellar/texlive/20260301/share/texmf-dist/web2c"
os.environ["TEXMFROOT"] = "/opt/homebrew/Cellar/texlive/20260301/share"
from manim import *
import numpy as np

class SumOfSquaresProof(ThreeDScene):
    def construct(self):
        # 1. Objective & Scene Setup
        self.set_camera_orientation(phi=70 * DEGREES, theta=-30 * DEGREES)
        N = 3
        
        # Base cubes for a step pyramid
        def get_base_pyramid():
            cubes = []
            for k in range(1, N + 1):
                for i in range(k):
                    for j in range(k):
                        cubes.append((j, i, k-1))
            return cubes

        base_pyr = get_base_pyramid()
        
        # Mathematical exact-cover partition of a 3x4x7 box
        # These 6 transformations and offsets map 6 pyramids perfectly into the solid block
        solutions = [
            (np.array([[-1, 0, 0], [0, -1, 0], [0, 0, 1]]), (0, 1, 4)),
            (np.array([[1, 0, 0], [0, 0, 1], [0, -1, 0]]), (0, 1, 0)),
            (np.array([[0, 1, 0], [1, 0, 0], [0, 0, -1]]), (0, 0, 0)),
            (np.array([[0, -1, 0], [0, 0, -1], [1, 0, 0]]), (0, 0, 4)),
            (np.array([[0, 0, -1], [-1, 0, 0], [0, 1, 0]]), (0, 1, 3)),
            (np.array([[0, 0, 1], [0, 1, 0], [-1, 0, 0]]), (0, 0, 1))
        ]
        
        # Restore the vibrant, distinct colors to easily visualize the 6 individual interlocking pyramids
        colors = [RED_E, BLUE_E, GREEN_E, YELLOW_E, PURPLE_E, ORANGE]
        
        pyramids = []
        for idx, (rot, offset) in enumerate(solutions):
            # Apply mathematical rotation
            rot_pyr = [np.dot(rot, c) for c in base_pyr]
            
            # Find bounds
            xs, ys, zs = zip(*rot_pyr)
            min_x, max_x = min(xs), max(xs)
            min_y, max_y = min(ys), max(ys)
            min_z, max_z = min(zs), max(zs)
            
            # Shift to 0,0,0 then apply exact interlocking offset
            shifted = [(x - min_x, y - min_y, z - min_z) for x, y, z in rot_pyr]
            final = [(x + offset[0], y + offset[1], z + offset[2]) for x, y, z in shifted]
            
            # Create the Manim VGroup for this pyramid
            pyr_group = VGroup()
            for x, y, z in final:
                cube = Cube(side_length=1.0, fill_opacity=1.0, fill_color=colors[idx])
                # Solid black borders are crucial to distinguish individual cubes
                cube.set_stroke(color=BLACK, width=2.0, opacity=1.0)
                cube.move_to(np.array([x, y, z], dtype=float))
                pyr_group.add(cube)
            
            pyramids.append(pyr_group)
        
        # Assemble them into a full block at origin to define their final interlocking state
        full_block = VGroup(*pyramids)
        full_block.move_to(ORIGIN)
        # Scale the whole block down further (from 0.5 to 0.35) so the exploded parts fit within screen bounds
        full_block.scale(0.35, about_point=ORIGIN)
        
        # Save their assembled target positions for later
        for p in pyramids:
            p.generate_target()
            
        # Explode them outward radially by a tightly controlled distance (reduced from 4.5 to 2.2) to keep them on screen
        for p in pyramids:
            offset = p.get_center() - ORIGIN
            dist = np.linalg.norm(offset)
            if dist > 0:
                p.shift((offset / dist) * 2.2)
        
        # Phase 1: Show a single pyramid to establish the shape
        first_pyr = pyramids[0].copy()
        first_pyr.move_to(ORIGIN)
        self.play(FadeIn(first_pyr), run_time=1.5)
        self.wait(1)
        
        # Add LaTeX formula
        formula = MathTex(
            r"\sum_{k=1}^{n} k^2 = \frac{n(n+1)(2n+1)}{6}",
            font_size=48
        ).to_corner(UL)
        # We must fix formula to camera so it doesn't move in 3D
        self.add_fixed_in_frame_mobjects(formula)
        self.play(Write(formula))
        self.wait(1)
        
        # Phase 2: Show the 6 identical separated pyramids
        self.play(
            ReplacementTransform(first_pyr, pyramids[0]),
            *[FadeIn(p) for p in pyramids[1:]],
            run_time=2
        )
        
        # Slowly pan the camera to view the separated geometry
        self.begin_ambient_camera_rotation(rate=0.2)
        self.wait(3)
        self.stop_ambient_camera_rotation()
        
        # Phase 3: The Assembly!
        # Slow down the assembly animation (run_time=8.0 seconds) so the audience can track the interlocking fit
        self.play(*[MoveToTarget(p) for p in pyramids], run_time=8.0)
        self.wait(1)
        
        # Phase 4: Full 360-degree rotation of the camera to show off the completed solid cuboid
        self.move_camera(
            theta=self.camera.get_theta() + 360 * DEGREES,
            run_time=10.0,
            rate_func=linear
        )
        self.wait(1)
