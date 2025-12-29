import os
from google import genai
from dotenv import load_dotenv

# تحميل المفتاح
load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    print("❌ Error: API Key not found in .env")
else:
    print(f"🔑 Using API Key starting with: {api_key[:5]}...")
    
    try:
        client = genai.Client(api_key=api_key)
        print("\n📡 Connecting to Google Servers to list available models...")
        
        # جلب القائمة
        models = client.models.list()
        
        found_any = False
        print("\n✅ Available Gemini Models for you:")
        for m in models:
            # نظهر فقط الموديلات التي تدعم إنشاء المحتوى (generateContent)
            if "gemini" in m.name and "generateContent" in (m.supported_actions or []):
                print(f" -> {m.name}")
                found_any = True
                
        if not found_any:
            print("⚠️ No compatible Gemini models found. Check if your API Key has access.")
            
    except Exception as e:
        print(f"\n❌ Connection Error: {e}")