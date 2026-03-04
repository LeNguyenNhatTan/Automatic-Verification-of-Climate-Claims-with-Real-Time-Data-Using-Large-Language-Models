import json
from typing import List, Dict
from .setting import query_Model, verdictsClimateFeedback

def verifier_evaluate(statement: str, claimant_responses: List[Dict], round_number: int = 1, max_rounds: int = 5) -> Dict:
    context = [{"Claimant": r["role"], "Verdict": r["Final Verdict"], "Explanation": r["Explanation"], "Sentiment": r["Sentiment"], "Intent": r["Intent"]} for r in claimant_responses]
    context_str = json.dumps(context, indent=2)

    # Listing 4: Verifier Primer
    verifier_primer = f'''
    Role: Authoritative "Verifier" System
    Primary Objective: Synthesize assessments from Claimants to determine the veracity of a user's statement on climate change, prioritizing scientific rigor.
    ### Expertise
    You specialize in:
    - Climate change
    - Climate science
    - Environmental science
    - Physics
    - Energy science
    - Science communication
    ### Responsibilities
    1. Review verdicts and explanations from Claimants.
    2. Consolidate into a final verdict, prioritizing evidence-based assessments.
    3. Seek clarification through follow-up questions if discrepancies arise.
    4. Prioritize Claimants with specific, high-quality evidence.
    5. Consider sentiment and intent for misinformation potential.
    ### Final Assessment Criteria
    1. Analyze collective Claimant assessments.
    2. Do not rely on majority voting; prioritize evidence quality.
    3. Assess sentiment and intent impact on misinformation.
    ### Guidelines
    1. Prioritize Claimants with concrete evidence over those with "Not Enough Information."
    2. Ask follow-up questions if Claimants provide conflicting evidence or if additional evidence is needed to strengthen the verdict.
    3. Stop debate if no Claimant changes assessment after follow-up or if evidence is sufficient.
    4. Cite 'Reference', 'Page', and 'URL' when referring to Claimant data.
    5. Assess risk level (High, Medium, Low) based on sentiment/intent.
    **Output Format**:
    {{
        "Final Verdict": "",
        "Explanation": "",
        "Confidence": "high|medium|low",
        "RiskLevel": "high|medium|low",
        "Debate": {{
            "Status": "Open|Closed",
            "Round": {round_number},
            "Follow-Up Questions": {{}}
        }}
    }}
    '''

    verdicts = [r["Final Verdict"] for r in claimant_responses]
    valid_verdicts = [v for v in verdicts if v != "Not Enough Information"]
    unique_verdicts = set(valid_verdicts)

    risk_level = "low"
    sentiment_warnings = []
    for r in claimant_responses:
        sentiment = r.get("Sentiment", {"emotion": "unknown", "score": 0.0})
        intent = r.get("Intent", {"intent": "unknown", "score": 0.0})
        if sentiment["emotion"] in ["anger", "fear"] or intent["intent"] in ["misleading", "controversial"]:
            risk_level = "high"
            sentiment_warnings.append(f"Warning: {r['role']} detected {sentiment['emotion']} sentiment or {intent['intent']} intent, increasing risk of misinformation spread.")
        elif sentiment["score"] > 0.5 or intent["score"] > 0.5:
            risk_level = max(risk_level, "medium")

    confidence = "high" if len(unique_verdicts) == 1 and len(valid_verdicts) >= 2 else "medium" if valid_verdicts else "low"
    debate_status = "Open" if len(unique_verdicts) > 1 or (len(valid_verdicts) == 1 and len(valid_verdicts) < len(verdicts) and confidence != "high") else "Closed"

    follow_up_questions = {}
    if debate_status == "Open" and round_number < max_rounds: 
        for r in claimant_responses:
            if r["Final Verdict"] == "Not Enough Information":
                follow_up_questions[r["role"]] = [
                    f"Can you provide specific evidence or data from your resources that directly addresses the statement '{statement}'?",
                    f"What additional information or analysis is needed to evaluate the accuracy of the statement, and why is it missing from your current resources?"
                ]
            elif r["role"] == "Denier":
                follow_up_questions[r["role"]] = [
                    f"Can you clarify the methodologies or data sources in your cited studies that support your assessment of the statement '{statement}'?",
                    f"How do your findings compare to the broader scientific consensus or mainstream climate science regarding this statement?"
                ]
            else:  # Support
                follow_up_questions[r["role"]] = [
                    f"Can you provide detailed evidence or studies from your resources to support or refute the statement '{statement}'?",
                    f"How does your assessment align with the broader scientific consensus or documented evidence on this topic?"
                ]

    prompt = f"""
    {verifier_primer}
    Statement: '{statement}'
    Claimants: {context_str}
    Debate Status: {debate_status}
    Confidence: {confidence}
    Follow-Up Questions: {json.dumps(follow_up_questions, indent=2)}
    """

    response = query_Model(prompt)
    result = json.loads(response)

    final_verdict = result.get("Final Verdict", "Not Enough Information")
    if final_verdict not in verdictsClimateFeedback:
        final_verdict = "Not Enough Information"

    result["Final Verdict"] = final_verdict
    result["Confidence"] = confidence
    result["RiskLevel"] = risk_level
    result["Explanation"] += "\n" + "\n".join(sentiment_warnings) if sentiment_warnings else ""
    result["Debate"] = {
        "Status": debate_status,
        "Round": round_number,
        "Follow-Up Questions": follow_up_questions
    }

    return result