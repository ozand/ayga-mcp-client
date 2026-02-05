# ayga-mcp-client: Локальная установка для Claude Desktop

## ⚠️ Проблема: Конфликт версий зависимостей

При установке `ayga-mcp-client` в глобальную среду Python возникает конфликт:
- `mcp>=1.0.0` требует `starlette>=0.51.0`
- `fastapi 0.115.0` требует `starlette<0.39.0`
- `gradio 5.38.0` имеет другие требования к `fastapi` и `pydantic`

**Решение**: Использовать отдельный virtual environment для ayga-mcp-client

## ✅ Быстрая установка (Windows)

### Вариант 1: Автоматическая установка (рекомендуется)

```powershell
# 1. Скачайте скрипт установки
# (или используйте уже созданный: t:\Code\python\A-PARSER\setup-ayga-mcp.ps1)

# 2. Запустите в PowerShell (НЕ нужен администратор)
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
& .\setup-ayga-mcp.ps1

# Скрипт автоматически:
# ✅ Создаст virtual environment
# ✅ Установит ayga-mcp-client 1.4.1
# ✅ Покажет конфигурацию для Claude Desktop
# ✅ Протестирует установку
```

### Вариант 2: Ручная установка

```powershell
# 1. Создайте virtual environment
python -m venv $env:USERPROFILE\.mcp\ayga-venv

# 2. Активируйте
& "$env:USERPROFILE\.mcp\ayga-venv\Scripts\Activate.ps1"

# 3. Обновите pip
python -m pip install --upgrade pip setuptools wheel

# 4. Установите ayga-mcp-client
pip install ayga-mcp-client>=1.4.1
```

## 📋 Конфигурация Claude Desktop

После успешной установки конфигурируйте Claude Desktop:

### Windows

1. Откройте `%APPDATA%\Claude\claude_desktop_config.json`

2. Добавьте конфигурацию:

```json
{
  "mcpServers": {
    "ayga": {
      "command": "C:\\Users\\ozand\\.mcp\\ayga-venv\\Scripts\\python.exe",
      "args": ["-m", "ayga_mcp_client"],
      "env": {
        "REDIS_API_KEY": "YOUR_API_KEY_HERE"
      }
    }
  }
}
```

**Важно**: Замените `C:\\Users\\ozand\\.mcp` на ваш путь!

### macOS/Linux

1. Откройте `~/.config/Claude/claude_desktop_config.json`

2. Добавьте конфигурацию:

```json
{
  "mcpServers": {
    "ayga": {
      "command": "python",
      "args": ["-m", "ayga_mcp_client"],
      "env": {
        "REDIS_API_KEY": "YOUR_API_KEY_HERE",
        "PYTHONPATH": "/path/to/.mcp/ayga-venv/lib/python3.11/site-packages"
      }
    }
  }
}
```

## 🔑 Получение API ключа

1. Перейдите на https://redis.ayga.tech
2. Получите API ключ для своего проекта
3. Замените `YOUR_API_KEY_HERE` на реальный ключ в конфигурации

## ✔️ Проверка установки

```powershell
# Активируйте venv
& "$env:USERPROFILE\.mcp\ayga-venv\Scripts\Activate.ps1"

# Проверьте версию
python -c "import ayga_mcp_client; print('✅ Installed')"

# Проверьте доступные парсеры
python -m ayga_mcp_client --help
```

## 📚 Доступные парсеры (40+)

### FreeAI (6)
- Perplexity, ChatGPT, GoogleAI, Kimi, DeepAI, Copilot

### Search Engines (8)
- Google, Yandex, Bing, DuckDuckGo, Baidu, Yahoo, Rambler, You.com

### Social Media (10)
- Instagram (6), TikTok, Telegram, Reddit (3)

### YouTube (6)
- Видеометаданные, поиск, предложения, канальная информация

### Content (3)
- Article Extractor, Text Extractor, **Link Extractor** ⭐

### Translation (4)
- Google, DeepL, Bing, Yandex

### Analytics (1)
- Google Trends

### Visual (1)
- Pinterest Search

### Net (1)
- HTTP Fetcher

## 🐛 Решение проблем

### Проблема: "command not found" или "ModuleNotFoundError"

**Решение**: Убедитесь, что путь к python.exe в конфигурации абсолютный:
```json
"command": "C:\\Users\\<USERNAME>\\.mcp\\ayga-venv\\Scripts\\python.exe"
```

### Проблема: "REDIS_API_KEY not found"

**Решение**: Убедитесь, что:
1. API ключ установлен в `claude_desktop_config.json`
2. Claude Desktop перезагружен после изменения конфигурации

### Проблема: Port already in use (8000)

**Решение**: Другой процесс использует порт. Убедитесь, что redis_wrapper не запущен, или используйте другой порт.

## 📞 Поддержка

- 📧 Email: support@ayga.tech
- 🌐 Сайт: https://redis.ayga.tech
- 📖 Документация: https://github.com/ozand/ayga-mcp-client

## 🔄 Обновление

```powershell
# Активируйте venv
& "$env:USERPROFILE\.mcp\ayga-venv\Scripts\Activate.ps1"

# Обновите пакет
pip install --upgrade ayga-mcp-client

# Проверьте версию
python -c "pip show ayga-mcp-client"
```

## ✨ Использование в Claude Desktop

После конфигурации используйте инструменты в Claude:

```
@ayga search_perplexity query="latest AI trends" timeout=90
@ayga parse_link_extractor query="https://example.com" preset="deep_crawl"
@ayga search_chatgpt query="explain quantum computing"
@ayga parse_article_extractor query="https://news.example.com/article"
```

---

**Версия**: 1.4.1  
**Последнее обновление**: 2026-01-15  
**Python**: 3.11+  
