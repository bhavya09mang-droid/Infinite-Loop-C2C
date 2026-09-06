import re
from collections import defaultdict

def clean_text(text):
    """Convert webpage text to lowercase and remove extra whitespace."""

    if not isinstance(text, str):
        raise TypeError("text must be a string")

    text = text.lower()
    text = re.sub(r"\s+", " ", text)

    return text.strip()



PATTERNS = {

  
    "urgency": [

        r"\bhurry\b",

        r"\bact\s+now\b",

        r"\bbuy\s+now\b",

        r"\border\s+now\b",

        r"\blimited\s+time\b",

        r"\bends?\s+soon\b",

        r"\boffer\s+ends?\b",

        r"\bdeal\s+ends?\b",

        r"\blast\s+chance\b",

        r"\bdon'?t\s+miss\s+out\b",
    ],


   
    "scarcity": [

        r"\bonly\s+\d+\s+(?:left|remaining|items?|units?)\b",

        r"\b(?:limited|low)\s+(?:stock|inventory|availability)\b",

        r"\bonly\s+\d+\s+available\b",

        r"\bwhile\s+stocks?\s+last\b",

        r"\blimited\s+availability\b",

        r"\bselling\s+fast\b",

        r"\balmost\s+sold\s+out\b",

        r"\bonly\s+a\s+few\s+left\b",
    ],


    
    "confirmshaming": [

        
        r"\bno[,\.\s]+(?:thanks|thank\s+you)[,\.\s]+"
        r"(?:i\s+)?(?:don't|do\s+not)\s+(?:want|need)\b",

        
        r"\bno[,\.\s]+(?:thanks|thank\s+you)\b",

        
        r"\bi\s+(?:don't|do\s+not)\s+want\b",

        
        r"\bi\s+(?:don't|do\s+not)\s+need\b",

        
        r"\bi\s+prefer\s+not\s+to\b",

        
        r"\bi'?ll\s+pass\b",
    ],


    
    "drip_pricing": [

        r"\bhandling\s+fee\b",

        r"\bservice\s+fee\b",

        r"\bprocessing\s+fee\b",

        r"\bplatform\s+fee\b",

        r"\bconvenience\s+fee\b",

        r"\bbooking\s+fee\b",

        r"\badditional\s+fee\b",

        r"\bextra\s+fee\b",

        r"\badditional\s+charge\b",

        r"\bextra\s+charge\b",
    ],


    
    "hidden_information": [

        r"\bsee\s+details\b",

        r"\bmore\s+details\b",

        r"\bshow\s+more\b",

        r"\bhidden\s+charges?\b",

        r"\bterms\s+and\s+conditions\b",

        r"\badditional\s+information\b",

        r"\bclick\s+here\s+for\s+details\b",

        r"\bconditions\s+apply\b",
    ]
}



def find_matches(text):
    """
    Search webpage text for dark-pattern signals.

    Returns:
        Dictionary containing matched text grouped
        by dark-pattern category.
    """

    text = clean_text(text)

    matches = defaultdict(list)

    for category, patterns in PATTERNS.items():

        
        detected_spans = []

        for pattern in patterns:

            regex = re.compile(pattern, re.IGNORECASE)

            for match in regex.finditer(text):

                start = match.start()
                end = match.end()

                
                overlaps = any(
                    start < existing_end and end > existing_start
                    for existing_start, existing_end
                    in detected_spans
                )

                if overlaps:
                    continue

                matches[category].append(match.group())
                detected_spans.append((start, end))

    return dict(matches)




def counts_from_matches(matches):
    """
    Convert detected matches into category counts.

    Example:

        {
            "urgency": ["hurry", "ends soon"],
            "scarcity": ["only 2 left"]
        }

    becomes:

        {
            "urgency": 2,
            "scarcity": 1
        }
    """

    return {
        category: len(hits)
        for category, hits in matches.items()
    }




def scan_text(text):
    """
    Main function used by the backend.

    Input:
        Raw webpage text

    Output:
        Category counts and detected matches.

    Risk scoring is NOT performed here.
    """

    matches = find_matches(text)

    counts = counts_from_matches(matches)

    
    for category in PATTERNS:
        counts.setdefault(category, 0)

    return {
        "counts": counts,
        "matches": matches
    }




if __name__ == "__main__":

    import json

    sample_text = """
    Flash Sale!

    Hurry! This offer ends soon.

    Only 2 left in stock!

    No thanks, I don't want this deal.

    A handling fee will be added at checkout.

    Please see details for additional information.
    """

    result = scan_text(sample_text)

    print("\n========== REGEX DETECTION RESULT ==========\n")

    print(json.dumps(result, indent=4))

    print("\n========== COUNTS SENT TO NLP ============\n")

    print(json.dumps(result["counts"], indent=4))