from telegram import Update, LabeledPrice
from telegram.ext import ContextTypes

# Настройки подписок (in cents / kopecks)
PLANS = {
    'monthly': {
        'title': '🌟 Premium на 1 месяц',
        'description': 'Безлимитные воспоминания, AI-советы и приоритетная поддержка',
        'payload': 'premium_monthly',
        'currency': 'RUB',
        'price': 29900,  # 299 рублей
        'label': 'Premium 1 месяц',
    },
    'yearly': {
        'title': '🚀 Premium на 1 год',
        'description': 'Всё включено + эксклюзивные функции. Скидка 40%',
        'payload': 'premium_yearly',
        'currency': 'RUB',
        'price': 214800,  # 2148 рублей
        'label': 'Premium 1 год',
    },
}


async def buy_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Show payment plans"""
    text = (
        '💎 **Premium-доступ**\n\n'
        'Базовый бот бесплатный. Premium даёт:\n'
        '✅ Безлимитное количество воспоминаний\n'
        '✅ Теги для воспоминаний\n'
        '✅ Ежедневные напоминания о самоуходе\n'
        '✅ AI-советы по настроению\n\n'
        'Выбери тариф:\n'
        '/buy\_monthly — 299 ₽/месяц\n'
        '/buy\_yearly — 2148 ₽/год (скидка 40%!)'
    )
    await update.message.reply_text(text, parse_mode='Markdown')


async def buy_monthly_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await _send_invoice(update, context, 'monthly')


async def buy_yearly_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await _send_invoice(update, context, 'yearly')


async def _send_invoice(update: Update, context: ContextTypes.DEFAULT_TYPE, plan_key: str):
    from config import PAYMENT_PROVIDER_TOKEN
    plan = PLANS[plan_key]
    prices = [LabeledPrice(plan['label'], plan['price'])]
    await context.bot.send_invoice(
        chat_id=update.effective_chat.id,
        title=plan['title'],
        description=plan['description'],
        payload=plan['payload'],
        provider_token=PAYMENT_PROVIDER_TOKEN,
        currency=plan['currency'],
        prices=prices,
        max_tip_amount=50000,
        suggested_tip_amounts=[10000, 20000, 50000],
        protect_content=False,
    )


async def precheckout_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Validate before payment"""
    query = update.pre_checkout_query
    if query.invoice_payload in ('premium_monthly', 'premium_yearly'):
        await query.answer(ok=True)
    else:
        await query.answer(ok=False, error_message='Неизвестный тариф. Пожалуйста, напиши /buy')


async def successful_payment_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle successful payment"""
    payment = update.message.successful_payment
    user_id = update.effective_user.id
    payload = payment.invoice_payload

    # Здесь можно сохранить в БД и выдать Premium-доступ
    # Пример: activate_premium(user_id, payload)

    amount = payment.total_amount / 100
    currency = payment.currency

    await update.message.reply_text(
        f'✅ Оплата прошла! {amount} {currency}\n\n'
        '🌟 Добро пожаловать в Premium!\n'
        'Теперь у тебя есть доступ ко всем функциям ❤️'
    )
