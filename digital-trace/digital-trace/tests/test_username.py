# tests/test_username.py
import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from utils.validator import validate_username

def test_valid_username():
    assert validate_username("johndoe") == True
    assert validate_username("john_doe123") == True
    assert validate_username("john.doe") == True

def test_invalid_username():
    assert validate_username("") == False
    assert validate_username("a" * 51) == False
    assert validate_username("john doe") == False   # spaces not allowed
    assert validate_username("<script>") == False

def test_dork_generator():
    from core.dork_generator import generate_dorks
    dorks = generate_dorks("example.com")
    assert isinstance(dorks, dict)
    assert len(dorks) > 0
    for cat, queries in dorks.items():
        for q in queries:
            assert "example.com" in q

def test_metadata_missing_file():
    from core.metadata_extractor import extract_metadata
    result = extract_metadata("/nonexistent/file.jpg")
    assert "error" in result

def test_validator_email():
    from utils.validator import validate_email
    assert validate_email("user@example.com") == True
    assert validate_email("notanemail") == False

def test_validator_ip():
    from utils.validator import validate_ip
    assert validate_ip("8.8.8.8") == True
    assert validate_ip("999.0.0.1") == False
    assert validate_ip("not-an-ip") == False

if __name__ == "__main__":
    tests = [test_valid_username, test_invalid_username, test_dork_generator,
             test_metadata_missing_file, test_validator_email, test_validator_ip]
    passed = 0
    for t in tests:
        try:
            t()
            print(f"  ✅ {t.__name__}")
            passed += 1
        except Exception as e:
            print(f"  ❌ {t.__name__}: {e}")
    print(f"\n{passed}/{len(tests)} tests passed")
