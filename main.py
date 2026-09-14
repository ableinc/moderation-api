from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from transformers import pipeline

app = FastAPI(title="Local Toxicity Detection API")

# Load model locally on CPU during container startup
# This uses the classic unitary/toxic-bert text classifier
classifier = pipeline(
    "text-classification",
    model="unitary/toxic-bert",
    top_k=None,
    device=-1,  # Explicitly use CPU
)


class TextRequest(BaseModel):
    text: str


@app.post("/v1/moderation")
async def moderate_text(request: TextRequest):
    if not request.text.strip():
        return {"flagged": False, "scores": {}}

    try:
        results = classifier(request.text)[0]

        # Format the model outputs into a clean map
        scores = {res["label"]: float(res["score"]) for res in results}

        # Decide if text should be flagged based on a common threshold (e.g., 0.70)
        # unitary/toxic-bert outputs labels like: toxic, severe_toxic, obscene, threat, insult, identity_hate
        is_flagged = any(score > 0.70 for label, score in scores.items())

        return {"flagged": is_flagged, "scores": scores}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
