import google.generativeai as genai

print("Attributes of google.generativeai:")
for attr in dir(genai):
    print(f"- {attr}")
