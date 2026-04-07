"""Procedural and interactive visualization helpers."""

import matplotlib.pyplot as plt
import matplotlib.patches as patches
import matplotlib.tri as mtri
import numpy as np


def _extract_arrays(report):
    points = report["points"]
    eastings = np.array([p["easting"] for p in points])
    northings = np.array([p["northing"] for p in points])
    subsidences = np.array([p["subsidence"] for p in points])
    return eastings, northings, subsidences


def _panel_polygon_xy(report):
    panel_points = report["inputs"]["panel_points"]
    xs = [p["easting"] for p in panel_points]
    ys = [p["northing"] for p in panel_points]
    if panel_points:
        xs.append(panel_points[0]["easting"])
        ys.append(panel_points[0]["northing"])
    return xs, ys


def plot_simple_map(report, save_path=None):
    bounds = report["bounds"]
    inputs = report["inputs"]
    calculated = report["calculated"]
    points = report["points"]

    fig, ax = plt.subplots(figsize=(12, 10))

    if points:
        e, n, s = _extract_arrays(report)
        sc = ax.scatter(e, n, c=s * 1000.0, cmap="RdYlGn_r", s=58, alpha=0.75, edgecolors="black", linewidth=0.35)
        plt.colorbar(sc, ax=ax, label="Subsidence (mm)")

    px, py = _panel_polygon_xy(report)
    ax.plot(px, py, color="navy", linewidth=2.2, label="Panel boundary")

    for p in inputs["panel_points"]:
        ax.add_patch(
            patches.Circle((p["easting"], p["northing"]), bounds["influence_distance"], linewidth=0.9, edgecolor="crimson", facecolor="none", linestyle="--", alpha=0.45)
        )

    ax.plot(inputs["center_easting"], inputs["center_northing"], "r*", markersize=16, label="Panel centroid")
    ax.set_title(
        "Single Seam Subsidence Map\n"
        f"s_max = {calculated['s_max_mm']:.2f} mm | Influence distance = {calculated['influence_distance']:.2f} m"
    )
    ax.set_xlabel("Easting (m)")
    ax.set_ylabel("Northing (m)")
    ax.set_aspect("equal")
    ax.grid(True, alpha=0.25)
    ax.legend(loc="upper right")

    if save_path:
        plt.savefig(save_path, dpi=300, bbox_inches="tight")
    plt.show()


def plot_advanced_view(report, save_path=None):
    points = report["points"]
    if not points:
        print("No influenced grid points were generated.")
        return

    inputs = report["inputs"]
    e, n, s = _extract_arrays(report)
    subs_mm = s * 1000.0
    px, py = _panel_polygon_xy(report)

    fig, axes = plt.subplots(2, 2, figsize=(15, 11))
    fig.suptitle("Single Seam Subsidence Analysis", fontsize=16, fontweight="bold")

    ax1 = axes[0, 0]
    sc = ax1.scatter(e, n, c=subs_mm, cmap="RdYlGn_r", s=52, alpha=0.75, edgecolors="black", linewidth=0.35)
    ax1.plot(px, py, color="navy", linewidth=2.2)
    ax1.set_title("Subsidence Scatter")
    ax1.set_xlabel("Easting (m)")
    ax1.set_ylabel("Northing (m)")
    ax1.set_aspect("equal")
    ax1.grid(True, alpha=0.25)
    plt.colorbar(sc, ax=ax1, label="Subsidence (mm)")

    ax2 = axes[0, 1]
    tri = mtri.Triangulation(e, n)
    ctf = ax2.tricontourf(tri, subs_mm, levels=15, cmap="RdYlGn_r")
    ax2.tricontour(tri, subs_mm, levels=10, colors="black", linewidths=0.4, alpha=0.35)
    ax2.plot(px, py, color="navy", linewidth=2.2)
    ax2.set_title("Subsidence Contour")
    ax2.set_xlabel("Easting (m)")
    ax2.set_ylabel("Northing (m)")
    ax2.set_aspect("equal")
    ax2.grid(True, alpha=0.25)
    plt.colorbar(ctf, ax=ax2, label="Subsidence (mm)")

    ax3 = axes[1, 0]
    ax3.hist(subs_mm, bins=24, color="steelblue", edgecolor="black", alpha=0.8)
    ax3.axvline(subs_mm.mean(), color="crimson", linestyle="--", linewidth=2, label=f"Mean {subs_mm.mean():.2f} mm")
    ax3.axvline(subs_mm.max(), color="darkgreen", linestyle="--", linewidth=2, label=f"Max {subs_mm.max():.2f} mm")
    ax3.set_title("Subsidence Histogram")
    ax3.set_xlabel("Subsidence (mm)")
    ax3.set_ylabel("Count")
    ax3.grid(True, axis="y", alpha=0.25)
    ax3.legend()

    ax4 = axes[1, 1]
    tol = inputs["mesh_spacing"] * 1.5
    profile = [p for p in points if abs(p["northing"] - inputs["center_northing"]) <= tol]
    if profile:
        profile = sorted(profile, key=lambda p: p["easting"])
        pe = [p["easting"] for p in profile]
        ps = [p["subsidence"] * 1000.0 for p in profile]
        ax4.plot(pe, ps, "o-", color="navy", linewidth=2, markersize=4.5)
        ax4.fill_between(pe, ps, color="skyblue", alpha=0.35)
    ax4.set_title("East-West Profile")
    ax4.set_xlabel("Easting (m)")
    ax4.set_ylabel("Subsidence (mm)")
    ax4.grid(True, alpha=0.25)

    fig.tight_layout(rect=[0, 0, 1, 0.97])
    if save_path:
        plt.savefig(save_path, dpi=300, bbox_inches="tight")
    plt.show()


