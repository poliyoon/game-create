import google.generativeai as genai

# Read API key
with open('.env', 'r', encoding='utf-8') as f:
    api_key = f.read().strip().split('\n')[-1].strip()

print(f"API Key loaded: {api_key[:10]}...")

# Configure API
genai.configure(api_key=api_key)

# List available models
with open('available_models.txt', 'w', encoding='utf-8') as f:
    f.write("Available models:\n\n")
    for model in genai.list_models():
        f.write(f"Model: {model.name}\n")
        if hasattr(model, 'supported_generation_methods'):
            f.write(f"  Supported methods: {model.supported_generation_methods}\n")
        f.write("\n")

print("Model list saved to available_models.txt")
