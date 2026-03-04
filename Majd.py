import logging
import google.generativeai as genai
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, MessageHandler, CommandHandler, filters

# --- الإعدادات ---
API_KEY = "AIzaSyCQqyxZkctebYN0SYcjrHH7viatXlxlF8I"
TOKEN = "8605870679:AAHRGMVDVLMjcly2NXEw0-1VrqXkhOimsH8"

# إعداد الـ API بشكل يضمن الوصول للموديل
genai.configure(api_key=API_KEY)

# استخدام الإصدار المستقر v1 بدلاً من v1beta
model = genai.GenerativeModel(
    model_name='gemini-1.5-flash',
    generation_config={"temperature": 0.7}
)

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_text = update.message.text
    try:
        # طلب الرد من جيميني
        response = model.generate_content(user_text)

        if response and response.text:
            # تطبيق قاعدتك (Majd -> رجال الله)
            final_reply = response.text.replace("Majd", "رجال الله").replace("majd", "رجال الله")
            await update.message.reply_text(final_reply)
        else:
            await update.message.reply_text("تلقيت الرسالة ولكن جيميني لم يرسل نصاً. حاول صياغة السؤال بشكل آخر.")

    except Exception as e:
        # طباعة الخطأ لمعرفة إذا كان هناك حظر جرافي أو مشكلة مفتاح
        error_msg = str(e)
        print(f"--- الخطأ المكتشف --- \n {error_msg} \n ------------------")

        if "finish_reason" in error_msg:
            await update.message.reply_text("عذراً، المحتوى الذي طلبته قد تم حظره بواسطة فلاتر الأمان.")
        else:
            await update.message.reply_text("لا زلت أواجه صعوبة في الاتصال. سأحاول إصلاح ذلك فوراً.")


if __name__ == '__main__':
    application = ApplicationBuilder().token(TOKEN).build()
    application.add_handler(
        CommandHandler("start", lambda u, c: u.message.reply_text("مرحباً! أنا رجال الله، أحاول الاتصال الآن...")))
    application.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), handle_message))

    print("جاري المحاولة بالنسخة المستقرة الأصلية...")
    application.run_polling()