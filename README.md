# ___WB Work Bot___ 

<font size = 2><i> Developed by [Malakhov Stas](https://github.com/MalakhovStas) in June 2022</i></font>

___
Телеграм бот для работы с API сайта Wildberries.
___
<a id="ceiling"></a>

### __Установка приложения:__

1. Для установки бота на свой компьютер или сервер клонируйте этот репозиторий командой: 
   <i><span style="color:  #228B22;"> git clone ссылка на репозиторий </span><i>

2. Установите зависимости из файла [requirements.txt](requirements.txt) командой: 
   <i><span style="color:  #228B22;"> pip install -r requirements.txt </span></i>

3. Создайте бота при помощи [BotFather](https://telegram.me/BotFather), полученный токен необходимо указать 
   в переменной [<span style="color:  #228B22;">BOT_TOKEN</span>](.env.template) файла [.env.template](.env.template) 
   вместо текста в кавычках (кавычки оставить).

4. Переменная [<span style="color:  #228B22;">ADMINS</span>](.env.template) в файле [.env.template](.env.template) - это список 
   id пользователей Telegram, которым будут предоставлены права администраторов вашего бота. Чтобы узнать id, необходимо 
   зайти в поисковую строку приложения Telegram и ввести <i><span style="color:  #228B22;">@getmyid_bot</span></i>, 
   активировать первого бота в списке, в ответ он пришлет уникальный id пользователя. Можно не указывать, либо указать 
   позднее, удалив текст и оставив пустые кавычки. 

5. Обязательно необходимо переименовать файл [.env.template](.env.template) в <i><span style="color:  #228B22;">.env
   </span></i> На этом установка завершена, запускайте файл [main.py](main.py) и пользуйтесь вашим приложением.

### __Настройка бота:__

- [config.py](config_data/config.py) - пользовательские настройки, с описанием. 

- [bot_messages](config_data/bot_messages.py) - словарь сообщений для удобства редактирования текста сообщений от бота пользователю 