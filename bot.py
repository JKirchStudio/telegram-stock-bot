from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
import yfinance as yf
import asyncio

import os

TELEGRAM_BOT_TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN")

async def get_stock_data(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        ticker = context.args[0].upper()
        stock = yf.Ticker(ticker)

        info = stock.info

        price = info.get('regularMarketPrice') or info.get('previousClose') or 'N/A'
        day_high = info.get('dayHigh', 'N/A')
        day_low = info.get('dayLow', 'N/A')
        volume = info.get('volume', 'N/A')
        previous_close = info.get('previousClose', None)

        if isinstance(price, (int, float)) and isinstance(previous_close, (int, float)):
            change = price - previous_close
            change_pct = (change / previous_close) * 100 if previous_close != 0 else 0
            change_str = f"{change:.2f} ({change_pct:.2f}%)"
        else:
            change_str = 'N/A'

        message = (
            f"📊 *{ticker} Stock Data*\n"
            f"Price: {price}\n"
            f"Change: {change_str}\n"
            f"Day High: {day_high}\n"
            f"Day Low: {day_low}\n"
            f"Volume: {volume}"
        )

        await update.message.reply_text(message, parse_mode='Markdown')
    except IndexError:
        await update.message.reply_text("❌ Usage: /stock SYMBOL\nExample: /stock MSFT")
    except Exception as e:
        await update.message.reply_text(f"⚠️ Error: {e}")

async def main():
    app = ApplicationBuilder().token(TELEGRAM_BOT_TOKEN).build()
    app.add_handler(CommandHandler("stock", get_stock_data))
    await app.run_polling()

if __name__ == '__main__':
    asyncio.run(main())
