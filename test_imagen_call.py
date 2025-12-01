import google.generativeai as genai
import os
import json

def get_api_key():
    try:
        with open('.env', 'r', encoding='utf-8') as f:
            content = f.read().strip()
            lines = [line.strip() for line in content.split('\n') if line.strip() and not line.strip().startswith('#')]
            return lines[-1] if lines else None
    except FileNotFoundError:
        print("Error: .env file not found.")
        return None

def test_imagen_call():
    api_key = get_api_key()
    if not api_key:
        print("No API key found")
        return

    genai.configure(api_key=api_key)
    
    # Try using GenerativeModel wrapper even if it says predict
    model_name = "imagen-4.0-fast-generate-001" 
    # Also try with 'models/' prefix
    
    print(f"Testing with model: {model_name}")
    
    try:
        model = genai.GenerativeModel(model_name)
        prompt = "A futuristic city with flying cars, concept art"
        
        print("Calling generate_content...")
        response = model.generate_content(prompt)
        
        print("Response received!")
        print(response)
        
        if response.parts:
            print("Response has parts")
            # Check for image data
            for part in response.parts:
                if hasattr(part, 'inline_data') and part.inline_data:
                    print("Found inline data (image)")
                    with open("test_imagen_gen.png", "wb") as f:
                        f.write(part.inline_data.data)
                    print("Saved image to test_imagen_gen.png")
                    return
        
        print("No image found in response")
        
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    test_imagen_call()
