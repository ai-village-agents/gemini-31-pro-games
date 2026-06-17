import urllib.request

try:
    url = "https://raw.githubusercontent.com/susam/adventure/master/walkthrough.txt"
    with urllib.request.urlopen(url) as response:
        text = response.read().decode('utf-8')
        for i, line in enumerate(text.splitlines()):
            if "trident" in line.lower() or "pearl" in line.lower() or "waterfall" in line.lower() or "clam" in line.lower():
                start = max(0, i - 2)
                end = min(len(text.splitlines()), i + 3)
                print(f"--- MATCH at line {i} ---")
                for j in range(start, end):
                    print(text.splitlines()[j])
except Exception as e:
    print(f"Error: {e}")
