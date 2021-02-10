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

Скрипт "generate_unconditional_samples.py" генерирует текст на общую тематику

Для того чтобы сгенерировать текст по ключу нужно использовать скрипт "interactive_conditional_samples.py"

Для этого сначала заполняем файл "keywords.csv" - ключевыми словами и категорией WordPress, в которую будет добавлен пост.

И запускаем скрипт, без параметра "nsamples", кол-во текстов будет столько сколько заданий в файле "keywords.csv":

c:\Python37\python src/interactive_conditional_samples.py

Также в файле "keywords.csv" можно указать title будущего поста, но если не указать, то title сгенерируется из первых 60 символов поста

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

Пример сайта на WordPress:

https://nevep.ru/tmp/gptwp/

# Пример команд для запуска GPT-2 на Google Colab GPU

Один раз выполнить:

from google.colab import drive

drive.mount('/content/drive') 

%cd /content/drive/My\ Drive/

!mkdir gpt-2

%cd gpt-2/

!git clone https://github.com/nevstas/gpt-2.git

%cd /content/drive/My\ Drive/gpt-2/gpt-2

%tensorflow_version 1.x

!pip3 install -r requirements.txt

!python3 download_model.py 124M

!python3 download_model.py 355M

!python3 download_model.py 774M

!python3 download_model.py 1558M

Выполнить каждый раз при старте/перезапуске:

from google.colab import drive

drive.mount('/content/drive') 

%cd /content/drive/My\ Drive/gpt-2/gpt-2

%tensorflow_version 1.x

!pip3 install -r requirements.txt

Далее можно запускать скрипты, этими командами:

!python3 src/generate_unconditional_samples.py

!python3 src/generate_unconditional_samples.py --model_name '1558M'

!python3 src/interactive_conditional_samples.py

!python3 src/interactive_conditional_samples.py --model_name '1558M'

!python3 src/export_to_csv.py

Время генерации текста на Бесплатном Google Colab GPU: 124M - 11 сек, 1558M - 50 сек

Время генерации текста на Бесплатном Google Colab TPU: 124M - 1 мин 50 сек, 1558M - не замерял

Если медленно выполняет, значит нет GPU: попробуйте изменить Runtime Type на GPU в меню Runtime → Change Runtime Type (Среда выполнения -> Сменить среду выполнения)

На данный момент есть два варианта генерации:

1) Генерация текстов общей тематики ("generate_unconditional_samples.py"). Title задавать нельзя, он генерируется из первых 60 символов поста.

Примеры постов первого варианта:

https://nevep.ru/tmp/gptwp/category/uncategorized/

2) Генерация по ключу ("interactive_conditional_samples.py"). На входе в скрипт поступает файл "keywords.csv" он выглядит вот так

https://nevep.ru/screenshots/2021-02-06_18.22.24_stqmczh5to.png

В первой колонке задается ключ по которому GPT-2 генерирует статью, часто бывает что ключ и получившаяся статья имеют мало чего общего. 

Вторая колонка это категория в WordPress. 

Третья колонка это title - его можно задавать, но можно и не задавать, тогда он сгенерируется из первых 60 символов поста. Сколько строк в cvs файле столько текстов и генерится.

Примеры постов второго варианта:

https://nevep.ru/tmp/gptwp/category/car/

https://nevep.ru/tmp/gptwp/category/music/

UP: Добавлены переводы. Для того чтобы включить/выключить перевод нужно в файле "export_to_csv.py" задать True или False параметру is_translate. И если перевод включен задать язык в параметре translate_lang