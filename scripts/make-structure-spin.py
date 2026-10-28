"""Render the looping structure animations used on the Research page.

    brew install pymol ffmpeg
    pip install Pillow numpy
    python3 scripts/make-structure-spin.py

For each entry in STRUCTURES this writes, into assets/:

    <stem>-spin-light.mp4    on the light-mode page background
    <stem>-spin-dark.mp4     on the dark-mode page background
    <stem>-still-light.jpg   first frame of each, for the poster and for
    <stem>-still-dark.jpg      anyone who asks for reduced motion

To add an animation for another project, copy a block in STRUCTURES and give it
a PDB ID, the chains to keep and a colour per chain. Everything else follows.

Things that are easy to get wrong here, all of them learned the hard way:

  * PyMOL exits 0 even when the script inside it raises, so a failed render
    looks like a success. The outer pass counts the PNGs and fails loudly.
  * PyMOL puts its own flags in sys.argv, so a script run as `pymol -cq x.py`
    sees "-cq" as argv[1]. Configuration is passed in the environment instead.
  * PyMOL's bundled Python has no Pillow, so this file runs under the system
    python3 and re-enters itself inside PyMOL for the render pass only.
  * The frame is sized to the volume the molecule sweeps, not its pose at
    frame 0. Spinning about screen-x throws a point at (y, z) out to
    hypot(y, z), so a frame that fits at rest can still clip mid-spin.
  * The loop is seamless because FRAMES x step is exactly 360 degrees and the
    last frame stops one step short of the first.
  * Video, not animated GIF or WebP. A full rotation changes nearly every
    pixel every frame, so formats without motion compensation cannot help:
    animated WebP of this clip came out at 6 MB against ~500 KB for H.264.
"""

import os
import pathlib
import shutil
import subprocess
import urllib.request

import numpy as np

try:
    from pymol import cmd
    IN_PYMOL = True
except ImportError:
    IN_PYMOL = False

# Inside PyMOL, __file__ points at PyMOL's own site-packages rather than at
# this script, so the outer pass hands the real location over in the
# environment. Getting this wrong writes frames into the PyMOL install.
HERE = pathlib.Path(os.environ.get("SPIN_HOME")
                    or pathlib.Path(__file__).resolve().parent)
SITE = HERE.parent
ASSETS = SITE / "assets"
CACHE = HERE / ".pdb-cache"
WORK = HERE / ".spin-work"

# The two page backgrounds, straight from the --bg tokens in assets/style.css.
BACKGROUNDS = {"light": "#fbfcfd", "dark": "#12161b"}

FRAMES = 60          # 60 x 6 deg = 360
RENDER_W = 900       # downscaled to TARGET_W, which also smooths the edges
TARGET_W = 460       # displayed at 240 CSS px, so still crisp on a retina screen
MARGIN = 1.09        # the surface sits a few A outside the atom centres
PAD = 24             # breathing room around the molecule, in render px
FPS = 10             # 60 frames / 10 fps = 6 s per revolution
CRF = 30
TRANSPARENCY = 0.62  # surface only; the cartoon inside stays solid

STRUCTURES = [
    {
        "stem": "il2-receptor",
        "pdb": "2ERJ",
        # 2ERJ holds two copies of the complex (A-D and E-H) plus N-glycans in
        # I-P. One copy, no glycans, is what reads at this size.
        "chains": {
            "D": "#94a2b2",   # IL-2
            "A": "#4292c6",   # CD25   / IL-2R alpha
            "B": "#3a9e8c",   # CD122  / IL-2R beta
            "C": "#c6dbef",   # CD132  / common gamma
        },
        # Spin about screen-y, so whatever points down stays pointing down.
        "axis": "y",
        # Start from IL-2Rbeta's membrane-proximal tip pointing straight down,
        # then roll the camera in the viewing plane to the pose Luke picked
        # from a reference image. The roll was found by rendering a grid of
        # (roll, azimuth) previews and scoring each against that image on
        # where the four chain colours sit, so it is matched rather than
        # eyeballed. Changing either value re-aims the spin, because the
        # animation turns about whatever ends up vertical.
        "down_ref": "B",
        "roll": 120,
        # Cosmetic: which chain starts on the left. Every azimuth is shown.
        "left_right": ["B", "C"],
    },
]


def rgb(h):
    return [int(h[i:i + 2], 16) / 255.0 for i in (1, 3, 5)]