def plot_interactive_map(report):
    points = report["points"]
    if not points:
        print("No influenced points available for interactive visualization.")
        return

    bounds = report["bounds"]
    inputs = report["inputs"]
    e, n, s = _extract_arrays(report)

    fig, ax = plt.subplots(figsize=(12, 10))
    sc = ax.scatter(e, n, c=s * 1000.0, cmap="RdYlGn_r", s=64, alpha=0.8, edgecolors="black", linewidth=0.35)
    plt.colorbar(sc, ax=ax, label="Subsidence (mm)")

    px, py = _panel_polygon_xy(report)
    ax.plot(px, py, color="navy", linewidth=2.3, label="Panel boundary")

    for p in inputs["panel_points"]:
        ax.add_patch(
            patches.Circle((p["easting"], p["northing"]), bounds["influence_distance"], linewidth=1.0, edgecolor="crimson", facecolor="none", linestyle=":", alpha=0.45)
        )

    ann = ax.annotate(
        "",
        xy=(0, 0),
        xytext=(15, 15),
        textcoords="offset points",
        bbox={"boxstyle": "round", "fc": "white", "alpha": 0.9},
        arrowprops={"arrowstyle": "->", "color": "black"},
    )
    ann.set_visible(False)

    def on_click(event):
        if event.inaxes != ax or event.xdata is None or event.ydata is None:
            return
        d = np.sqrt((e - event.xdata) ** 2 + (n - event.ydata) ** 2)
        idx = int(np.argmin(d))
        diag = np.sqrt((bounds["influence_east"] - bounds["influence_west"]) ** 2 + (bounds["influence_north"] - bounds["influence_south"]) ** 2)
        if d[idx] <= max(1e-9, 0.03 * diag):
            ann.xy = (e[idx], n[idx])
            ann.set_text(f"E: {e[idx]:.2f}\nN: {n[idx]:.2f}\nS: {s[idx]:.4f} m")
            ann.set_visible(True)
            fig.canvas.draw_idle()

    fig.canvas.mpl_connect("button_press_event", on_click)

    ax.plot(inputs["center_easting"], inputs["center_northing"], "r*", markersize=15, label="Centroid")
    ax.set_title("Interactive Subsidence Map (click near a point)")
    ax.set_xlabel("Easting (m)")
    ax.set_ylabel("Northing (m)")
    ax.set_aspect("equal")
    ax.grid(True, alpha=0.25)
    ax.legend(loc="upper right")
    plt.show()
