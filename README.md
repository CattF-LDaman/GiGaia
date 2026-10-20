# GiGaia

A 2D multiplayer survival game with procedural worlds, custom networking, and a Pygame CE client.

## Features

- Client/server architecture with shared game logic in `GiGaia/GiCore`
- Procedural terrain generation (OpenSimplex noise layers)
- Custom binary protocol and world/user persistence
- Tile-based world with lighting, inventory, and entities

## Requirements

- Python 3.10+
- SDL2 (provided by `pygame-ce` wheels on most platforms)

## Quick start

From the repository root (so `GiGaia` imports resolve):

```bash
# Conda (recommended; env name matches legacy batch scripts)
conda env create -f environment.yml
conda activate GiGaia

# Or venv + pip
python -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements.txt
pip install -e .
```

Run the dedicated server, then the client in another terminal:

```bash
python run_server.py
python run_client.py
```

Client and server data live under OS-specific app data paths (for example `~/.local/share/GiGaia` and `~/.local/share/GiGaiaServer` on Linux); see `GiGaia/GiCore/Data/data.py`.

## Project layout

| Path | Role |
|------|------|
| `GiGaia/GiCore/` | Shared engine: networking, data formats, world generation, entities |
| `GiGaia/GiClient/` | Game client and UI |
| `GiGaia/GiServer/` | Authoritative server and admin terminal |
| `GiGaia_Assets/` | Art, audio, JSON data |
| `GiGaiaBundler/` | Windows bundler (optional; see `requirements-bundler.txt`) |
| `run_client.py`, `run_server.py` | Entry points for local development |

## Optional tools

- **World data viz:** `python wdataviz.py`
- **Proc-gen preview:** `python gentest.py`
- **Release bundle (Windows):** `pip install -r requirements-bundler.txt` then `python -m GiGaiaBundler`

## License

Source is provided for portfolio and reference; no license file is included yet. Contact the maintainer before redistribution.