def unit(v):
    return np.asarray(v, float) / np.linalg.norm(v)


def tail_centre(obj, n=12):
    """Mean CA position of a chain's last n residues: its membrane-proximal end."""
    atoms = sorted(cmd.get_model(f"{obj} and name CA").atom,
                   key=lambda a: int(a.resi))
    return np.array([a.coord for a in atoms[-n:]]).mean(0)


def view_rotation(spec, centre):
    """Camera basis putting the down_ref chain's C-terminal tip straight down.

    Returns the 3x3 whose rows are the camera's right, up and toward-viewer
    axes in world coordinates, which is the layout PyMOL's get_view uses.

    `centre` must be the point the camera looks at. Measuring "down" from any
    other origin, such as a different chain's centre of mass, tilts the result
    by the offset between the two.
    """
    down = unit(tail_centre(f"ch{spec['down_ref']}") - centre)
    up = -down

    a, b = spec["left_right"]
    hint = np.array(cmd.centerofmass(f"ch{b}")) - np.array(cmd.centerofmass(f"ch{a}"))
    right = unit(hint - np.dot(hint, up) * up)      # drop the vertical part
    toward = np.cross(right, up)

    roll = np.radians(spec.get("roll", 0))
    if roll:                                        # turn within the viewing plane
        right, up = (np.cos(roll) * right + np.sin(roll) * up,
                     -np.sin(roll) * right + np.cos(roll) * up)
    return np.array([right, up, toward])


def fetch(pdb_id):
    CACHE.mkdir(exist_ok=True)
    path = CACHE / f"{pdb_id.lower()}.cif"
    if not path.exists():
        print(f"  downloading {pdb_id}")
        urllib.request.urlretrieve(
            f"https://files.rcsb.org/download/{pdb_id.upper()}.cif", path)
    return path


def render(spec, theme, outdir):
    cmd.reinitialize()
    cmd.load(str(fetch(spec["pdb"])), "m")
    cmd.remove(f"m and not chain {'+'.join(spec['chains'])}")
    cmd.remove("m and not polymer")
    cmd.remove("solvent")

    # One object per chain so each surface carries its own transparency.
    for ch, hexcol in spec["chains"].items():
        obj = f"ch{ch}"
        cmd.create(obj, f"m and chain {ch}")
        cmd.set_color(f"col{ch}", rgb(hexcol))
        cmd.color(f"col{ch}", obj)
        cmd.show("cartoon", obj)
        cmd.show("surface", obj)
        cmd.set("transparency", TRANSPARENCY, obj)
    cmd.delete("m")

    cmd.set_color("pagebg", rgb(BACKGROUNDS[theme]))
    cmd.bg_color("pagebg")
    cmd.set("ray_opaque_background", 1)
    cmd.set("surface_quality", 0)
    cmd.set("transparency_mode", 2)
    cmd.set("cartoon_smooth_loops", 1)
    cmd.set("cartoon_fancy_helices", 1)
    cmd.set("cartoon_discrete_colors", 0)
    cmd.set("antialias", 2)
    cmd.set("ray_shadows", 0)
    cmd.set("depth_cue", 0)
    cmd.set("specular", 0.18)
    cmd.set("shininess", 50)
    cmd.set("ambient", 0.22)
    cmd.set("direct", 0.50)
    cmd.set("reflect", 0.36)
    cmd.set("light_count", 2)
    cmd.set("orthoscopic", 1)

    xyz = np.array(cmd.get_coords("all"))
    centre = xyz.mean(0)

    R = view_rotation(spec, centre)
    view = list(cmd.get_view())
    view[0:9] = R.flatten().tolist()
    cmd.set_view(view)

    cam = (xyz - centre) @ R.T

    # The spin axis keeps its own screen extent; the other two sweep into each
    # other, so that half-extent is hypot of the pair, not either one alone.
    axis = spec.get("axis", "y")
    if axis == "y":
        half_h = float(np.hypot(cam[:, 0], cam[:, 2]).max()) * MARGIN
        half_v = max(abs(cam[:, 1].min()), abs(cam[:, 1].max())) * MARGIN
    else:
        half_h = max(abs(cam[:, 0].min()), abs(cam[:, 0].max())) * MARGIN
        half_v = float(np.hypot(cam[:, 1], cam[:, 2]).max()) * MARGIN
    height = int(round(RENDER_W * half_v / half_h))

    corners = np.array([[sx * half_h, sy * half_v, 0.0]
                        for sx in (-1, 1) for sy in (-1, 1)])
    for i, w in enumerate(corners @ R + centre):
        cmd.pseudoatom("box", pos=list(map(float, w)), name=f"c{i}")
    cmd.zoom("box", complete=1)
    cmd.delete("box")

    base = cmd.get_view()          # framing settled; every frame starts here
    step = 360.0 / FRAMES
    for i in range(FRAMES):
        cmd.set_view(base)
        cmd.turn(axis, i * step)
        cmd.png(f"{outdir}/f{i:03d}.png", width=RENDER_W, height=height,
                dpi=150, ray=1)


