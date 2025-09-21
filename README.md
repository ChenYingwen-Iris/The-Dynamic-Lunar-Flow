# Lunar Phase Polar Animation (2024)

Generate a polar animation (MP4) of daily lunar illumination for New York, USA in 2024 using Python and a CSV dataset.

## Overview
- Parse lunar data from CSV (use rows where `Line == 1`), align to the full year, and interpolate missing values.
- Visualize illumination on a circular (polar) track with monthly labels and a star field.
- Render daily frames and encode a smooth MP4 with imageio/ffmpeg.

## Demo
- Watch the video: [moon_phase_animation_2024.mp4](./moon_phase_animation_2024.mp4)

<video src="moon_phase_animation_2024.mp4" width="480" controls muted>
Your browser does not support embedded video. Please download the MP4 above.
</video>

## Requirements
- Python 3.7+
- Dependencies:
  - pandas
  - numpy
  - matplotlib
  - imageio

Install:
```bash
pip install pandas numpy matplotlib imageio
```

Note: MP4 encoding requires ffmpeg available on your system PATH (or managed by imageio).

## Data
- File: `astro-202401-202412.csv`
- Relevant columns: `Date`, `Line`, `Illuminated` (percentage string, e.g., `75.0%`).
- Place the CSV in the same directory as `moon.py`.

## Usage
1. Ensure `astro-202401-202412.csv` and `moon.py` are in the same folder.
2. Run:
   ```bash
   python moon.py
   ```
3. Output: `moon_phase_animation_2024.mp4` (temporary frame images are auto-cleaned).

## Customize
- Year and CSV path: edit the `__main__` section in `moon.py`.
- Frame rate: `create_moon_phase_animation(..., frame_rate=15)`.
- Colors: adjust `create_moon_colormap()`.

## Troubleshooting (ffmpeg)
- macOS: `brew install ffmpeg`
- Ubuntu/Debian: `sudo apt-get install ffmpeg`
- Windows: install from https://ffmpeg.org and add to PATH.

## Project layout
```
.
├── moon.py
├── astro-202401-202412.csv
└── moon_phase_animation_2024.mp4
```

## References
- Matplotlib: https://matplotlib.org/
- imageio: https://imageio.readthedocs.io/

---

For other years or datasets, adjust the parameters in `moon.py` accordingly.
