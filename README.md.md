# 🌊 India Hydro-Vector Data Gateway (Render)

Ultra-lightweight secure resolution proxy for streaming `FlatGeobuf` vector data (`Watershed.fgb` and `Streams.fgb`).

## 🔐 Environment Setup on Render
Set these exact environment keys in your Render service deployment settings:
* `HF_TOKEN`: Read-access token to your private Hugging Face dataset (`JS2512/hydrology-data-vault`).
* `CLIENT_API_KEY`: Custom string used to authorize your client connections.

## 📡 Endpoints
* `GET /health` : Healthcheck
* `GET /api/v1/resolve/watershed` : Pre-signed URL for the Watershed vector dataset.
* `GET /api/v1/resolve/streams` : Pre-signed URL for the Streams vector dataset.