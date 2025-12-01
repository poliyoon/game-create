import google.generativeai as genai
import os

def get_api_key():
    try:
        with open('.env', 'r', encoding='utf-8') as f:
            content = f.read().strip()
            lines = [line.strip() for line in content.split('\n') if line.strip() and not line.strip().startswith('#')]
            return lines[-1] if lines else None
    except FileNotFoundError:
        print("Error: .env file not found.")
        return None

def test_image_generation():
    api_key = get_api_key()
    if not api_key:
        print("No API key found")
        return

    genai.configure(api_key=api_key)
    
    # Try with the exact model name from the list
    model_name = "imagen-4.0-fast-generate-001"
    print(f"Testing image generation with model: {model_name}")
    
    try:
        imagen = genai.ImageGenerationModel(model_name)
        
        prompt = "A futuristic city with flying cars, concept art"
        print(f"Prompt: {prompt}")
        
        result = imagen.generate_images(
            prompt=prompt,
            number_of_images=1,
        )
        
        if result.images:
            output_file = "test_image.png"
            result.images[0].save(output_file)
            print(f"✅ Success! Image saved to {output_file}")
        else:
            print("❌ No images returned")
            
    except Exception as e:
        print(f"❌ Error with {model_name}: {e}")
        
        # Try with 'models/' prefix
        try:
            model_name_prefix = f"models/{model_name}"
            print(f"\nRetrying with prefix: {model_name_prefix}")
            imagen = genai.ImageGenerationModel(model_name_prefix)
            result = imagen.generate_images(
                prompt=prompt,
                number_of_images=1,
            )
            if result.images:
                output_file = "test_image_prefix.png"
                result.images[0].save(output_file)
                print(f"✅ Success with prefix! Image saved to {output_file}")
        except Exception as e2:
            print(f"❌ Error with prefix: {e2}")

if __name__ == "__main__":
    test_image_generation()
