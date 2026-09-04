@echo off
echo ========================================
echo   SelfCare Bot - Локальный запуск
echo ========================================
echo.

REM Проверка наличия .env файла
if not exist .env (
    echo [ОШИБКА] Файл .env не найден!
    echo.
    echo Скопируй .env.example в .env и заполни токены:
    echo   copy .env.example .env
    echo   notepad .env
    echo.
    pause
    exit /b 1
)

REM Проверка Python
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [ОШИБКА] Python не установлен!
    echo Скачай с https://python.org
    pause
    exit /b 1
)

echo [1/3] Проверка зависимостей...
pip install -r requirements.txt --quiet

echo [2/3] Инициализация базы данных...
echo.

echo [3/3] Запуск бота...
echo.
echo Бот запущен! Нажми Ctrl+C для остановки
echo ========================================
echo.

python bot.py

pause
