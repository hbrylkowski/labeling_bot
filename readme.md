## labeling telegram bot

This application is build to render and print labels sent to it via telegram, as well
as provide info about printer status and other useful information.


## Supported commands
- `/media_info` - show info about currently installed media
- `/simple_label` - print a simple label

### usage example
You need to things:
1. A telegram bot token, you can write to [@BotFather](https://t.me/BotFather) to get one
2. A compatible printer
3. docker installed on your system

```yaml
version: "3.8"
services:
  bot:
    build:
      context: .
      dockerfile: Dockerfile
    environment:
      - PRINTER_IP=<printer_ip>
      - TELEGRAM_TOKEN=<telegram_bot_token>
    command:
      - python
      - labeler/adapter/telegram_bot.py

```

### Supported printers
- Brother PT-E550W