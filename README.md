# это сайт по дыле

сначала нужно установить все зависимости командой
```terminal
pip install -r requirements.txt
```

## далее настроить бд ##
все команды в файле [creatingDB.txt](https://github.com/whtslv7837/musicstore/blob/master/creatingDB.txt)

чтобы открыть сайт нужно запустить его на локальном сервере, все действия в джанго производятся через файл manage.py
в консоли переходим в директорию с фалом manage.py или пкм по папке и open in > terminal

## далее используем команду ##
для линукса и мака:
```terminal
python3 manage.py runserver
```
для винды:
```terminal
python manage.py runserver
```

далее в браузере заходим на [локальный сервер](http://127.0.0.1:8000/)

