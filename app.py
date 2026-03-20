from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
from rag import retrieve, generate_answer

user_memory = {}

TOKEN = "8013382238:AAGNX19MZIeQQBhcrAdNK7l0boAiwWXIavs"

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("🤖 RAG Bot Ready! Use /ask <question>")

async def help_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("""
Commands:
/ask <question> - Ask from documents
/summarize - Summarize conversation
/help - Show help
""")

async def ask(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    query = " ".join(context.args)

    if not query:
        await update.message.reply_text("Please provide a question.")
        return

    # Initialize memory
    if user_id not in user_memory:
        user_memory[user_id] = []

    # Get last 3 messages
    history = user_memory[user_id][-3:]
    history_text = "\n".join(history)

    # Retrieve docs
    docs = retrieve(query)

    # Combine history + current question
    full_query = f"Previous conversation:\n{history_text}\n\nCurrent question:\n{query}"

    answer = generate_answer(full_query, docs)

    # Save memory
    user_memory[user_id].append(f"Q: {query}\nA: {answer}")

    sources = "\n".join([name for _, name in docs])

    response = f"{answer}\n\n📄 Sources:\n{sources}"

    await update.message.reply_text(response)

async def summarize(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id

    if user_id not in user_memory or not user_memory[user_id]:
        await update.message.reply_text("No conversation to summarize.")
        return

    history = "\n".join(user_memory[user_id][-5:])

    summary_prompt = f"Summarize this conversation briefly:\n{history}"

    docs = retrieve(history)
    summary = generate_answer(summary_prompt, docs)

    await update.message.reply_text(f"📝 Summary:\n{summary}")
    

app = ApplicationBuilder().token(TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("help", help_cmd))
app.add_handler(CommandHandler("ask", ask))
app.add_handler(CommandHandler("summarize", summarize))

print("🚀 Bot running...")
app.run_polling()
