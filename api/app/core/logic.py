import re
from typing import Dict, List, Any

TRUSTED_DOMAINS = ["bbc.co.uk", "reuters.com", "apnews.com", "nytimes.com", "wsj.com", "npr.org", "theguardian.com", "nature.com", "science.org", "gov.uk", "gov", "edu"]
SUSPICIOUS_DOMAINS = ["bit.ly", "tinyurl.com", "clickbait.news", "real-truth.net", "secret-revealed.co"]

SUSPICIOUS_KEYWORDS = [
    "miracle cure", "secret leaked", "hidden truth", "they don't want you to know",
    "scam", "must share", "guaranteed", "100% real", "don't miss out", "emergency alert",
    "breaking news!!", "SHOCKING", "unbelievable", "conspiracy", "leak"
]

def extract_links(text: str) -> List[str]:
    # Regex to catch http/https links and common domain patterns
    return re.findall(r'((?:https?://|www\.)[^\s]+|(?:[a-zA-Z0-9-]+\.)+(?:com|org|net|gov|uk|io|ly|edu|news|net)[^\s]*)', text)

def get_domain(url: str) -> str:
    domain = re.sub(r'https?://(www\.)?', '', url).split('/')[0]
    return domain.lower()

def calculate_reliability_score(content: str) -> Dict[str, Any]:
    score = 100
    risky_keywords_found = []
    links = extract_links(content)
    
    # 1. Check Keywords (Avoid double-counting sub-strings)
    content_lower = content.lower()
    # Sort by length descending to catch longer phrases first
    sorted_keywords = sorted(SUSPICIOUS_KEYWORDS, key=len, reverse=True)
    
    temp_content = content_lower
    for kw in sorted_keywords:
        if kw.lower() in temp_content:
            score -= 10
            risky_keywords_found.append(kw)
            # Remove from temp_content to avoid sub-phrase double counting
            temp_content = temp_content.replace(kw.lower(), "[FOUND]")
            
    # 2. Check ALL CAPS
    words = content.split()
    if len(words) > 5:
        caps_words = [w for w in words if w.isupper() and len(w) > 1]
        if len(caps_words) / len(words) > 0.5:
            score -= 15
            
    # 3. Excessive Punctuation
    if re.search(r'[!?]{3,}', content):
        score -= 10
        
    # 4. Domain Check
    found_domains = []
    for link in links:
        domain = get_domain(link)
        if domain in found_domains: continue
        found_domains.append(domain)
        
        if any(td in domain for td in TRUSTED_DOMAINS):
            score += 10
        elif any(sd in domain for sd in SUSPICIOUS_DOMAINS):
            score -= 20
            
    # Clamp score
    score = max(0, min(100, score))
    
    # Determine Label
    if score >= 85: # Tightened for Reliable
        label = "Likely Reliable"
    elif score >= 60:
        label = "Needs Verification"
    else:
        label = "Suspicious"
        
    return {
        "score": score,
        "label": label,
        "risky_keywords": list(set(risky_keywords_found)),
        "links": links
    }
