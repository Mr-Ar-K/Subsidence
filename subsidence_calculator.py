"""
Simple single-seam subsidence calculations using panel boundary points.
"""

import json
import math
from statistics import mean


def calculate_max_subsidence(thickness, extraction_ratio, subsidence_factor):
    return thickness * extraction_ratio * subsidence_factor


def calculate_influence_distance(depth_of_cover, angle_of_draw_deg):
    return depth_of_cover * math.tan(math.radians(angle_of_draw_deg))


def calculate_panel_width(depth_of_cover, new_ratio):
    return new_ratio * depth_of_cover


def polygon_centroid(points):
    # Fallback to average if area is near zero.
    area_term = 0.0
    cx = 0.0
    cy = 0.0
    count = len(points)

    for i in range(count):
        x1, y1 = points[i]
        x2, y2 = points[(i + 1) % count]
        cross = x1 * y2 - x2 * y1
        area_term += cross
        cx += (x1 + x2) * cross
        cy += (y1 + y2) * cross

    if abs(area_term) < 1e-12:
        avg_x = sum(p[0] for p in points) / count
        avg_y = sum(p[1] for p in points) / count
        return avg_x, avg_y

    factor = 1.0 / (3.0 * area_term)
    return cx * factor, cy * factor


def point_in_polygon(easting, northing, polygon):
    # Ray-casting algorithm.
    inside = False
    count = len(polygon)

    for i in range(count):
        x1, y1 = polygon[i]
        x2, y2 = polygon[(i + 1) % count]

        cond = ((y1 > northing) != (y2 > northing))
        if cond:
            x_intersect = (x2 - x1) * (northing - y1) / ((y2 - y1) + 1e-15) + x1
            if easting < x_intersect:
                inside = not inside

    return inside


def distance_point_to_segment(px, py, x1, y1, x2, y2):
    vx = x2 - x1
    vy = y2 - y1
    wx = px - x1
    wy = py - y1

    seg_len_sq = vx * vx + vy * vy
    if seg_len_sq == 0:
        return math.sqrt((px - x1) ** 2 + (py - y1) ** 2)

    t = (wx * vx + wy * vy) / seg_len_sq
    t = max(0.0, min(1.0, t))

    proj_x = x1 + t * vx
    proj_y = y1 + t * vy

    return math.sqrt((px - proj_x) ** 2 + (py - proj_y) ** 2)


def distance_to_polygon_boundary(easting, northing, polygon):
    min_distance = float("inf")
    count = len(polygon)

    for i in range(count):
        x1, y1 = polygon[i]
        x2, y2 = polygon[(i + 1) % count]
        distance = distance_point_to_segment(easting, northing, x1, y1, x2, y2)
        if distance < min_distance:
            min_distance = distance

    return min_distance


def build_bounds(panel_points, influence_distance):
    eastings = [point[0] for point in panel_points]
    northings = [point[1] for point in panel_points]

    panel_west = min(eastings)
    panel_east = max(eastings)
    panel_south = min(northings)
    panel_north = max(northings)

    return {
        "influence_west": panel_west - influence_distance,
        "influence_east": panel_east + influence_distance,
        "influence_south": panel_south - influence_distance,
        "influence_north": panel_north + influence_distance,
        "panel_west": panel_west,
        "panel_east": panel_east,
        "panel_south": panel_south,
        "panel_north": panel_north,
        "influence_distance": influence_distance,
        "panel_points": [{"easting": p[0], "northing": p[1]} for p in panel_points],
    }


def subsidence_at_point(easting, northing, panel_points, max_subsidence, influence_distance):
    if influence_distance <= 0:
        return 0.0

    inside_panel = point_in_polygon(easting, northing, panel_points)
    if inside_panel:
        return max_subsidence

    distance = distance_to_polygon_boundary(easting, northing, panel_points)
    if distance > influence_distance:
        return 0.0

    ratio = distance / influence_distance
    return max_subsidence * max(0.0, 1.0 - ratio * ratio)


def generate_grid_points(bounds, panel_points, max_subsidence, mesh_spacing):
    points = []
    easting = bounds["influence_west"]

    while easting <= bounds["influence_east"] + 1e-9:
        northing = bounds["influence_south"]
        while northing <= bounds["influence_north"] + 1e-9:
            value = subsidence_at_point(
                easting,
                northing,
                panel_points,
                max_subsidence,
                bounds["influence_distance"],
            )
            if value > 0:
                points.append(
                    {
                        "easting": round(easting, 2),
                        "northing": round(northing, 2),
                        "subsidence": round(value, 4),
                    }
                )
            northing += mesh_spacing
        easting += mesh_spacing

    return points


