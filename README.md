# Leaf Hunt

An offline, audio-first plant scavenger hunt. Each week it gives you five seasonal clues based on your local last spring frost date. You head outside, identify plants with a local open-weight vision model, and describe your finds by voice. Everything runs on your own machine, so it works in airplane mode.

> **Status: early development.** The project skeleton and configuration loading are in place. The clue engine, plant identification, voice notes, and journal are planned but not finished.

## Why offline and open

- **Works with no signal.** Nothing calls a remote API at runtime.
- **Your data stays with you.** Photos and voice notes never leave your device.
- **Free to run.** No per-request costs, so you can play all season.
- **Swappable models.** Vision, speech-to-text, and text-to-speech sit behind one adapter interface, so you can change models in `config.toml`.

## Features

| Command | What it does | Status |
| --- | --- | --- |
| `hunt` | Generates five weekly clues from your frost date and reads them aloud | Planned |
| `identify <image>` | Identifies a plant from a photo and says so when confidence is low | Planned |
| `note` | Records a voice note, transcribes it locally, and saves it with a timestamp | Planned |
| `journal` | Lists your finds and exports them to CSV or a styled HTML page | Planned |

## Hardware

Not yet measured. The target is a laptop or a Raspberry Pi. Record RAM, CPU, and model size here once you've tested on real hardware.

## Install

Check `requires-python` in `pyproject.toml` for the supported Python version.

```bash
git clone https://github.com/<your-username>/leaf-hunt.git
cd leaf-hunt
python -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate
pip install -e ".[dev]"
```

Then install a local model server (Ollama) and pull the vision model named in `config.toml`:

```bash
ollama pull <vision-model-name>
```

## Configuration

Settings live in `config.toml`:

| Setting | Purpose |
| --- | --- |
| Region | Chooses the seasonal plant data for your area |
| Last spring frost date | Sets the timing for weekly clues |
| Model names | Vision, speech-to-text, and text-to-speech models |
| Data directory | Where the journal and voice notes are saved |
| Theme colors | Hex colors for terminal output and the HTML export |

## Usage

```bash
leaf-hunt hunt
leaf-hunt identify path/to/photo.jpg
leaf-hunt note
leaf-hunt journal --export csv
```

Every step works with the screen off. Output is kept minimal.

## Model licenses

The code is MIT licensed (see [LICENSE](LICENSE)). Model weights have their own licenses, and some restrict certain uses. Before you publish or redistribute, check the license for each model you use and note it here.

## Development

```bash
pytest
```

Tests use a mock backend, so they run without model weights.

## Good first issues

1. **Validate config on load.** Give clear error messages for missing or malformed values in `config.py`.
2. **Add a `--version` flag** to the CLI.
3. **Write a seasonal plant dataset** for one region, starting with about 10 plants in `seasonal_plants.json`.
4. **Add a `NO_COLOR` test** to confirm plain-text output when the variable is set.
5. **Run mypy in CI.** The package already includes `py.typed`, so type checking is a natural next step.

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md). Hacktoberfest contributions are welcome.