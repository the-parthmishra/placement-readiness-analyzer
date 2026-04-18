from config import WEIGHTS

def calculate_scores(answers, questions, target):
    # Initialize score counters for each category
    category_scores = {
        "DSA": 0, "OS": 0, "DBMS": 0,
        "CN": 0, "Aptitude": 0, "Communication": 0
    }
    category_total = category_scores.copy()

    # Loop through each question and check answer
    for i, q in enumerate(questions):
        cat = q["category"]
        category_total[cat] += 1

        if answers.get(f"q{i}") == q["answer"]:
            category_scores[cat] += 1

    # Normalize: convert raw count to percentage (0.0 to 1.0)
    normalized = {}
    for cat in category_scores:
        if category_total[cat] == 0:
            normalized[cat] = 0
        else:
            normalized[cat] = category_scores[cat] / category_total[cat]

    # Apply company-specific weights to get final weighted score
    weighted_score = sum(normalized[c] * WEIGHTS[target][c] for c in normalized)

    return normalized, weighted_score
