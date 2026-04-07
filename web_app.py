#!/usr/bin/env python
"""Flask web application for interactive subsidence visualization."""

from flask import Flask, render_template, request, jsonify
from subsidence_calculator import create_report
import plotly.graph_objects as go
import json
from pathlib import Path

app = Flask(__name__)


def generate_interactive_html(report):
    """Generate Plotly interactive map."""
    points = report["points"]
    if not points:
        return None

    e = [p["easting"] for p in points]
    n = [p["northing"] for p in points]
    s = [p["subsidence"] for p in points]

    figure = go.Figure()

    figure.add_trace(
        go.Scatter(
            x=e,
            y=n,
            mode="markers",
            marker=dict(
                size=8,
                color=[val * 1000 for val in s],
                colorscale="RdYlGn_r",
                showscale=True,
                colorbar=dict(title="Subsidence (mm)"),
                line=dict(width=0.5, color="white"),
            ),
            text=[f"E: {ei:.2f}<br>N: {ni:.2f}<br>S: {si:.4f} m" for ei, ni, si in zip(e, n, s)],
            hovertemplate="%{text}<extra></extra>",
        )
    )

    # Add panel boundary
    panel_points = report["inputs"]["panel_points"]
    if panel_points:
        px = [p["easting"] for p in panel_points] + [panel_points[0]["easting"]]
        py = [p["northing"] for p in panel_points] + [panel_points[0]["northing"]]
        figure.add_trace(
            go.Scatter(
                x=px,
                y=py,
                mode="lines",
                name="Panel boundary",
                line=dict(color="navy", width=3),
                hoverinfo="skip",
            )
        )

    # Add centroid
    centroid = report["centroid"]
    figure.add_trace(
        go.Scatter(
            x=[centroid["easting"]],
            y=[centroid["northing"]],
            mode="markers",
            marker=dict(size=12, color="red", symbol="star"),
            name="Panel centroid",
            hovertemplate="Centroid<extra></extra>",
        )
    )

    # Add influence circles
    bounds = report["bounds"]
    influence_dist = bounds["influence_distance"]
    for i, p in enumerate(panel_points, 1):
        theta = list(range(0, 361, 5))
        import math
        circle_x = [p["easting"] + influence_dist * math.cos(math.radians(t)) for t in theta]
        circle_y = [p["northing"] + influence_dist * math.sin(math.radians(t)) for t in theta]
        figure.add_trace(
            go.Scatter(
                x=circle_x,
                y=circle_y,
                mode="lines",
                name=f"Influence zone {i}",
                line=dict(color="crimson", width=1, dash="dot"),
                hoverinfo="skip",
            )
        )

    figure.update_layout(
        title="Interactive Subsidence Map",
        xaxis_title="Easting (m)",
        yaxis_title="Northing (m)",
        yaxis={"scaleanchor": "x", "scaleratio": 1},
        template="plotly_white",
        hovermode="closest",
        height=600,
    )

    return figure.to_html(include_plotlyjs="cdn")


@app.route("/")
def index():
    """Render the main page."""
    return render_template("index.html")


@app.route("/api/calculate", methods=["POST"])
def calculate():
    """Calculate subsidence based on input parameters."""
    try:
        data = request.json
        
        # Parse panel points
        panel_points = []
        for i in range(int(data.get("num_points", 4))):
            panel_points.append({
                "easting": float(data[f"point_{i}_e"]),
                "northing": float(data[f"point_{i}_n"])
            })

        # Get other parameters
        thickness = float(data.get("thickness", 2.5))
        depth_of_cover = float(data.get("depth_of_cover", 300))
        extraction_ratio = float(data.get("extraction_ratio", 1.0))
        subsidence_factor = float(data.get("subsidence_factor", 0.5))
        new_ratio = float(data.get("new_ratio", 1.4))
        angle_of_draw = float(data.get("angle_of_draw", 35))
        mesh_spacing = float(data.get("mesh_spacing", 25))

        # Generate report
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

        # Generate interactive HTML
        plot_html = generate_interactive_html(report)

        return jsonify({
            "status": "success",
            "plot_html": plot_html,
            "report": {
                "s_max": report["calculations"]["s_max"],
                "influence_distance": report["calculations"]["influence_distance"],
                "num_points": len(report["points"]),
                "average_subsidence": report["calculations"]["average_subsidence"],
                "max_subsidence": report["calculations"]["max_subsidence"],
            }
        })

    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 400


if __name__ == "__main__":
    print("Starting Subsidence Visualization Server...")
    print("Open http://localhost:5000 in your browser")
    app.run(debug=True, host="0.0.0.0", port=5000)
