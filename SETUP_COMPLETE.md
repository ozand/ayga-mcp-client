# ✅ ayga-mcp-client: Установка и конфигурация решена!

## 🎯 Что было проблемой

При установке в глобальную среду Python возникал конфликт версий:
```
fastapi 0.115.0 требует starlette<0.39.0
mcp>=1.0.0 требует starlette>=0.51.0
```

## ✅ Решение: Virtual Environment

Создан **отдельный virtual environment** для `ayga-mcp-client` с чистыми зависимостями.

### Скрипт установки уже запущен! ✔️

```
✅ Virtual environment создан: C:\Users\ozand\.mcp\ayga-venv
✅ ayga-mcp-client 1.4.1 установлен
✅ Все зависимости установлены без конфликтов
✅ Установка протестирована успешно
```

## 📋 СЛЕДУЮЩИЕ ШАГИ

### 1️⃣ Для Claude Desktop

**Откройте файл конфигурации:**
```
%APPDATA%\Claude\claude_desktop_config.json
```

**Замените содержимое на:**
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

*Или скопируйте готовый файл:*
```powershell
Copy-Item .\claude_desktop_config.json.example `
  "$env:APPDATA\Claude\claude_desktop_config.json"
```

### 2️⃣ Для VS Code Copilot

**Откройте файл конфигурации:**
```
%APPDATA%\Code\User\mcp.json
```

**Добавьте конфигурацию:**
```json
{
  "servers": {
    "ayga": {
      "type": "stdio",
      "command": "C:\\Users\\ozand\\.mcp\\ayga-venv\\Scripts\\python.exe",
      "args": ["-m", "ayga_mcp_client"],
      "env": {
        "REDIS_API_KEY": "YOUR_API_KEY_HERE"
      }
    }
  }
}
```

*Или скопируйте готовый файл:*
```powershell
Copy-Item .\vscode_mcp_config.json.example `
  "$env:APPDATA\Code\User\mcp.json"
```

### 3️⃣ Получить API ключ

1. Перейдите на: **https://redis.ayga.tech**
2. Получите API ключ для вашего проекта
3. Замените `YOUR_API_KEY_HERE` на реальный ключ

### 4️⃣ Перезагрузить Claude Desktop / VS Code

После редактирования конфигурационных файлов:
- Закройте Claude Desktop полностью
- Откройте снова
- Проверьте, что `ayga` инструменты доступны

## ✔️ Проверка установки

```powershell
# Активируйте virtual environment
& "C:\Users\ozand\.mcp\ayga-venv\Scripts\Activate.ps1"

# Проверьте версию
python -c "import ayga_mcp_client; print('✅ ayga-mcp-client установлен')"

# Посмотрите доступные парсеры
python -m ayga_mcp_client --help
```

## 📚 Доступные инструменты (40+ парсеров)

### Примеры использования в Claude Desktop

```
@ayga list_parsers
Список всех доступных парсеров

@ayga search_perplexity query="latest AI trends" timeout=90
AI-powered поиск с источниками

@ayga parse_link_extractor query="https://example.com" preset="deep_crawl"
Извлечение ссылок с сайта (многоуровневое сканирование)

@ayga search_chatgpt query="explain quantum computing"
ChatGPT с веб-поиском

@ayga parse_article_extractor query="https://news.example.com"
Извлечение статей с Mozilla Readability

@ayga translate_google_translate query="Hello world" from_language="en" to_language="ru"
Перевод

@ayga get_google_trends query="artificial intelligence" timeout=90
Google Trends анализ
```

## 🔧 Структура установки

```
C:\Users\ozand\.mcp\ayga-venv\
├── Scripts/
│   ├── python.exe          ← Используется в конфигурации
│   ├── pip.exe
│   └── activate.ps1
├── Lib/
│   └── site-packages/
│       ├── ayga_mcp_client/    ← Наш пакет (1.4.1)
│       └── mcp/                 ← MCP SDK (1.25.0)
└── pyvenv.cfg
```

## 🆘 Решение проблем

### Проблема: "Команда не найдена" (command not found)

**Проверьте:**
1. Путь к python.exe в конфигурации абсолютный
2. Virtual environment существует: `C:\Users\ozand\.mcp\ayga-venv\`
3. Файл существует: `C:\Users\ozand\.mcp\ayga-venv\Scripts\python.exe`

### Проблема: "API ключ не установлен"

**Решение:**
1. Получите ключ на https://redis.ayga.tech
2. Замените `YOUR_API_KEY_HERE` в конфигурации на реальный ключ
3. Сохраните файл
4. Перезагрузите Claude Desktop

### Проблема: "Module not found"

**Решение:**
```powershell
# Активируйте venv и переустановите
& "C:\Users\ozand\.mcp\ayga-venv\Scripts\Activate.ps1"
pip install --upgrade ayga-mcp-client
```

## 🔄 Обновление

```powershell
# Активируйте venv
& "C:\Users\ozand\.mcp\ayga-venv\Scripts\Activate.ps1"

# Обновите пакет
pip install --upgrade ayga-mcp-client

# Проверьте версию
pip show ayga-mcp-client
```

## 📞 Контакты

- 🌐 **Сайт**: https://redis.ayga.tech
- 📧 **Email**: support@ayga.tech
- 💬 **GitHub**: https://github.com/ozand/ayga-mcp-client

## 📋 Быстрая справка

| Задача              | Команда                                                  |
| ------------------- | -------------------------------------------------------- |
| Активировать venv   | `& "C:\Users\ozand\.mcp\ayga-venv\Scripts\Activate.ps1"` |
| Проверить установку | `python -c "import ayga_mcp_client; print('OK')"`        |
| Обновить пакет      | `pip install --upgrade ayga-mcp-client`                  |
| Посмотреть версию   | `pip show ayga-mcp-client`                               |
| Деактивировать venv | `deactivate`                                             |

---

**Версия**: 1.4.1  
**Установлена**: 2026-01-15  
**Python**: 3.13  
**Статус**: ✅ Готово к использованию  
