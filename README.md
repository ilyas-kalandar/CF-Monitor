# CF-Monitor
A simple script for monitoring user on Codeforces <br>
Простой скрипт, при помощи которого можно мониторить какого-либо пользователя на Codeforces

## How to run ?
### First, we <b>need</b> to install some python packages. <br>

## Как запустить ?
### Для начала необходимо установить несколько python-пакетов.

### Install requests, tabulate, colorama/Установите библиотеки requests, tabulate и colorama
## Windows
<code>pip --user install requests tabulate colorama </code>
## Linux/macOS
<code>pip3 --user install requests tabulate colorama</code>

### Run script/Запуск
## Windows
<code>py main.py</code>
## Linux/macOS
<code>python3 main.py</code>

### How to use ? / Как использовать
After launch, you will immediately receive an invitation to enter a nickname <br>
После запуска, вы сразу увидите приглашение ввести ник пользователя на codeforces <br>
So, enter nickname and press enter <br>
Введите имя и нажмите ENTER <br><br>
<img src='screenshots/1.png'>

After these manipulations, you will notice that the program asks you "whether to monitor a specific day of the user"<br>
После этих манипуляций, вы заметите что программа спрашивает у вас "промониторить ли конкретный день пользователя"<br>
You can say no by Enter no, No, or blablabla or you can say "Yes" by enter "yes", "y", "yeah" and any word which start with 'y'<br>
Вы можете сказать нет напечатав No, no, n или любое другое слово, также вы можете сказать да прописав yes, yeah или любое другое слово начинающееся на 'y'<br>

If you say "yes", you must enter date, you can press enter to keep the default values (datetime.now())<br>
Если вы ответили "yes", то вы должны ввести дату, вы можете просто нажать enter, для пропуска конкретного поля, значение будет дефолтным (то есть сегодня)<br>

<img src='screenshots/2.png'>

## That's all! With Love, Ilyas Kalandar
