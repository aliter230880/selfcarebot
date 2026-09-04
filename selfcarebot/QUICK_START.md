# ⚡ Быстрый старт за 5 минут

## 1️⃣ Создай бота (2 минуты)

Открой [@BotFather](https://t.me/BotFather) в Telegram:

```
/newbot
My SelfCare Bot
myselfcare_bot
```

**Скопируй токен!** Выглядит так: `1234567890:ABCdefGHI...`

---

## 2️⃣ Залей на GitHub (1 минута)

### Через GitHub Desktop:
1. Скачай: https://desktop.github.com/
2. `File` → `New Repository` → Name: `selfcarebot`
3. Local path: `E:\AI\AI_folder\SelfcareBot\extracted\SelfcareBot`
4. `Publish repository`

### Или через консоль:
```powershell
cd E:\AI\AI_folder\SelfcareBot\extracted\SelfcareBot
git init
git add .
git commit -m "Initial"
# Создай репо на github.com, потом:
git remote add origin https://github.com/USERNAME/selfcarebot.git
git push -u origin main
```

---

## 3️⃣ Деплой на Railway (2 минуты)

1. Открой: https://railway.app
2. **Login** → через GitHub
3. **New Project** → **Deploy from GitHub repo** → выбери `selfcarebot`
4. Нажми на сервис → **Variables** → **New Variable**:

```
BOT_TOKEN = вставь_твой_токен_сюда
DATABASE_PATH = /app/selfcare.db
```

5. Сохрани — Railway перезапустит бота автоматически

---

## ✅ Готово!

Открой Telegram → найди `@myselfcare_bot` → `/start`

Если отвечает — **работает!** 🎉

---

## 💳 Добавить оплаты (опционально)

1. @BotFather → `/mybots` → твой бот → `Bot Settings` → `Payments`
2. Выбери `Stripe TEST MODE`
3. Следуй инструкциям @StripeBot
4. Скопируй токен провайдера
5. Railway → Variables → добавь:
```
PAYMENT_PROVIDER_TOKEN = токен_от_stripe
```

**Тестовая карта:** `4242 4242 4242 4242`, срок любой будущий, CVC любой

---

## 🔧 Частые проблемы

**Бот не отвечает:**
- Railway → Deployments → View Logs — смотри ошибки
- Проверь что `BOT_TOKEN` правильный

**Хочу остановить бота:**
- Railway → Settings → Delete Service

**Хочу обновить код:**
- Сделай commit в GitHub — Railway обновится автоматически

---

## 📚 Полная инструкция

Смотри файл `DEPLOY.md` в этой папке
