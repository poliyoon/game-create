import requests
import json
import os
import base64

def get_api_key():
    try:
        with open('.env', 'r', encoding='utf-8') as f:
            content = f.read().strip()
            lines = [line.strip() for line in content.split('\n') if line.strip() and not line.strip().startswith('#')]
            return lines[-1] if lines else None
    except FileNotFoundError:
        print("Error: .env file not found.")
        return None

def test_imagen_rest():
    api_key = get_api_key()
    if not api_key:
        print("No API key found")
        return

    model_name = "imagen-3.0-generate-001" # Try 3.0 first as it's more likely to be stable
    # Or try the one from the list: imagen-4.0-fast-generate-001
    model_name = "imagen-4.0-fast-generate-001"
    
    url = f"https://generativelanguage.googleapis.com/v1beta/models/{model_name}:predict?key={api_key}"
    
    headers = {
        "Content-Type": "application/json"
    }
    
    data = {
        "instances": [
            {
                "prompt": "A futuristic city with flying cars, concept art"
            }
        ],
        "parameters": {
            "sampleCount": 1,
            "aspectRatio": "16:9"
        }
    }
    
    print(f"Sending request to {url.split('?')[0]}...")
    
    try:
        response = requests.post(url, headers=headers, json=data)
        print(f"Status Code: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            # print(json.dumps(result, indent=2)[:500]) # Print first 500 chars
            
            if 'predictions' in result:
                prediction = result['predictions'][0]
                # The structure might be different depending on the model
                # It could be 'bytesBase64Encoded' or similar
                
                if 'bytesBase64Encoded' in prediction:
                    img_data = base64.b64decode(prediction['bytesBase64Encoded'])
                    with open("test_rest_image.png", "wb") as f:
                        f.write(img_data)
                    print("✅ Image saved to test_rest_image.png")
                elif 'mimeType' in prediction and 'bytesBase64Encoded' in prediction:
                     img_data = base64.b64decode(prediction['bytesBase64Encoded'])
                     with open("test_rest_image.png", "wb") as f:
                        f.write(img_data)
                     print("✅ Image saved to test_rest_image.png")
                else:
                    print("Unknown prediction format:", prediction.keys())
            else:
                print("No predictions found in response")
                print(result)
        else:
            print("Error response:")
            print(response.text)
            
    except Exception as e:
        print(f"Exception: {e}")

if __name__ == "__main__":
    test_imagen_rest()
