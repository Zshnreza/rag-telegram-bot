from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
from rag import retrieve, generate_answer

TOKEN = "8013382238:AAGNX19MZIeQQBhcrAdNK7l0boAiwWXIavs"

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("🤖 RAG Bot Ready! Use /ask <question>")

async def help_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("""
Commands:
/ask <question> - Ask from documents
/help - Show help
""")

async def ask(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = " ".join(context.args)

    if not query:
        await update.message.reply_text("Please provide a question.")
        return

    docs = retrieve(query)
    answer = generate_answer(query, docs)

    sources = "\n".join([name for _, name in docs])

    response = f"{answer}\n\n📄 Sources:\n{sources}"

    await update.message.reply_text(response)

app = ApplicationBuilder().token(TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("help", help_cmd))
app.add_handler(CommandHandler("ask", ask))

print("🚀 Bot running...")
app.run_polling()
