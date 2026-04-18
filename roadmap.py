from config import THRESHOLD
import json

with open("resources.json") as f:
    resources = json.load(f)

def analyze_and_generate(scores, target):
    gaps = []
    roadmap = []

    weakest = min(scores, key=scores.get)
    strongest = max(scores, key=scores.get)

    # Check each category — if below threshold, add to gaps
    for cat, score in scores.items():
        if score < THRESHOLD:
            gaps.append(cat)
            roadmap.extend(resources[cat])

    roadmap.append(f"Focus first on your weakest area: {weakest}")
    roadmap.append(f"Your strongest area is: {strongest} — keep it up!")

    # Target-specific advice
    if target == "product" and scores["DSA"] < 0.5:
        roadmap.append("You are not ready for Product companies yet. Improve DSA first.")
    elif target == "product" and scores["DSA"] >= 0.5:
        roadmap.append("You can start preparing for Product company interviews.")

    if target == "service" and scores["Aptitude"] < 0.5:
        roadmap.append("Improve Aptitude — it is heavily weighted for Service companies like TCS, Infosys.")

    if target == "core" and scores["CN"] < 0.5:
        roadmap.append("Improve Computer Networks — it is the most important subject for Core companies.")

    return gaps, roadmap, weakest, strongest
