import logging
import os
from telegram import Update
from telegram.ext import Application, MessageHandler, filters, ContextTypes

# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Your personal chat ID
YOUR_CHAT_ID = os.getenv('YOUR_CHAT_ID', '7035950028')

async def forward_photo(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """PhotoFWD bot - Forward photos from groups to personal inbox"""
    try:
        # Check if message is from a group
        if update.effective_chat.type in ['group', 'supergroup']:
            # Get photo info
            photo = update.message.photo[-1]  # Get highest resolution photo
            
            # Get group info
            group_name = update.effective_chat.title
            sender_name = update.message.from_user.first_name
            if update.message.from_user.last_name:
                sender_name += f" {update.message.from_user.last_name}"
            
            # Create caption with source info
            caption = f"📸 PhotoFWD\n🏢 From: {group_name}\n👤 Sender: {sender_name}"
            if update.message.caption:
                caption += f"\n💬 Caption: {update.message.caption}"
            
            # Forward photo to your personal chat
            await context.bot.send_photo(
                chat_id=YOUR_CHAT_ID,
                photo=photo.file_id,
                caption=caption
            )
            
            logger.info(f"PhotoFWD: Photo forwarded from {group_name} by {sender_name}")
            
    except Exception as e:
        logger.error(f"PhotoFWD Error: {e}")

async def error_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle errors for PhotoFWD bot"""
    logger.warning(f'Update {update} caused error {context.error}')

def main() -> None:
    """Start the bot"""
    # Get bot token from environment variable
    token = os.getenv('TELEGRAM_BOT_TOKEN')
    if not token:
        raise ValueError("Please set TELEGRAM_BOT_TOKEN environment variable")
    
    if not YOUR_CHAT_ID:
        raise ValueError("Please set YOUR_CHAT_ID environment variable")
    
    # Create application
    application = Application.builder().token(token).build()
    
    # Add handlers
    application.add_handler(MessageHandler(filters.PHOTO, forward_photo))
    application.add_error_handler(error_handler)
    
    # Start the bot
    logger.info("Starting PhotoFWD bot (@photofwdbot)...")
    application.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == '__main__':
    main()
