# Moderation API

A lightweight content moderation API that flags toxic text using the
[`unitary/toxic-bert`](https://huggingface.co/unitary/toxic-bert) model. Runs
on CPU, packaged as a Docker container for an ARM64 (aarch64) EC2 instance.

## API

### `POST /v1/moderation`

Request body:

```json
{ "text": "some text to check" }
```

Response body:

```json
{
  "flagged": true,
  "scores": {
    "toxic": 0.97,
    "severe_toxic": 0.12,
    "obscene": 0.85,
    "threat": 0.02,
    "insult": 0.76,
    "identity_hate": 0.05
  }
}
```

`flagged` is `true` if any label's score exceeds `0.70`.

## Running

```bash
docker compose up --build -d
```

This builds the image for `linux/arm64` and starts the API on port `9090`,
bound to `127.0.0.1` only — it is reachable from other processes on the same
machine (e.g. `curl http://127.0.0.1:9090/v1/moderation`) but not from the
public internet or other hosts on the network.

To stop it:

```bash
docker compose down
```

## Local development (without Docker)

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn main:app --host 127.0.0.1 --port 9090
```
