"""
Ad-hoc test script for the moderation API.

Sends a handful of scenarios to an already-running instance of the API
(see README for how to start it) and prints the request/response pairs
to stdout for manual inspection.
"""

import json
import urllib.error
import urllib.request

BASE_URL = "http://127.0.0.1:9090"

SCENARIOS = [
    ("Clean text", "The weather is lovely today, let's go for a walk."),
    ("Toxic / insult", "You are such a worthless idiot, nobody likes you."),
    ("Threat", "I will hurt you if you show up here again."),
    ("Obscene language", "This is absolute bullshit and I'm done with it."),
    ("Identity hate", "People like you don't belong in this country."),
    ("Empty string", ""),
    ("Whitespace only", "   \n\t  "),
    ("Long benign text", "Thank you so much for your help today, " * 10),
]


def call_moderation_api(text: str) -> dict:
    payload = json.dumps({"text": text}).encode("utf-8")
    request = urllib.request.Request(
        f"{BASE_URL}/v1/moderation",
        data=payload,
        headers={"Content-Type": "application/json"},
        method="POST",
    )
    with urllib.request.urlopen(request, timeout=30) as response:
        return json.loads(response.read().decode("utf-8"))


def format_scores(scores: dict) -> str:
    if not scores:
        return "  (none)"
    return "\n".join(f"  {label:<15} {score:.4f}" for label, score in scores.items())


def main() -> None:
    print(f"Testing moderation API at {BASE_URL}\n")

    for name, text in SCENARIOS:
        print("=" * 60)
        print(f"Scenario: {name}")
        print(f"Input:    {text!r}")

        try:
            result = call_moderation_api(text)
        except urllib.error.URLError as exc:
            print(f"Result:   ERROR - could not reach API ({exc})")
            print()
            continue
        except urllib.error.HTTPError as exc:
            print(f"Result:   HTTP {exc.code} - {exc.read().decode('utf-8')}")
            print()
            continue

        print(f"Flagged:  {result.get('flagged')}")
        print("Scores:")
        print(format_scores(result.get("scores", {})))
        print()

    print("=" * 60)
    print("Done.")


if __name__ == "__main__":
    main()
