import telebot
import google.generativeai as genai

# الإعدادات التي استخرجناها من صورتك رقم 27
GOOGLE_API_KEY = "AIzaSyCQqyxZkctebYN0SYcjrHH7viatXlx1F8I"
TELEGRAM_TOKEN = "8605870679:AAHRGMVDVLMjcly2NXEw0-1VrqXkhOimsH8"

# تجهيز الذكاء الاصطناعي
genai.configure(api_key=GOOGLE_API_KEY)
model = genai.GenerativeModel('gemini-pro')

# تشغيل البوت
bot = telebot.TeleBot(TELEGRAM_TOKEN)

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "تم تفعيل بوت 'رجال الله' بنجاح! أنا الآن متصل بذكاء Gemini العالمي. اسألني أي شيء.")

@bot.message_handler(func=lambda message: True)
def handle_message(message):
    try:
        response = model.generate_content(message.text)
        bot.reply_to(message, response.text)
    except Exception as e:
        bot.reply_to(message, "حدث خطأ بسيط، سأحاول مجدداً.")

print("البوت انطلق...")
bot.infinity_polling()
