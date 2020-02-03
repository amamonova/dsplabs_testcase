# DSP Labs test case

Telegram bot which saves voice messages and photos with face(s) to a
disk. Also a database `bot.db` is created for storing paths to saved 
files.

## Description
The main functionality is developed in `bot.py`. First of all, the
database is created with two tables: `voice`, `photo`. These tables
contain paths to saved files in local disk breakdown by users: 

uid| file_path
--- | --- 
user_1 | path_to_file 

For converting audio to wav use [ffmpeg](https://www.ffmpeg.org). 
For face recognition - 
[face_recognition](https://github.com/ageitgey/face_recognition).


## Getting Started

For starting this bot in your local machine you'll need to 
[register your Bot](https://core.telegram.org/bots#6-botfather) 
in Telegram and insert an authorization token to `config.py`.

## Installing

Clone this repo:
```shell script
git clone https://github.com/amamonova/dsplabs_testcase.git
```

Install all requirements from `requirements.txt`:
```shell script
pip install -r requirements.txt
```

Install `ffmpeg`:
```shell script
brew install ffmpeg
```

Edit the `config.py`. 

Run the bot:
```shell script
python bot.py
```

