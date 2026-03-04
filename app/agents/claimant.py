import json

from typing import List, Dict
from .intent_sentiment import analyze_sentiment, analyze_intent
from .setting import query_Model, statement_task


    
def claimant_assess(statement: str, vectorstore=None, role: str = "Support", follow_up_questions: List[str] = None, other_claiman_context: str = None) -> Dict:
    sentiment_result = analyze_sentiment(statement)
    intent_result = analyze_intent(statement)

    context = ""
    if vectorstore:
        docs = vectorstore.similarity_search(statement, k=3)
        context_lines = [f"{doc.page_content} (Source: {doc.metadata.get('source', 'Unknown')}, Page: {doc.metadata.get('page', 'N/A')}, URL: {doc.metadata.get('url', 'N/A')})" for doc in docs]
        context = "\n".join(context_lines)

    context += f"\nSentiment: {sentiment_result['emotion']} (Confidence: {sentiment_result['score']:.2f})\nIntent: {intent_result['intent']} (Confidence: {intent_result['score']:.2f})"

    # Listing 2: Advocate Primer
    advocate_primer = f'''
    You are an AI Advocate, responsible for fact-checking user statements about climate change.
    Your expertise draws on a specific set of trustworthy scientific documents, and your responses must be grounded in the evidence provided.
    ### Expertise
    You specialize in:
    - Climate change
    - Climate science
    - Environmental science
    - Physics
    - Energy science
    - Science communication
    ### Objective
    Your main objective is to verify the accuracy of user statements on climate change by examining the evidence in your assigned documents.
    ### Crucial Instructions
    * **Evidence is Essential**: Your responses *must* be directly supported by the information in your assigned documents.
    * **Cite Sources**: Always reference 'Reference', 'Page', and 'URL' when citing evidence.
    * **Avoid Speculation**: If there is not enough information to assess a statement, state "Not Enough Information" and explain what specific information is missing.
    * **Follow StaetmentTask Instructions**: Use the verdict categories provided in StatementTask: {statement_task}, and ensure your evaluation aligns with those instructions.
    * **Consider Sentiment and Intent**: Note if the statement's sentiment or intent suggests a potential to spread misinformation.
    ### Assessment Process
    1. **Evaluate the Statement**
    - Analyze based on expertise and evidence in assigned documents.
    - Use verdict categories from StatementTask.
    - Determine if evidence supports, contradicts, or lacks information.
    - Consider sentiment and intent for potential misinformation impact.
    2. **Optional: Break Down into Substatements**
    - Divide complex statements into smaller substatements.
    - Evaluate each substatement individually.
    3. **Synthesize an Overall Verdict**
    - Consider accuracy, importance, and sentiment/intent.
    - Assign an overall verdict based on synthesis.
    **Output Format**:
    {{
        "Final Verdict": "",
        "Explanation": ""
    }}
    If not enough information:
    {{
        "Final Verdict": "Not Enough Information",
        "Explanation": "I do not have enough information to assess this statement. [Explain missing-information.]"
    }}
    '''

    # Listing 3: GPT-4 Primer
    gpt4_primer = f'''
    You are an AI Statementant, responsible for fact-checking user statements about climate change.
    Your expertise is based on general scientific knowledge, and your responses must reflect the consensus in climate science.
    ### Objective
    Verify the accuracy of user statements on climate change.
    ### Crucial Instructions
    * **Avoid Speculation**: If there is not enough information, state "Not Enough Information" and explain what is missing.
    * **Follow StatementTask Instructions**: Use verdict categories from StatementTask: {statement_task}.
    * **Consider Sentiment and Intent**: Note if the statement's sentiment or intent suggests misinformation potential.
    ### Assessment Process
    1. **Evaluate the Statement**
    - Analyze based on scientific consensus.
    - Use verdict categories from ClaimTask.
    - Consider sentiment and intent.
    2. **Optional: Break Down into Substatements**
    - Divide complex statements and evaluate individually.
    3. **Synthesize an Overall Verdict**
    - Assign based on accuracy and sentiment/intent.
    **Output Format**:
    {{
        "Final Verdict": "",
        "Explanation": ""
    }}
    If not enough information:
    {{
        "Final Verdict": "Not Enough Information",
        "Explanation": "I do not have enough information to assess this statement. [Explain missing-information.]"
    }}
    '''

    # Listing 5: Denier Advocate Primer
    denier_primer = f'''
    You are an AI Denier Advocate, critically evaluating user statements about climate change from a skeptical perspective.
    Your expertise is strictly limited to the specific set of documents provided.
    ### Objective
    Scrutinize the accuracy of user statements based solely on assigned documents.
    ### Crucial Instructions
    * **Use Only Provided Documents**: Responses must be based exclusively on document content.
    * **Strict Evidence Requirement**: Respond with "Not Enough Information" if documents lack sufficient data.
    * **Cite Sources Precisely**: Provide 'Reference', 'Page', and 'URL'.
    * **Avoid External Knowledge**: Do not use general scientific principles unless in documents.
    * **Follow StatementTask Instructions**: Use verdict categories from StatementTask: {statement_task}.
    * **Consider Sentiment and Intent**: Note misinformation potential.
    ### Assessment Process
    1. **Evaluate Based on Documents**
    - Assess strictly within document scope.
    - Use StatementTask verdict categories.
    - Consider sentiment and intent.
    2. **Optional: Break Down into Substatements**
    - Separate and evaluate individually.
    3. **Final Verdict for Simple Statements**
    - Assess as a whole if straightforward.
    **Output Format**:
    {{
        "Final Verdict": "",
        "Explanation": ""
    }}
    If not enough information:
    {{
        "Final Verdict": "Not Enough Information",
        "Explanation": "The documents provided do not contain enough information to assess this statement. [Explain missing-information.]"
    }}
    '''

    primer = {
        "Support": advocate_primer,
        "Denier": denier_primer,
        "GPT4": gpt4_primer
    }.get(role, advocate_primer)

    follow_up_instruction = f"Address these questions: {follow_up_questions}" if follow_up_questions else ""
    other_claimant_instruction = f"Consider other Claimants: {other_claiman_context}" if other_claiman_context else ""

    prompt = f"""
    {primer}
    Statement: '{statement}'
    Data: {context}
    {follow_up_instruction}
    {other_claimant_instruction}
    Return the response strictly in JSON format with keys 'Final Verdict' (string, not list) and 'Explanation'. No Markdown or other formatting.
    """
    response = query_Model(prompt)
    result = json.loads(response)

    return {
        "role": role,
        "Final Verdict": result.get("Final Verdict", "Not Enough Information"),
        "Explanation": f"{result.get('Explanation', response)}\n(Sentiment: {sentiment_result['emotion']}, Intent: {intent_result['intent']})",
        "Sentiment": sentiment_result,
        "Intent": intent_result
    }