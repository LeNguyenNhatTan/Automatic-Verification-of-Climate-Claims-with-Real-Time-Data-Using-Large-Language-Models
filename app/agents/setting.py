from core.config import client

def clean_response(response: str) -> str:
    response = response.strip()
    if response.startswith("```") or response.startswith("'''"):
        response = response.strip("`").strip("'").strip()
        if response.lower().startswith("json"):
            response = response[4:].strip()
    return response.strip()


def query_Model(prompt: str, max_retries: int = 3) -> dict:

    full_prompt = prompt.strip() + "\nReturn the response strictly in JSON format with keys 'Final Verdict' and 'Explanation'. No Markdown, no formatting, no extra text."

    for attempt in range(max_retries):
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "user", "content": full_prompt}
            ],
            temperature=0.2,
            top_p=0.9,
            max_tokens=1024,
        )

        raw_text = response.choices[0].message.content.strip()
        return clean_response(raw_text)
    

    
verdictsClimateFeedback = ["Credible", "Not Credible"]        

statement_task = f'''
 You are a fact-checking AI assistant specializing in scientific information.
# Your task is to analyze statements and categorize their accuracy using the following categories: {verdictsClimateFeedback}. Each level describes common characteristics and examples to guide your analysis:
---
## Credible
Assign this label if the statement:
- Is supported by strong scientific evidence or aligns with the established scientific consensus.
- May lack some nuance or context, but remains fundamentally accurate and not misleading.
**Examples**:
- *"Babies under six months should not drink water as it can result in health risks."*  
  → **Credible**. Backed by medical guidelines on infant hydration.
- *"Prioritizing plant-based foods reduces greenhouse gas emissions."*  
  → **Credible**. Generally supported by environmental research, though effects depend on scale of adoption.
- *"Climate change will destroy all ecosystems."*  
  → **Credible**, if interpreted with added context. While some ecosystems may adapt, many are at severe risk.
---
## Not Credible
Assign this label if the statement:
- Contradicts scientific consensus or lacks reliable evidence.
- Is based on flawed reasoning, misleading framing, or speculative claims without scientific backing.
- Contains factual inaccuracies that distort public understanding of the issue.
**Examples**:
- *"CO2 increases are mainly due to natural causes, not humans."*  
  → **Not Credible**. Overwhelming evidence shows fossil fuel emissions are the primary cause.
- *"Greenland's ice cores show no significant warming, disproving climate change."*  
  → **Not Credible**. Scientific data confirms Greenland’s warming trends.
- *"The Atlantic is cooling, and scientists don't know why."*  
  → **Not Credible**. Misleading due to cherry-picking short-term anomalies.
---
## Instructions
1. **Analyze** the statement's factual accuracy and scientific reasoning.
2. **Choose one label**: `Credible` or `Not Credible`.
3. **Provide a brief explanation** justifying the label.
4. **If necessary**, identify missing context or evidence and explain why it matters.
'''