import os
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters
from openai import OpenAI
import logging

# Setup logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Get environment variables
BOT_TOKEN = os.environ.get('TELEGRAM_BOT_TOKEN')
OPENAI_API_KEY = os.environ.get('OPENAI_API_KEY')

if not BOT_TOKEN or not OPENAI_API_KEY:
    print("❌ Please set TELEGRAM_BOT_TOKEN and OPENAI_API_KEY")
    exit(1)

# Setup OpenAI
client = OpenAI(api_key=OPENAI_API_KEY)

PROMPT_TEXT = """
Transform this image into a painterly anime couture vision — 
where the softness of shoujo elegance meets the structured intensity of high-fashion. 
Focus on ultra-detailed textures, realistic lighting, precise color harmony, depth, and composition. 
Maintain all elements intact to preserve maximum visual impact and clarity. 
Do not simplify or remove any features; each aspect contributes to the overall emotional strength.
"""

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🎨 **Hello! Send me an image and I'll convert it to anime style**\n\n"
        "✨ **Features:**\n"
        "• Convert images to high-quality anime\n"
        "• Unique artistic style\n"
        "• 1024x1024 high resolution\n\n"
        "📸 **Just send me an image now!**"
    )

async def handle_photo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        await update.message.reply_text("🔄 Image received, processing... ⏳")

        # Download the sent photo
        photo_file = await update.message.photo[-1].get_file()
        photo_url = photo_file.file_path

        # Convert image using DALL-E 3
        response = client.images.generate(
            model="dall-e-3",
            prompt=PROMPT_TEXT,
            size="1024x1024",
            quality="standard",
            n=1,
        )

        # Get the result image URL
        image_url = response.data[0].url
        
        # Send the image to user
        await update.message.reply_photo(photo=image_url, caption="✅ **Your image has been converted!**\n\n🎨 In Painterly Anime Couture style")

    except Exception as e:
        logger.error(f"Error: {e}")
        await update.message.reply_text("❌ Error processing image. Please try later.")

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "📖 **How to use:**\n\n"
        "1. Send /start to begin\n"
        "2. Send any image directly\n"
        "3. Wait for processing to complete\n"
        "4. Receive your converted image\n\n"
        "⚡ **Notes:**\n"
        "• Processing takes 10-30 seconds\n"
        "• Quality: 1024x1024 pixels\n"
        "• Supports most image formats"
    )

def main():
    try:
        # Setup bot
        app = ApplicationBuilder().token(BOT_TOKEN).build()
        
        # Add handlers
        app.add_handler(CommandHandler("start", start))
        app.add_handler(CommandHandler("help", help_command))
        app.add_handler(MessageHandler(filters.PHOTO, handle_photo))

        print("🚀 Anime Painter Bot is running...")
        app.run_polling()
        
    except Exception as e:
        logger.error(f"Failed to start bot: {e}")

if __name__ == '__main__':
    main()
