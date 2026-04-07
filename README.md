# Subsidence Calculator

An interactive single-seam subsidence calculator with polygon-based panel boundaries and real-time 3D visualization.

## Features

- **Polygon Panel Geometry**: Define mining panels using arbitrary polygon boundaries
- **Real-time Visualization**: Interactive maps with Plotly.js
- **Multiple Interfaces**: Choose between Jupyter, Flask web server, or terminal UI
- **Subsidence Physics**: Calculates maximum subsidence and influence zones based on mining depth and extraction ratios
- **Data Export**: Save results as HTML maps or CSV data files

## Installation

```bash
cd /workspaces/Subsidence

# Install Python dependencies
pip install -r requirements.txt
# OR manually: pip install plotly flask numpy pandas ipywidgets jupyter
```

## Three Ways to Use

### 1. Interactive Jupyter Notebook (Recommended for data analysis)

```bash
jupyter notebook subsidence_interactive.ipynb
```

**Features:**
- Real-time parameter sliders
- Instant Plotly visualization updates
- Calculate button triggers fresh computation
- Inline results and analysis

### 2. Flask Web Server (Recommended for sharing results)

```bash
python web_app.py
```

Then open your browser to: **http://localhost:5000**

**Features:**
- Professional web interface with gradient styling
- Responsive design (desktop/tablet/mobile)
- Dynamic panel point editing
- Live subsidence calculation on form submit
- Hover tooltips for interactive exploration

### 3. Terminal UI (Simple/headless)

```bash
python main.py
```

**Features:**
- Console-based parameter input
- Generates HTML interactive map
- Automatically opens browser

## Usage Example

### Define a Panel

Input the Easting and Northing coordinates of panel boundary vertices:
- Point 1: E=0.0, N=0.0
- Point 2: E=100.0, N=0.0
- Point 3: E=100.0, N=100.0
- Point 4: E=0.0, N=100.0

### Set Parameters

| Parameter | Default | Description |
|-----------|---------|-------------|
| Panel thickness (h) | 2.5 m | Seam thickness |
| Depth of cover (H) | 300 m | Distance from surface to seam |
| Extraction ratio (e) | 1.0 | 1.0=Longwall, 0.7=Board & Pillar |
| Subsidence factor (a) | 0.5 | Material property |
| Angle of draw (α) | 35° | Influence cone angle |
| Mesh grid spacing | 25 m | Resolution of calculation grid |

### Calculate Subsidence

The calculator generates:
- **s_max**: Maximum subsidence directly above panel (h × e × a)
- **Influence distance**: How far subsidence extends (H × tan(α))
- **Grid points**: All locations with non-zero subsidence
- **Interactive map**: Hover-enabled visualization

## File Structure

```
.
├── subsidence_calculator.py      # Core calculation engine
├── subsidence_visualization.py   # Plotly visualization functions
├── main.py                       # Terminal interface
├── web_app.py                    # Flask web server
├── templates/
│   └── index.html               # Web interface template
├── subsidence_interactive.ipynb # Jupyter notebook
└── README.md                     # This file
```

## Physics Model

### Maximum Subsidence

$$s_{max} = h \times e \times a$$

Where:
- h = seam thickness
- e = extraction ratio
- a = subsidence factor

### Influence Distance

$$d = H \times \tan(\alpha)$$

Where:
- H = depth of cover
- α = angle of draw (typically 30-45°)

### Spatial Distribution

Subsidence decreases quadratically from panel boundary until it reaches zero at the influence distance.

## Requirements

- Python 3.7+
- Dependencies: plotly, flask, numpy, pandas, ipywidgets, jupyter

## License

MIT