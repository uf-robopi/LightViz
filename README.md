# LightViz: Autonomous Light-field Surveying and Mapping for Distributed Light Pollution Monitoring

![Paper](https://doi.org/10.1007/s10661-025-13862-5)
![Pre-print](https://arxiv.org/pdf/2408.00808)
![Project Page](https://robopi.ece.ufl.edu/lightviz.html)

This work is licensed under a
[Creative Commons Attribution-NonCommercial 4.0 International License][cc-by-nc].

[![CC BY-NC 4.0][cc-by-nc-image]][cc-by-nc]

[cc-by-nc]: https://creativecommons.org/licenses/by-nc/4.0/
[cc-by-nc-image]: https://licensebuttons.net/l/by-nc/4.0/88x31.png
[cc-by-nc-shield]: https://img.shields.io/badge/License-CC%20BY--NC%204.0-lightgrey.svg


## 📌 Overview

This repository contains the official implementation of the paper **[LightViz: Autonomous Light-field Surveying and Mapping for Distributed Light Pollution Monitoring](https://doi.org/10.1007/s10661-025-13862-5)**.

LightViz is an interactive tool designed for automating light pollution data collection, visualization, and mapping. It enables researchers and policymakers to generate high-resolution light-field maps, simulate lighting scenarios, and analyze the impact of light pollution in various regions.

LightViz integrates [TkinterMapView](https://github.com/TomSchimansky/TkinterMapView) for its interactive map-based user interface and [Leaflet.idw](https://github.com/spatialsparks/Leaflet.idw) for light-field interpolation using inverse distance weighting (IDW). These tools allow for real-time visualization and analysis of light pollution distribution.

**Key Features:**
- 🌍 **Geospatial Visualization** – Generates interactive light pollution maps.
- 🔬 **Simulation & Analysis** – Models light attenuation and environmental impact.
- 🏛 **Policy Support** – Assists in conservation strategies for light pollution control.

## 🎥 Demo
| Add a light source | Render light-field map |
|-------|-------|
| ![](demo/edit.gif) | ![](demo/render.gif) |
## ⚠️ Caution

Please keep the following in mind when using LightViz:

1. **Lighting Coverage Limitations**    
Since the area illuminated by each street lamp is only **on a meter scale**, an insufficient number of lamps in a region may result in **no visible light field rendering**. This is because the **LightViz map is built on a county scale (~20 km or more) and uses a grid to sample the light field, meaning some areas may be ignored**. If there aren't enough light sources, the generated map may appear invisible. You can increse the grid resolution by changing `grid_resolution` in main.py (see *line 381*).
3. **Rendering Time Considerations**    
The rendering process **can take hours** depending on the computational power of the equipment. If the process is slow, users can **adjust the cell size** in the configuration settings (see *line 83* in [example_directdraw.html](src/example_directdraw.html)) to accelerate the rendering process at the cost of spatial resolution.
4. **Why are some areas that should be black not actually black?**    
For visual presentation purposes, most black areas have been colored. You can modify *line 506* in main.py by changing `filtered_data = data_list` to obtain a realistic light-field map.

## 📄 Paper

📜 **Citation:**
If you use this repository, please cite the following paper:
```bibtex
@article{huang2024lightviz,
  title={{LightViz: Autonomous Light-field Surveying and Mapping for Distributed Light Pollution Monitoring}},
  author={Huang, Sheng-En and Suhi, Kazi Farha Farzana and Islam, Md Jahidul},
  journal={Environmental Monitoring and Assessment (EMA)},
  volume={197},
  number={384.4},
  pages = {1573-2959},
  doi = {https://doi.org/10.1007/s10661-025-13862-5},
  year={2025},
  publisher={Springer Nature}
}
```

📑 [Read the full paper (PDF)](https://arxiv.org/pdf/2408.00808.pdf)

## 📖 How to Use LightViz
LightViz provides two types of light sources: point sources with or without attenuation. **They cannot be used simultaneously**. With attenuation, you can perform single point interpolation and render a light field map. Without attenuation, you can only perform single point interpolation. We provide IDW, OK, Shepard, SVR, and NNR methods for interpolation.
### Single Point Interpolation
#### Without Attenuation
1. Zoom in to the desired level.
2. Right-click and select "Add Light Source".
3. Enter SQM values (ensure at least 3 points for interpolation, including upper and lower intensity sampling points).
4. Left-click the target point for interpolation.
#### With Attenuation
1. Follow the same steps as above but select "Add Light Source with Attenuation".
2. Fine-tune the C1 and C2 parameters.
3. Confirm and close.
4. You can now perform interpolation on the target point.
### Light Field Map Rendering (with attenuation 📉 on light source)
1. Set up the light sources with attenuation in the county area.
2. Choose the county.
3. Click **Render**.
4. The light field map will be generated. (*Caution: This process is time-consuming depending on the number of light sources and equipment.*)

### Datasets
- [st_johns_street_map_6k.csv](maps_files/st_johns_street_map_6k.csv) is the 6k streetlights csv for St. Johns County with their profiles.
- [Alachua_street_map.csv](maps_files/Alachua_street_map.csv) is the streetlights csv for Alachua County with their profiles.
- Modify **line 114** in main.py to load dataset.


### Troubleshooting
1. **`geocoder.osm` Error Code 403 (`HTTP Error 403: Forbidden`)**  
   - If you encounter this error while using LightViz, please refer to the official issue for a solution:  
     🔗 [geocoder.osm Issue #471](https://github.com/DenisCarriere/geocoder/issues/471).
2. **Unexpected Exceptions or Crashes**  
   - LightViz is still in its prototype stage, and occasional errors may occur.  
   - If you encounter an exception, we sincerely apologize.  
   - **Solution:** Simply restart the program. We are actively working to improve stability and will fix these issues in future updates.

## 🛠 Installation

### Prerequisites

Ensure you have the following installed:
- Python 3.10
- Install dependencies for graphics, GUI development, and library bindings
   ```bash
   sudo apt install libcairo2-dev libxt-dev libgirepository1.0-dev

### Setup & Quick Start

1. Clone the repository:
   ```bash
   git clone https://github.com/uf-robopi/LightViz_Internal.git
   cd LightViz_Internal/Release/
2. Setup the environment:
   ```bash
   conda env create -f environment.yml
   conda activate lightviz
3. Run LightViz:
   ```bash
   python main.py
