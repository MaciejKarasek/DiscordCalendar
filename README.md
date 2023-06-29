<h1 align=center> Discord Calendar </h1>
<h3 align=center> Discord bot that you can use as calendar created with python and SQL database </h3>

<p align="center">
<img src=https://img.shields.io/github/last-commit/MaciejKarasek/DiscordCalendar>
</p>

## How to run
### Create new Discord app:
* Go on [this](https://discord.com/developers/applications) site and create new app,
* Go to OAuth2 tab select Authorization method as `In-app Authorization`, Scopes and Bot Permissions set like on the screenshot below:
<p align="center">
<img src=https://i.imgur.com/3MBuKIA.png>
</p>

* Now go to URL Generator tab and select same as before, then copy the URL. You will use this URL to invite this bot on your server, so save it somewhere.
* Then go to Bot tab and select `PRESENCE INTENT`, `SERVER MEMBERS INTENT` and `MESSAGE CONTENT INTENT`
* After that, in the same tab click Reset Token button and copy new generated token.<br />
<b>WARNING: REMEMBER TO DO NOT SHARE THIS TOKEN</b>
* Create `config.json` file that will contain your bot token:
  ```json
  {
    "token": "your_bot_token"
  }
  ```

### Clone the repository:
```bash
$ git clone https://github.com/MaciejKarasek/DiscordCalendar.git
```
* Put your `config.json` file into `.../DiscordCalendar/` directory 

### Install Python 3.11:
Linux:
```bash
$ sudo apt-get install python3.11
```

Windows:
Download Python from [official Python site](https://www.python.org/downloads/windows/).

### Install Python libaries:
Go to .../DiscordCalendar directory and run this command:
```bash
.../DiscordCalendar$ pip install -r requirements.txt
```

### Run the bot:
```bash
.../DiscordCalendar$ python3 main.py
```

## Commands:
`-help` - Shows you all comands and their usage
#### Add task:
```
<-add / -a> <Task info> <arguments>
```
Arguments:\
`-td` - Adds TODO status to your task<br />
`-time` - Adds deadline to your task, by default its tommorrow, but You can change this by adding date in format `YYYY.MM.DD`<br />
Example: `-a "Task one" -td -time 2023.3.1` - Creates task with info "Task one", TODO status and deadline 2023.03.01.

#### Show tasks:
```
-show
```
Arguments:\
`-s` - shows all tasks in compact version.

#### Change status:
```
-status <scope> <TODO / InProg / DONE / None>
```
Scope:\
Use `Task_ID` of exact task or `all` to change status of all tasks\
Arguments:\
`TODO` - TODO ⭕️\
`InProg` - In Progress ⏳\
`DONE` - DONE ✅\
`None` -  No status

#### Remove tasks:
```
<-remove / -r> <scope>
```
o
Scope:\
`Task_ID` - remove specific task,\
`all` or `-a` to remove your all tasks,\
`done` or `-d` to remove all your DONE tasks,\
`old` or `-o` to remove all your out of date tasks\

#### Private tasks:
To create, show, change status and remove private tasks use double prefix `--`\
Example: `--help` - Sends you private message with bot instructions'