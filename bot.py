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


TOKEN = os.environ["TOKEN"]
GEMINI_API_KEY = os.environ["GEMINI_API_KEY"]

client = genai.Client(api_key=GEMINI_API_KEY)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "مرحباً، أنا مساعدك الدراسي الذكي 📚"
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

    response = client.models.generate_content(
        model="gemini-3.7-flash",
        contents=prompt
    )

    await update.message.reply_text(response.text)


app = Application.builder().token(TOKEN).build()

app.add_handler(CommandHandler("start", start))

app.add_handler(
    MessageHandler(
        filters.TEXT & ~filters.COMMAND,
        reply
    )
)


PORT = int(os.environ.get("PORT", 10000))
WEBHOOK_URL = os.environ["WEBHOOK_URL"]

app.run_webhook(
    listen="0.0.0.0",
    port=PORT,
    webhook_url=WEBHOOK_URL
)app.run_polling()
