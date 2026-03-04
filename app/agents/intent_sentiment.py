from transformers import pipeline

intent_analyzer = pipeline(
    "zero-shot-classification",
    model="facebook/bart-large-mnli"
)

def analyze_intent(statement: str):
    labels = ["informative", "persuasive", "controversial", "misleading", "alarmist"]
    result = intent_analyzer(statement, labels)
    return {
        "intent": result["labels"][0],
        "score": result["scores"][0]
    }

sentiment_analyzer = pipeline(
    "text-classification",
    model="j-hartmann/emotion-english-distilroberta-base",
    top_k=1
)

def analyze_sentiment(statement: str):
    result = sentiment_analyzer(statement)
    return {
        "emotion": result[0][0]["label"].lower(),
        "score": result[0][0]["score"]
    }