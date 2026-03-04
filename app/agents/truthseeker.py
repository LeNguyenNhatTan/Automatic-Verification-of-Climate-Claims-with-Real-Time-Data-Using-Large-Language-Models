from typing import Dict
from rag.vectorstore import load_vectorstore
from .claimant import claimant_assess
from .verifier import verifier_evaluate
from .neutral_verifier import neutral_verifier_evaluate

def truthseekers(statement: str, max_rounds: int = 5) -> Dict:

    support_vectorstore = load_vectorstore(persist_dir="archive/chroma_store_nasa", source="nasa.gov", query="climate change nasa")
    oppose_vectorstore = load_vectorstore(persist_dir="archive/chroma_store_ncei", source="noaa.gov", query="climate change noaa")

    claimants = [
        {"role": "Support", "vectorstore": support_vectorstore},
        {"role": "Denier", "vectorstore": oppose_vectorstore},
        {"role": "GPT4", "vectorstore": None}
    ]

    claimant_responses = []
    round_number = 1

    for claimant in claimants:
        response = claimant_assess(statement, claimant["vectorstore"], claimant["role"])
        print(f"Claimant {claimant['role']} response: {response}")
        claimant_responses.append(response)

    verifier_result = verifier_evaluate(statement, claimant_responses, round_number)
    neutral_verifier_result = neutral_verifier_evaluate(statement, claimant_responses, verifier_result, round_number)
    while neutral_verifier_result["Debate"]["Status"] == "Open" and round_number < max_rounds:
        round_number += 1
        follow_up = neutral_verifier_result["Debate"]["Follow-Up Questions"]
        new_responses = []

        for claimant in claimants:
            role = claimant["role"]
            questions = follow_up.get(role, [])
            if not questions:
                for r in claimant_responses:
                    if r["role"] == role:
                        new_responses.append(r)
                        break
                continue

            others = [f"{r['role']} Claimant: Verdict: {r['Final Verdict']}, Explanation: {r['Explanation']}" for r in claimant_responses if r["role"] != role]
            other_context = "\n".join(others)

            response = claimant_assess(
                statement,
                claimant["vectorstore"],
                role,
                follow_up_questions=questions,
                other_claiman_context=other_context
            )
            new_responses.append(response)

        claimant_responses = new_responses
        verifier_result = verifier_evaluate(statement, claimant_responses, round_number)
        neutral_verifier_result = neutral_verifier_evaluate(statement, claimant_responses, verifier_result, round_number)

        new_verdicts = [r["Final Verdict"] for r in claimant_responses]
        if all(v == "Not Enough Information" for v in new_verdicts) and neutral_verifier_result["Final Verdict"] == "Not Enough Information":
            neutral_verifier_result["Debate"]["Status"] = "Closed"
            neutral_verifier_result["Explanation"] += "\nDebate closed due to no new information provided in round {}.".format(round_number)
            break

    return {
        "statement": statement,
        "final_verdict": neutral_verifier_result.get("Final Verdict", "Not Enough Information"),
        "explanation": neutral_verifier_result.get("Explanation", "No reasoning provided"),
        "confidence": neutral_verifier_result.get("Confidence", "low"),
        "risk_level": neutral_verifier_result.get("RiskLevel", "low"),
        "debate_rounds": round_number,
        "claimant_responses": claimant_responses,
        "verifier_result": verifier_result
    }