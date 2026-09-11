import os

from telegram import Update
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    ContextTypes,
    filters
)

from google import genai


# قراءة المفاتيح من Environment Variables
TOKEN = os.environ["TOKEN"]
GEMINI_API_KEY = os.environ["GEMINI_API_KEY"]

# الاتصال بـ Gemini
client = genai.Client(api_key=GEMINI_API_KEY)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "مرحباً، أنا مساعدك الدراسي الذكي 📚\n"
        "أرسل لي سؤالك وسأساعدك."
    )


async def reply(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_text = update.message.text

    prompt = f"""
أنت مساعد دراسة متخصص بالسادس الإعدادي العلمي العراقي.

مهمتك:
- اشرح الدروس بطريقة واضحة ومناسبة للطالب.
- أنشئ اختبارات وأسئلة تدريبية.
- ساعد الطالب على تنظيم وقته.
- تابع تقدمه الدراسي.
- إذا طلب الطالب حلاً، اشرح خطوات الحل وليس الجواب فقط.
- استخدم اللغة العربية.
- اجعل الشرح مناسباً للمنهج العراقي قدر الإمكان.

رسالة الطالب:
{user_text}
"""

    try:
        response = client.models.generate_content(
            model="gemini-3.7-flash",
            contents=prompt
        )

        await update.message.reply_text(response.text)

    except Exception as e:
        print(f"Gemini error: {e}")

        await update.message.reply_text(
            "حدث خطأ أثناء الاتصال بالذكاء الاصطناعي. حاول مرة أخرى."
        )


# إنشاء تطبيق Telegram
app = Application.builder().token(TOKEN).build()

# أمر /start
app.add_handler(
    CommandHandler("start", start)
)

# استقبال رسائل المستخدم
app.add_handler(
    MessageHandler(
        filters.TEXT & ~filters.COMMAND,
        reply
    )
)


# تشغيل البوت
app.run_polling()
