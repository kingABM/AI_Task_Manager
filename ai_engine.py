import os
from dotenv import load_dotenv
import chromadb
from sentence_transformers import SentenceTransformer
from google import genai
import arabic_reshaper
from bidi.algorithm import get_display

# 1. تهيئة البيئة والمفاتيح الأمنية
load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")

print("System Ignition: Loading AI Engine Components...")

# 2. تشغيل المحركات المحلية والسحابية
# المحرك المحلي للترجمة الرياضية
embed_model = SentenceTransformer('all-MiniLM-L6-v2', device='cpu')

# الاتصال بقاعدة البيانات المتجهة ChromaDB التي تم شحنها بالتاسكات
chroma_client = chromadb.PersistentClient(path="./chroma_db")
vector_collection = chroma_client.get_collection(name="tasks_vectors")

# تهيئة عميل جوجل جيميناي الحديث (الجيل الجديد)
client = genai.Client(api_key=api_key)

# 3. دالة الاستعلام والربط الذكي (The RAG Pipeline)
def ask_ai_manager(user_query):
    print(f"\n[User Input]: {user_query}")
    print("Step 1: Converting query to Vector...")
    
    # تحويل سؤال المستخدم إلى أرقام بنفس المترجم المحلي
    query_vector = embed_model.encode(user_query).tolist()
    
    print("Step 2: Scanning ChromaDB for matching contexts...")
    # البحث في قاعدة البيانات المتجهة عن أفضل 3 مهام قريبة لمعنى السؤال
    results = vector_collection.query(
        query_embeddings=[query_vector],
        n_results=3
    )
    
    # استخراج النصوص الأصلية للتاسكات التي عثر عليها المحرك
    retrieved_docs = results.get('documents', [[]])[0]
    context = "\n".join(retrieved_docs)
    
    if not context:
        context = "لا توجد مهام متعلقة بهذا الاستفسار في قاعدة البيانات حالياً."
        
    print("Step 3: Injecting context and invoking Gemini Core...")
    # بناء الـ Prompt الهندسي المدعم بالبيانات الحقيقية
    prompt = f"""
    أنت مساعد ذكي ومحلل نظم خبير لإدارة المهام الشخصية. 
    بناءً على المهام المستخرجة من قاعدة البيانات التالية فقط، أجب على سؤال المستخدم بدقة واحترافية وبلهجة مصرية مشجعة (مثلا استخدم: يا هندسة، يا بطل).

    المهام المتاحة المستخرجة (Context):
    {context}

    سؤال المستخدم الحالي (Query):
    {user_query}
    """
    
    # إرسال الطلب النهائي المتكامل لعقل الذكاء الاصطناعي في جوجل
    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt
    )
    
    return response.text

# 4. بروتوكول التشغيل والاختبار الذاتي
if __name__ == "__main__":
    # اكتب هنا أي سؤال يخطر على بالك بخصوص الـ 6 تاسكات الموجدين في قاعدة بياناتك
    my_question = "قولي إيه هي المهام اللي المفروض اشتغل عليها دلوقتي؟"
    
    response = ask_ai_manager(my_question)
    
    print("\n" + "="*50)
    print(" AI TASK MANAGER RESPONSE:")
    print("="*50)
    reshaped_text = arabic_reshaper.reshape(response)
    bidi_text = get_display(reshaped_text)
    print(bidi_text)