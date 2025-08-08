# utils/ner.py
import spacy
from collections import defaultdict

nlp = spacy.load("en_core_web_sm")

def extract_entities(text: str):
    doc = nlp(text)
    entities = defaultdict(list)
    for ent in doc.ents:
        entities[ent.label_].append(ent.text)
    # Convert to plain dict with unique lists
    return {k: list(dict.fromkeys(v)) for k, v in entities.items()}
