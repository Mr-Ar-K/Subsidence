"""
Terminal-driven runner for single seam subsidence calculations.
"""

from subsidence_calculator import create_report, format_report
from subsidence_visualization import plot_interactive_map


def prompt_float(label, default=None, minimum=None):
    while True:
        suffix = f" [{default}]" if default is not None else ""
        raw_value = input(f"{label}{suffix}: ").strip()
        if not raw_value:
            if default is not None:
                value = float(default)
                break
            print("A value is required.")
            continue
        try:
            value = float(raw_value)
        except ValueError:
            print("Enter a numeric value.")
            continue
        break

    if minimum is not None and value < minimum:
        print(f"Value must be at least {minimum}.")
        return prompt_float(label, default=default, minimum=minimum)

    return value


def prompt_extraction_ratio():
    print("Extraction ratio:")
    print("  1 = Longwall")
    print("  0.7 = Board and Pillar")
    while True:
        raw_value = input("Choose 1 or 0.7 [1]: ").strip()
        if not raw_value:
            return 1.0
        if raw_value in {"1", "1.0"}:
            return 1.0
        if raw_value in {"0.7", ".7"}:
            return 0.7
        try:
            value = float(raw_value)
        except ValueError:
            print("Enter 1, 0.7, or a numeric value.")
            continue
        if value <= 0:
            print("Extraction ratio must be positive.")
            continue
        return value


def prompt_panel_points():
    print("Panel boundary points:")
    print("  Enter multiple vertices in order (clockwise or counter-clockwise).")
    print("  Minimum 3 points are required.")

    while True:
        count = int(prompt_float("Number of panel boundary points", default=4, minimum=3))
        points = []

        for index in range(1, count + 1):
            print(f"Point {index}:")
            easting = prompt_float("  Easting")
            northing = prompt_float("  Northing")
            points.append((easting, northing))

        unique_points = len(set(points))
        if unique_points < 3:
            print("At least 3 unique points are required. Please re-enter all points.")
            continue

        return points


def print_points(points, limit=20):
    print("\nInfluenced points (easting, northing, subsidence in m):")
    print("-" * 72)
    if not points:
        print("No points were generated.")
        return

    for index, point in enumerate(points[:limit], start=1):
        print(
            f"{index:>3}. ({point['easting']:.2f}, {point['northing']:.2f}) -> {point['subsidence']:.4f}"
        )

    remaining = len(points) - limit
    if remaining > 0:
        print(f"... {remaining} more points")


def main():
    print("\n" + "=" * 72)
    print("SINGLE SEAM SUBSIDENCE CALCULATOR")
    print("=" * 72)
    print("Enter the values in the terminal. Press Enter to use the default.")
    print()

    panel_points = prompt_panel_points()
    thickness = prompt_float("Panel thickness h (m)", default=2.5, minimum=0)
    depth_of_cover = prompt_float("Depth of cover H (m)", default=300.0, minimum=0)
    extraction_ratio = prompt_extraction_ratio()
    subsidence_factor = prompt_float("Subsidence factor a", default=0.5, minimum=0)
    new_ratio = prompt_float("NEW ratio W(new)/H", default=1.4, minimum=0)
    angle_of_draw = prompt_float("Angle of draw alpha (deg)", default=35.0, minimum=0)
    mesh_spacing = prompt_float("Mesh grid spacing (m)", default=25.0, minimum=0)

    report = create_report(
        panel_points,
        thickness,
        depth_of_cover,
        extraction_ratio,
        subsidence_factor,
        new_ratio,
        angle_of_draw,
        mesh_spacing,
    )

    print()
    print(format_report(report))
    print_points(report["points"], limit=25)

    print("\nOpening interactive visualization...")
    plot_interactive_map(report)

    return report


if __name__ == "__main__":
    main()
