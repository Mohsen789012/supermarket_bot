import os
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, MessageHandler, filters
from dotenv import load_dotenv

# Load the bot token from .env file
load_dotenv()
BOT_TOKEN = os.getenv("BOT_TOKEN")

# Product categories and items
categories = {
    "تنقلات": ["تخمه آفتاب گردان", "آلبالو خشکه", "ترشک", "لواشک", "پفک", "چیپس", "شکلات خمیر دندونی فرمند", "آجیل روکش شکلاتی", "های بای"],
    "سُس و رُب": ["رب گوجه فرنگی", "رب انار", "لیموعمانی"],
    "صبحانه": ["حلوا شکری", "پنیر لیقوان"],
    "نوشیدنی": ["شربت سن ایچ", "آب انار سن ایچ"],
    "عطاری": ["گلاب یک و یک", "عرق شا تره"],
    "ترشی و شور": ["هفت بیجار", "شور", "سیر ترشی"],
    "زیتون پرورده": ["زیتون پرورده ۲۰۰ گرمی", "زیتون پرورده ۵۰۰ گرمی", "زیتون پرورده ۱ کیلویی", "زیتون پرورده ۲ کیلویی"],
    "سس‌ها": ["سس گلوریا سبز", "سس گلوریا قرمز"],
    "سبزی خشک و غذای آماده": ["سبزی خشک قرمه سبزی", "قرمه سبزی آماده"],
    "بارییکیو": ["سیخ کباب کوبیده ۶ عددی", "سیخ کباب کوبیده ۱۲ عددی", "سیخ جوجه کباب ۶ عددی", "سیخ جوجه کباب ۱۲ عددی", "باد بزن"],
    "آجیل و خرما": ["رطب", "پسته", "مویز", "انجیر خشک"],
    "قند و نبات": ["قند شکسته", "نبات سفید", "نیات زعفرانی"],
    "پودر ژله٬ پودر کیک": ["پودر ژله", "پودر کیک"],
    "ادویه": ["زرد چوبه"],
    "حبوبات و سویا": ["سویا", "لوبیا چی تی", "لوبیا قرمز"],
    "حراجی": ["زرد چویه", "پشمک حاج عبدلله"]
}

# Persistent menu buttons
persistent_menu = ReplyKeyboardMarkup(
    [["🛍 سبد خرید", "🏠 شروع"], ["📚 راهنما", "📞 ارتباط با ما"]],
    resize_keyboard=True,
    one_time_keyboard=False
)

# Start command
async def start(update: Update, context):
    chat_id = update.message.chat_id
    keyboard = [[InlineKeyboardButton("🛍 مشاهده دسته‌بندی کالاها", callback_data="categories")]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text(
        "سلام! به سوپرمارکت ما خوش آمدید 🛒‎",
        reply_markup=persistent_menu
    )
    await update.message.reply_text(
        "لطفاً یک گزینه را انتخاب کنید:",
        reply_markup=reply_markup
    )

# Show categories (edit previous message instead of sending a new one)
async def categories_menu(update: Update, context):
    query = update.callback_query
    await query.answer()

    keyboard = []
    category_list = list(categories.keys())

    for i in range(0, len(category_list), 2):  # Arrange categories in pairs
        row = [InlineKeyboardButton(category_list[i] + "‎", callback_data=category_list[i])]
        if i + 1 < len(category_list):
            row.append(InlineKeyboardButton(category_list[i + 1] + "‎", callback_data=category_list[i + 1]))
        keyboard.append(row)

    reply_markup = InlineKeyboardMarkup(keyboard)
    await query.message.edit_text("🔹 لطفاً یک دسته‌بندی را انتخاب کنید:", reply_markup=reply_markup)

# Show products in selected category (edit previous message)
async def show_products(update: Update, context):
    query = update.callback_query
    await query.answer()
    category = query.data

    if category in categories:
        keyboard = []
        for i in range(0, len(categories[category]), 2):
            row = [InlineKeyboardButton(categories[category][i] + "‎", callback_data=f"product_{categories[category][i]}")]
            if i + 1 < len(categories[category]):
                row.append(InlineKeyboardButton(categories[category][i + 1] + "‎", callback_data=f"product_{categories[category][i + 1]}"))
            keyboard.append(row)

        # Add a back button to return to categories
        keyboard.append([InlineKeyboardButton("🔙 بازگشت به دسته‌بندی‌ها", callback_data="categories")])
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.message.edit_text(f"🛒 محصولات دسته {category}:", reply_markup=reply_markup)

# Handle persistent menu button clicks
async def handle_menu_buttons(update: Update, context):
    text = update.message.text
    if text == "🛍 سبد خرید":
        await update.message.reply_text("سبد خرید شما خالی است.")
    elif text == "🏠 شروع":
        await start(update, context)
    elif text == "📚 راهنما":
        await update.message.reply_text("راهنمای استفاده از ربات:\n\n1. برای مشاهده محصولات، از دکمه 'شروع' استفاده کنید.\n2. برای افزودن محصول به سبد خرید، روی محصول کلیک کنید.\n3. برای ارتباط با ما، از دکمه 'ارتباط با ما' استفاده کنید.")
    elif text == "📞 ارتباط با ما":
        await update.message.reply_text("برای ارتباط با ما، لطفاً به آدرس زیر پیام دهید:\n@example_support")

# Main function  
def main():
    app = Application.builder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(categories_menu, pattern="categories"))
    app.add_handler(CallbackQueryHandler(show_products))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_menu_buttons))
    print("Bot is running...")
    app.run_polling()

if __name__ == "__main__":
    main()