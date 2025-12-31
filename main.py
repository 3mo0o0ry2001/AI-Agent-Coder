import os
import subprocess
import datetime
from dotenv import load_dotenv
from openai import OpenAI

# إعداد مفاتيح البيئة
load_dotenv()
client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=os.getenv("OPENROUTER_API_KEY"),
)

def log_audit(task, attempts, success, final_output):
    """حفظ سجل تدقيق للعمليات لضمان المراقبة والحوكمة."""
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    status = "SUCCESS" if success else "FAILED"
    
    log_entry = (
        f"[{timestamp}] STATUS: {status}\n"
        f"Task: {task}\n"
        f"Attempts: {attempts}\n"
        f"Final Result: {final_output}\n"
        f"{'-'*50}\n"
    )
    
    with open("audit_log.txt", "a", encoding="utf-8") as f:
        f.write(log_entry)
    print(f"\n📝 Audit log updated: audit_log.txt")

def generate_code_solution(task, previous_error=None):
    """توليد الكود باستخدام نماذج التفكير (Reasoning Models)."""
    system_prompt = "You are an expert Python developer. Output ONLY clean Python code without markdown blocks."
    user_content = task
    
    if previous_error:
        user_content = f"Your previous code failed with this error: {previous_error}. Please think step-by-step and fix it.\nTask: {task}"

    response = client.chat.completions.create(
        model="meta-llama/llama-3.3-70b-instruct:free", # الموديل الذي نجحنا باستخدامه
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_content}
        ]
    )
    return response.choices[0].message.content.strip()

def run_generated_code(code):
    """تشغيل الكود في بيئة معزولة (Sandbox) والتقاط النتائج."""
    with open("temp_solution.py", "w", encoding="utf-8") as f:
        f.write(code)
    
    try:
        result = subprocess.run(
            ["python", "temp_solution.py"],
            capture_output=True, text=True, timeout=10
        )
        if result.returncode == 0:
            return True, result.stdout
        else:
            return False, result.stderr
    except Exception as e:
        return False, str(e)

if __name__ == "__main__":
    # المهمة الصعبة لاختبار الـ Custom Exceptions
    my_task = """Write a Python script that STRICTLY defines a custom class InsufficientFundsError(Exception). 
    Create a BankAccount with 100 AED. Attempt to withdraw 150 AED. 
    You MUST raise the custom exception and catch it to print 'Transaction Failed: Insufficient Funds'."""
    
    print(f"🚀 Starting AI Agent...")
    
    max_attempts = 3
    attempt = 1
    success = False
    last_error = None

    while attempt <= max_attempts:
        print(f"\n--- Attempt {attempt} ---")
        code = generate_code_solution(my_task, last_error)
        
        print("🔍 Analyzing & Executing...")
        success, output = run_generated_code(code)
        
        if success:
            print(f"✅ Success! Output: {output.strip()}")
            log_audit(my_task, attempt, True, output.strip())
            break
        else:
            print(f"❌ Error detected. Agent is rethinking...")
            last_error = output
            attempt += 1

    if not success:
        print("🛑 Failed after maximum attempts.")
        log_audit(my_task, max_attempts, False, "Max attempts reached.")