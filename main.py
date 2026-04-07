"""
Terminal-driven runner for single seam subsidence calculations.
"""

from subsidence_calculator import create_report, format_report, save_json
from visualizer import plot_advanced_view, plot_simple_map


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

    center_easting = prompt_float("Panel center easting", default=1000.0)
    center_northing = prompt_float("Panel center northing", default=2000.0)
    thickness = prompt_float("Panel thickness h (m)", default=2.5, minimum=0)
    depth_of_cover = prompt_float("Depth of cover H (m)", default=300.0, minimum=0)
    extraction_ratio = prompt_extraction_ratio()
    subsidence_factor = prompt_float("Subsidence factor a", default=0.5, minimum=0)
    new_ratio = prompt_float("NEW ratio W(new)/H", default=1.4, minimum=0)
    angle_of_draw = prompt_float("Angle of draw alpha (deg)", default=35.0, minimum=0)
    mesh_spacing = prompt_float("Mesh grid spacing (m)", default=25.0, minimum=0)

    report = create_report(
        center_easting,
        center_northing,
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

    save_json(report, "subsidence_report.json")
    print("\nJSON report written to subsidence_report.json")

    print("\nOpening visualizations...")
    plot_simple_map(report)
    plot_advanced_view(report)

    return report


if __name__ == "__main__":
    main()
