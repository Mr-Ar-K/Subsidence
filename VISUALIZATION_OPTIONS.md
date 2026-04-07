# Visualization Options Summary

You now have **THREE** ways to visualize and interact with your subsidence calculator:

---

## 🎯 Option 1: Jupyter Notebook (Best for Iteration)

**File:** `subsidence_interactive.ipynb`

**Start it:**
```bash
jupyter notebook subsidence_interactive.ipynb
```

**Features:**
✓ Interactive widgets for real-time parameter adjustment
✓ Live Plotly visualization updates inline
✓ Instant calculation when you click "Calculate & Plot"
✓ All functionality in one place
✓ Perfect for data analysis and exploration

**Access:** Opens in your browser automatically, typically at `http://localhost:8888`

---

## 🌐 Option 2: Flask Web Server (Best for Sharing)

**File:** `web_app.py`

**Start it:**
```bash
python web_app.py
```

**Access:** Open http://localhost:5000 in your browser

**Features:**
✓ Professional web interface with gradient styling
✓ Responsive design (works on desktop, tablet, mobile)
✓ Left panel for controls, right for visualization
✓ Real-time preview as you adjust parameters
✓ Beautiful UI with sliders and modern forms
✓ Perfect for demonstrations and sharing results

**Interface Layout:**
- Left sidebar: Parameter sliders and point inputs
- Right panel: Interactive Plotly map with results
- Results summary showing key metrics

---

## 📊 Option 3: Terminal Interface (Simple)

**File:** `main.py`

**Start it:**
```bash
python main.py
```

**Features:**
✓ Console-based parameter input
✓ Auto-generates HTML interactive map
✓ Opens map in browser automatically
✓ Good for headless environments
✓ Minimal dependencies

**Process:**
1. Enter panel boundary points (E, N coordinates)
2. Enter subsidence parameters
3. Calculator generates grid and visualization
4. HTML file opens automatically in browser

---

## 📋 Quick Comparison

| Feature | Notebook | Flask | Terminal |
|---------|----------|-------|----------|
| Real-time adjustment | ✓ | ✓ | ✗ |
| Professional UI | △ | ✓✓ | ✗ |
| Easy to share | ✗ | ✓✓ | △ |
| Data analysis | ✓✓ | ✗ | ✗ |
| Export options | ✓ | ✓ | ✓ |
| Learning curve | Low | Low | None |
| Best for... | Iteration | Demos | Quick runs |

---

## 🚀 Recommended Usage

**For Development/Analysis:**
→ Use **Jupyter Notebook** - fastest iteration, inline results

**For Client Demos:**
→ Use **Flask Web Server** - polished UI, impressive visuals

**For Quick Calculations:**
→ Use **Terminal UI** - straightforward input/output

**For Headless Systems:**
→ Use **Terminal UI** or **Notebook in non-interactive mode**

---

## 📁 New Files Created

```
/workspaces/Subsidence/
├── web_app.py                        # Flask application
├── templates/
│   └── index.html                   # Web interface HTML
├── subsidence_interactive.ipynb      # Jupyter notebook
├── requirements.txt                  # Python dependencies
├── QUICKSTART.sh                     # Quick start guide
└── VISUALIZATION_OPTIONS.md          # This file
```

---

## 🔧 Installation

All required packages are already installed in your .venv:
```bash
pip install -r requirements.txt
```

---

## 📝 Tips

1. **Persistent Server**: Flask runs indefinitely. Stop with Ctrl+C
2. **Notebook Cells**: Run them in order. Click "Calculate & Plot" to update
3. **Export Results**: Use functions in notebook to save HTML or CSV
4. **Responsive**: Flask interface works on mobile - share the URL with others
5. **Performance**: Adjust mesh spacing to balance detail vs speed

---

## 🆘 Troubleshooting

**Flask server won't start:**
- Check port 5000 isn't already in use: `lsof -i :5000`
- Try different port in web_app.py: `app.run(port=5001)`

**Jupyter notebook won't load calculator:**
- Ensure you're in `/workspaces/Subsidence` directory
- Check subsidence_calculator.py exists and has no errors

**Terminal UI doesn't open browser:**
- HTML file is still created at `subsidence_interactive.html`
- Open it manually with: `$BROWSER subsidence_interactive.html`

---

**Enjoy your interactive subsidence visualizer! 🎉**
