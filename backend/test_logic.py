from app.core.logic import calculate_reliability_score

def test_logic():
    # Test 1: Reliable content
    reliable = "The official government report states that the city parks will open next Monday. View details at https://gov.uk/parks"
    res1 = calculate_reliability_score(reliable)
    print(f"Test 1 (Reliable): Score={res1['score']}, Label={res1['label']}")
    assert res1['score'] >= 80

    # Test 2: Suspicious content (Caps + Keywords)
    suspicious = "SHOCKING EMERGENCY ALERT!!! MIRACLE CURE FOR EVERYTHING REVEALED!!!! SECRET LEAKED BY DOCTORS!! SHARE NOW!!!"
    res2 = calculate_reliability_score(suspicious)
    print(f"Test 2 (Suspicious): Score={res2['score']}, Label={res2['label']}")
    assert res2['score'] < 50

    # Test 3: Mixed content
    mixed = "I heard there is a secret leaked about the new phone, check bit.ly/click-here for more."
    res3 = calculate_reliability_score(mixed)
    print(f"Test 3 (Mixed): Score={res3['score']}, Label={res3['label']}")
    assert 50 <= res3['score'] < 80

    print("All tests passed!")

if __name__ == "__main__":
    test_logic()
