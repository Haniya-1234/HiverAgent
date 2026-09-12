import os
import json
import urllib.request
import urllib.error

def test_cerebras():
    api_key = os.environ.get("CEREBRAS_API_KEY")
    if not api_key:
        print("Error: CEREBRAS_API_KEY environment variable not set.")
        return

    url = "https://api.cerebras.ai/v1/chat/completions"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}",
        "User-Agent": "Cerebras-Test/1.0"
    }
    
    # Use qwen-3.8-27b as a generic text evaluation model on Cerebras
    data = {
        "model": "qwen-3.8-27b", 
        "messages": [
            {"role": "user", "content": "Reply with exactly: CEREBRAS_TEST_OK"}
        ],
        "max_completion_tokens": 50,
        "temperature": 0.0
    }
    
    req = urllib.request.Request(url, data=json.dumps(data).encode('utf-8'), headers=headers)
    try:
        response = urllib.request.urlopen(req)
        result = json.loads(response.read().decode('utf-8'))
        
        # print only the returned text
        print(result['choices'][0]['message']['content'])
    except urllib.error.HTTPError as e:
        print(f"HTTPError: {e.code} - {e.read().decode('utf-8')}")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    test_cerebras()
