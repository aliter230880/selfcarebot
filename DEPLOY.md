# 🚀 Деплой SelfcareBot на Railway

## Шаг 1: Подготовка бота в Telegram

1. Открой [@BotFather](https://t.me/BotFather) в Telegram
2. Отправь `/newbot`
3. Введи имя бота (например: `My SelfCare Bot`)
4. Введи username (например: `myselfcare_bot`)
5. **Скопируй токен** (выглядит как `1234567890:ABCdefGHIjklMNOpqrsTUVwxyz`)

## Шаг 2: Настройка платежей (опционально)

1. В чате с @BotFather отправь `/mybots`
2. Выбери своего бота
3. Нажми `Bot Settings` → `Payments`
4. Выбери `Stripe TEST MODE` (для тестирования)
5. Перейди по ссылке к @StripeBot
6. Следуй инструкциям @StripeBot
7. Вернись в @BotFather — **скопируй PAYMENT_PROVIDER_TOKEN**

> ⚠️ **Для живых платежей:** подключи настоящий Stripe или ЮKassa через @BotFather

## Шаг 3: GitHub подготовка

### Вариант А: Через GitHub Desktop (проще)

1. Скачай [GitHub Desktop](https://desktop.github.com/)
2. Залогинься в GitHub
3. `File` → `New Repository`:
   - Name: `selfcarebot`
   - Local path: `E:\AI\AI_folder\SelfcareBot\extracted\SelfcareBot`
4. Нажми `Publish repository` (сними галку Private если хочешь публичный)

### Вариант Б: Через командную строку

```bash
cd E:\AI\AI_folder\SelfcareBot\extracted\SelfcareBot
git init
git add .
git commit -m "Initial commit"
# Создай репозиторий на github.com и выполни:
git remote add origin https://github.com/твой_username/selfcarebot.git
git push -u origin main
```

## Шаг 4: Деплой на Railway

1. Зайди на [railway.app](https://railway.app)
2. Нажми **Login** → войди через **GitHub**
3. Нажми **New Project**
4. Выбери **Deploy from GitHub repo**
5. Найди и выбери `selfcarebot` из списка
6. Railway начнёт деплой автоматически, но будет ошибка — нужны переменные!

## Шаг 5: Добавь переменные окружения в Railway

1. На странице проекта нажми на сервис (он называется `selfcarebot`)
2. Перейди на вкладку **Variables**
3. Нажми **New Variable** и добавь:

```
BOT_TOKEN = твой_токен_от_BotFather
PAYMENT_PROVIDER_TOKEN = токен_от_Stripe_через_BotFather
DATABASE_PATH = /app/selfcare.db
```

4. Нажми **Deploy** (или Railway автоматически перезапустит бота)

## Шаг 6: Проверка

1. Открой Telegram
2. Найди своего бота по username
3. Отправь `/start`
4. Если бот ответил — **всё работает! 🎉**

## Логи и отладка

В Railway:
- **Deployments** → нажми на последний деплой → **View Logs**
- Там увидишь ошибки если что-то не работает

## Бесплатные лимиты Railway (2026)

- ✅ 500 часов выполнения в месяц (хватает на 24/7)
- ✅ 512 MB RAM
- ✅ 1 GB диска
- ⚠️ Если лимит закончится, бот остановится

## Альтернативы Railway

- **Render.com** — 750 часов бесплатно
- **Fly.io** — 3 микро-VM бесплатно
- **VPS Reg.ru** — если хочешь полный контроль (платно)

## Проблемы?

### Бот не отвечает
- Проверь логи в Railway (Deployments → View Logs)
- Убедись что `BOT_TOKEN` правильный

### Ошибка при оплате
- Проверь `PAYMENT_PROVIDER_TOKEN`
- В тестовом режиме используй карту `4242 4242 4242 4242`

### База данных пропадает при рестарте
- Railway не сохраняет файлы между деплоями
- Для продакшена используй PostgreSQL (можно добавить в Railway бесплатно)

---

**Готово!** Твой бот теперь работает 24/7 🚀
