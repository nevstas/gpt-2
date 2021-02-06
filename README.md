# Делаем сайт на WordPress из генерируемого контента GPT-2

Скачиваем Python, обязательно версии 3.7.* и обязательно 64 битной разрядности.

Ссылка для Windows:

https://www.python.org/ftp/python/3.7.9/python-3.7.9-amd64.exe

Я выбрал кастомную установку, изменил только путь установки "c:\Python37\", остальные параметры оставил по умолчанию.



Далее нужно установить Microsoft Visual C++ 14.*

По этой ссылке скачиваем "Build Tools для Visual Studio 2019"

https://visualstudio.microsoft.com/ru/downloads/

Для этого раскрываем меню "Инструменты для Visual Studio 2019" и скачиваем "Build Tools для Visual Studio 2019"

Запускаем и выбираем установку "Средства сборки C++"

Перезагружаемся


Скачиваем zip архив по ссылке:
https://github.com/nevstas/gpt-2/archive/master.zip
Распаковываем, у меня например по такому пути "e:\python\gpt-2\"
Открываем командную строку (консоль) и переходим в папку "gpt-2"

c:\Python37\Scripts\pip3 install --upgrade setuptools

Устанавливаем tensorflow. Либо CPU версию, либо GPU версию (у меня CPU версия)
Для CPU версии выполняем команду:
c:\Python37\Scripts\pip3 install tensorflow==1.15
Для GPU версии выполняем команду:
c:\Python37\Scripts\pip3 install tensorflow-gpu==1.15
Для GPU вроде как нужна видеокарта с CUDA, и нужно настроить драйвер. Я GPU версию не устанавливал.

c:\Python37\Scripts\pip3 install -r requirements.txt

Загружаем модели
c:\Python37\python download_model.py 124M
c:\Python37\python download_model.py 355M
c:\Python37\python download_model.py 774M
c:\Python37\python download_model.py 1558M

По умолчанию используется модель 124M
Можно пытаться запускать генерацию командой:
c:\Python37\python src/generate_unconditional_samples.py
Ждем пару минут, в папке "result" должен появиться файл "result1.txt"

Можно запустить генерацию нескольких текстов за раз, передав в параметре "nsamples" количество, например 5:
c:\Python37\python src/generate_unconditional_samples.py --nsamples 5

Можно указать другую модель в параметре "model_name":
c:\Python37\python src/generate_unconditional_samples.py --nsamples 5 --model_name '1558M'

Примеры текстов 124M:
https://nevep.ru/tmp/gpt/result1.html
https://nevep.ru/tmp/gpt/result2.html

Примеры текстов 1558M:
https://nevep.ru/tmp/gpt/result-1558M-1.html
https://nevep.ru/tmp/gpt/result-1558M-2.html

Время генерации текста на CPU: 124M - 3 минуты, 1558M - 30 минут

Делаем экспорт постов в CSV для дальнейшей загрузки в WordPress:
c:\Python37\python src/export_to_csv.py
После запуска должен появиться файл export.csv

Устанавливаем в WordPress плагин "WP All Import" и импортируем файл export.csv