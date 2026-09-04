import logging
from telegram import Update
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    PreCheckoutQueryHandler,
    ContextTypes,
    filters,
)
from config import BOT_TOKEN
from database import init_db, add_user, save_memory, get_random_memory, get_all_memories, delete_memory
from payments import (
    buy_cmd,
    buy_monthly_cmd,
    buy_yearly_cmd,
    precheckout_callback,
    successful_payment_callback,
)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

RECOMMENDATIONS = {
    'еда': [
        '🍕 Закажи любимую пиццу и насладись вечером',
        '🍜 Приготовь что-то новое по рецепту из интернета',
        '☕ Сходи в уютное кафе и выпей кофе',
    ],
    'спорт': [
        '🚶 Прогуляйся 30 минут на свежем воздухе',
        '🧘 Попробуй 10 минут медитации или йоги',
        '🚴 Покатайся на велосипеде или самокате',
    ],
    'отдых': [
        '📺 Посмотри серию любимого сериала',
        '📚 Почитай книгу 20 минут',
        '🎮 Поиграй в любимую игру',
        '🛁 Прими расслабляющую ванну',
    ],
}


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    add_user(user.id, user.username, user.first_name)
    await update.message.reply_text(
        f'Привет, {user.first_name}! 🌟\n\n'
        'Я твой бот для самоухода. Вот что я умею:\n\n'
        '/save — сохранить приятное воспоминание\n'
        '/remember — показать случайное воспоминание\n'
        '/list — все мои воспоминания\n'
        '/delete <id> — удалить воспоминание\n'
        '/recommend — получить рекомендацию (еда/спорт/отдых)\n'
        '/buy — 💎 Premium-доступ\n\n'
        'Начни с /save и расскажи мне что-то хорошее из своего дня 😊'
    )


async def save_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        '✍️ Расскажи мне о приятном моменте — напиши его следующим сообщением:'
    )
    context.user_data['awaiting_memory'] = True


async def remember_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    memory = get_random_memory(user_id)
    if memory:
        mem_id, text, created_at = memory
        date = created_at[:10] if created_at else ''
        await update.message.reply_text(
            f'🌈 Вот одно из твоих воспоминаний (#{mem_id}, {date}):\n\n{text}'
        )
    else:
        await update.message.reply_text(
            'У тебя пока нет сохранённых воспоминаний. Используй /save чтобы добавить первое!'
        )


async def list_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    memories = get_all_memories(user_id)
    if not memories:
        await update.message.reply_text('Список пуст. Добавь первое воспоминание командой /save')
        return
    text = '📋 Твои воспоминания:\n\n'
    for mem_id, mem_text, created_at in memories:
        date = created_at[:10] if created_at else ''
        preview = mem_text[:60] + '...' if len(mem_text) > 60 else mem_text
        text += f'#{mem_id} [{date}]: {preview}\n'
    await update.message.reply_text(text)


async def delete_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    if not context.args:
        await update.message.reply_text('Укажи ID воспоминания: /delete 3')
        return
    try:
        mem_id = int(context.args[0])
    except ValueError:
        await update.message.reply_text('ID должен быть числом, например: /delete 3')
        return
    if delete_memory(user_id, mem_id):
        await update.message.reply_text(f'✅ Воспоминание #{mem_id} удалено')
    else:
        await update.message.reply_text(f'Воспоминание #{mem_id} не найдено')


async def recommend_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    import random
    category = random.choice(list(RECOMMENDATIONS.keys()))
    tip = random.choice(RECOMMENDATIONS[category])
    await update.message.reply_text(
        f'💡 Рекомендация ({category}):\n\n{tip}'
    )


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if context.user_data.get('awaiting_memory'):
        user_id = update.effective_user.id
        text = update.message.text
        save_memory(user_id, text)
        context.user_data['awaiting_memory'] = False
        await update.message.reply_text(
            '💾 Сохранено! Я запомню этот момент.\n'
            'Используй /remember когда захочешь вспомнить что-то хорошее 🌟'
        )
    else:
        await update.message.reply_text(
            'Используй команды:\n'
            '/save — сохранить воспоминание\n'
            '/remember — вспомнить что-то хорошее\n'
            '/recommend — получить совет\n'
            '/buy — 💎 Premium'
        )


def main():
    init_db()
    app = Application.builder().token(BOT_TOKEN).build()

    # Основные команды
    app.add_handler(CommandHandler('start', start))
    app.add_handler(CommandHandler('save', save_cmd))
    app.add_handler(CommandHandler('remember', remember_cmd))
    app.add_handler(CommandHandler('list', list_cmd))
    app.add_handler(CommandHandler('delete', delete_cmd))
    app.add_handler(CommandHandler('recommend', recommend_cmd))

    # Оплата
    app.add_handler(CommandHandler('buy', buy_cmd))
    app.add_handler(CommandHandler('buy_monthly', buy_monthly_cmd))
    app.add_handler(CommandHandler('buy_yearly', buy_yearly_cmd))
    app.add_handler(PreCheckoutQueryHandler(precheckout_callback))
    app.add_handler(MessageHandler(filters.SUCCESSFUL_PAYMENT, successful_payment_callback))

    # Текстовые сообщения
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    logger.info('Бот запущен...')
    app.run_polling()


if __name__ == '__main__':
    main()
