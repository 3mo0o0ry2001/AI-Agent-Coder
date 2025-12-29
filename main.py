import os
import subprocess
import time
from openai import OpenAI
from dotenv import load_dotenv

# 1. إعداد الاتصال بـ OpenRouter
load_dotenv()
api_key = os.getenv("OPENROUTER_API_KEY")

if not api_key:
    raise ValueError("OPENROUTER_API_KEY not found in .env file")

# OpenRouter متوافق تماماً مع مكتبة OpenAI
client = OpenAI(
  base_url="https://openrouter.ai/api/v1",
  api_key=api_key,
)

# 2. دالة توليد الكود
def generate_code_solution(task_description, previous_error=None):
    
    system_prompt = "You are an expert Python programmer. Return ONLY raw Python code. No markdown. No explanations."
    
    # سنطلب من الموديل التفكير خطوة بخطوة كما في تقنيات 2025
    user_content = f"Task: {task_description}"
    if previous_error:
        user_content += f"\n\nFix this error and return only the corrected code:\n{previous_error}"

    try:
        response = client.chat.completions.create(
            # استخدمنا موديل مجاني ومستقر جداً
            model="meta-llama/llama-3.3-70b-instruct:free",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_content}
            ]
        )
        
        code = response.choices[0].message.content
        # تنظيف الكود من أي علامات تنسيق زائدة
        code = code.replace("```python", "").replace("```", "").strip()
        return code
        
    except Exception as e:
        return f"# API Error: {str(e)}"

# 3. دالة تشغيل الكود
def run_generated_code(code_string):
    if code_string.startswith("# API Error"):
        return False, code_string

    filename = "temp_solution.py"
    with open(filename, "w", encoding="utf-8") as f:
        f.write(code_string)
    
    try:
        result = subprocess.run(
            ["python", filename], 
            capture_output=True, 
            text=True, 
            timeout=5 
        )
        return (result.returncode == 0, result.stdout if result.returncode == 0 else result.stderr)
    except Exception as e:
        return False, str(e)

# --- التشغيل ---
if __name__ == "__main__":
    my_task = "Write a python script to calculate the factorial of 5 and print it."
    print(f"🚀 Starting OpenRouter Agent for task: {my_task}\n")
    
    code = generate_code_solution(my_task)
    
    for i in range(3):
        print(f"--- Attempt {i+1} ---")
        success, output = run_generated_code(code)
        
        if success:
            print(f"✅ Success! Output: {output.strip()}")
            break
        else:
            print(f"❌ Error: {output.strip()}")
            print("🔄 Agent is rethinking...")
            code = generate_code_solution(my_task, previous_error=output)