def create_report(panel_points, thickness, depth_of_cover, extraction_ratio, subsidence_factor, new_ratio, angle_of_draw_deg, mesh_spacing):
    max_subsidence = calculate_max_subsidence(thickness, extraction_ratio, subsidence_factor)
    influence_distance = calculate_influence_distance(depth_of_cover, angle_of_draw_deg)
    nominal_width = calculate_panel_width(depth_of_cover, new_ratio)

    bounds = build_bounds(panel_points, influence_distance)
    center_easting, center_northing = polygon_centroid(panel_points)
    points = generate_grid_points(bounds, panel_points, max_subsidence, mesh_spacing)

    return {
        "inputs": {
            "panel_points": [{"easting": p[0], "northing": p[1]} for p in panel_points],
            "center_easting": round(center_easting, 3),
            "center_northing": round(center_northing, 3),
            "thickness": thickness,
            "depth_of_cover": depth_of_cover,
            "extraction_ratio": extraction_ratio,
            "subsidence_factor": subsidence_factor,
            "new_ratio": new_ratio,
            "angle_of_draw_deg": angle_of_draw_deg,
            "mesh_spacing": mesh_spacing,
        },
        "calculated": {
            "s_max": round(max_subsidence, 4),
            "s_max_mm": round(max_subsidence * 1000.0, 2),
            "influence_distance": round(influence_distance, 2),
            "nominal_panel_width_from_ratio": round(nominal_width, 2),
        },
        "bounds": bounds,
        "points": points,
        "summary": {
            "point_count": len(points),
            "max_point_subsidence": round(max((p["subsidence"] for p in points), default=0.0), 4),
            "avg_point_subsidence": round(mean([p["subsidence"] for p in points]), 4) if points else 0.0,
        },
    }


def format_report(report):
    inputs = report["inputs"]
    calculated = report["calculated"]
    bounds = report["bounds"]
    summary = report["summary"]

    lines = []
    lines.append("=" * 72)
    lines.append("SINGLE SEAM SUBSIDENCE REPORT")
    lines.append("=" * 72)
    lines.append("Panel boundary points (E, N):")
    for index, point in enumerate(inputs["panel_points"], start=1):
        lines.append(f"  {index}. ({point['easting']}, {point['northing']})")
    lines.append(f"Panel centroid: ({inputs['center_easting']}, {inputs['center_northing']})")
    lines.append(f"Thickness h: {inputs['thickness']}")
    lines.append(f"Depth of cover H: {inputs['depth_of_cover']}")
    lines.append(f"Extraction ratio e: {inputs['extraction_ratio']}")
    lines.append(f"Subsidence factor a: {inputs['subsidence_factor']}")
    lines.append(f"NEW ratio W(new)/H: {inputs['new_ratio']}")
    lines.append(f"Angle of draw alpha: {inputs['angle_of_draw_deg']} deg")
    lines.append(f"Grid spacing: {inputs['mesh_spacing']}")
    lines.append("")
    lines.append(f"s_max = h * e * a = {calculated['s_max']} m ({calculated['s_max_mm']} mm)")
    lines.append(f"Influence distance = H * tan(alpha) = {calculated['influence_distance']} m")
    lines.append(f"Nominal panel width from ratio = {calculated['nominal_panel_width_from_ratio']} m")
    lines.append("")
    lines.append("Panel / influence limits:")
    lines.append(f"  Panel west/east: {bounds['panel_west']} / {bounds['panel_east']}")
    lines.append(f"  Panel south/north: {bounds['panel_south']} / {bounds['panel_north']}")
    lines.append(f"  Grid west/east: {bounds['influence_west']} / {bounds['influence_east']}")
    lines.append(f"  Grid south/north: {bounds['influence_south']} / {bounds['influence_north']}")
    lines.append("")
    lines.append(f"Influenced points: {summary['point_count']}")
    lines.append(f"Max point subsidence: {summary['max_point_subsidence']} m")
    lines.append(f"Average point subsidence: {summary['avg_point_subsidence']} m")
    lines.append("=" * 72)
    return "\n".join(lines)


def save_json(report, filename):
    with open(filename, "w", encoding="utf-8") as file_handle:
        json.dump(report, file_handle, indent=2)