def encode(spec, theme, workdir):
    from PIL import Image

    frames = [Image.open(p).convert("RGB")
              for p in sorted(workdir.glob("f*.png"))]
    W, H = frames[0].size
    panel = np.array([int(BACKGROUNDS[theme][i:i + 2], 16) for i in (1, 3, 5)])

    box = None
    for im in frames:
        diff = np.abs(np.asarray(im, dtype=np.int16) - panel).sum(2)
        ys, xs = np.where(diff > 10)
        b = (xs.min(), ys.min(), xs.max() + 1, ys.max() + 1)
        box = b if box is None else (min(box[0], b[0]), min(box[1], b[1]),
                                     max(box[2], b[2]), max(box[3], b[3]))
    box = (max(0, box[0] - PAD), max(0, box[1] - PAD),
           min(W, box[2] + PAD), min(H, box[3] + PAD))
    cw, ch = box[2] - box[0], box[3] - box[1]

    tw = TARGET_W - TARGET_W % 2           # H.264 needs even dimensions
    th = int(round(ch * TARGET_W / cw));  th -= th % 2

    stage = workdir / "stage"
    stage.mkdir(exist_ok=True)
    for i, im in enumerate(frames):
        im.crop(box).resize((tw, th), Image.LANCZOS).save(f"{stage}/s{i:03d}.png")

    mp4 = ASSETS / f"{spec['stem']}-spin-{theme}.mp4"
    subprocess.run(
        ["ffmpeg", "-y", "-framerate", str(FPS), "-i", f"{stage}/s%03d.png",
         "-an", "-c:v", "libx264", "-pix_fmt", "yuv420p", "-crf", str(CRF),
         "-preset", "slow", "-g", "30", "-movflags", "+faststart", str(mp4)],
        check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

    still = ASSETS / f"{spec['stem']}-still-{theme}.jpg"
    Image.open(f"{stage}/s000.png").save(
        still, quality=86, optimize=True, progressive=True)
    return tw, th, mp4, still


def workdir_for(stem, theme):
    return WORK / f"{stem}-{theme}"


if IN_PYMOL:
    for spec in STRUCTURES:
        for theme in BACKGROUNDS:
            render(spec, theme, workdir_for(spec["stem"], theme))
else:
    shutil.rmtree(WORK, ignore_errors=True)
    for spec in STRUCTURES:
        for theme in BACKGROUNDS:
            workdir_for(spec["stem"], theme).mkdir(parents=True)

    print(f"rendering {len(STRUCTURES) * len(BACKGROUNDS) * FRAMES} frames "
          f"in pymol, this takes a few minutes")
    subprocess.run(["pymol", "-cq", str(pathlib.Path(__file__).resolve())],
                   check=True, env={**os.environ, "SPIN_HOME": str(HERE)})

    # PyMOL exits 0 even when its script raised, so check the output itself.
    for spec in STRUCTURES:
        for theme in BACKGROUNDS:
            n = len(list(workdir_for(spec["stem"], theme).glob("f*.png")))
            if n != FRAMES:
                raise SystemExit(
                    f"pymol produced {n} of {FRAMES} frames for "
                    f"{spec['stem']} ({theme}). Re-run the render pass with "
                    f"`pymol -cq {pathlib.Path(__file__).name}` to see why.")

    for spec in STRUCTURES:
        for theme in BACKGROUNDS:
            tw, th, mp4, still = encode(
                spec, theme, workdir_for(spec["stem"], theme))
            print(f"{spec['pdb']} {theme:5}  {tw}x{th}   "
                  f"{mp4.name}  {mp4.stat().st_size/1024:.0f} KB   "
                  f"{still.name}  {still.stat().st_size/1024:.0f} KB")
            print(f"  markup needs width=\"{tw}\" height=\"{th}\"")
    shutil.rmtree(WORK, ignore_errors=True)
