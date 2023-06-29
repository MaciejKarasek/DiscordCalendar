from datetime import date, timedelta
import sqlite3
from database import insertValues, getValues, change_status


def handle_response(message, usr_message, is_private) -> str:
    p_message = usr_message.lower()
    split_msg = p_message.split()
    # TODO more commands and functionality
    # Test command
    if split_msg[0] == 'test run':
        return 0xffc200, 'Test', 'test run 1 2 3...'

    # Command that returns usable commands and information about them
    if split_msg[0] == 'help':
        return 0x87ceeb, 'Help:', '`-test run` - runs a test of a bot\n\
                                    Use double prefix for answer \
                                    in private chat `--`\n\
                                    `example: --help` - Sends you private \
                                                message with bot instructions'

    if split_msg[0] == 'add':
        tsk_msg = ""
        todo_status = 'None'
        dt = 'None'
        endmsg = 0
        time = (0, dt)
        for i, word in enumerate(split_msg[1:]):
            if i == 0:
                tsk_msg = tsk_msg + word
            elif word[0] != '-' and endmsg == 0:
                tsk_msg = tsk_msg + ' ' + word
            elif word == '-td':
                endmsg = 1
                todo_status = 'TODO'
            elif word == '-time':
                endmsg = 1
                if len(split_msg[1:]) > i+1 and split_msg[i+2] \
                        and split_msg[i+2][0] != '-':
                    date_list = split_msg[i+2].split('.')
                    date_list = [eval(j) for j in date_list]
                    dt = date(date_list[0], date_list[1], date_list[2])
                    time = (1, dt)
                else:
                    dt = date.today() + timedelta(days=1)
                    time = (1, dt)
        insertValues(message, tsk_msg, todo_status, time, is_private)
        return 0xffc200, 'SUCCESS', 'NEW TASK ADDED CORRECTLY'

    if split_msg[0] == 'show':
        tasks = getValues(message, is_private)
        if tasks == 0:
            return 0xFF0000, 'Error', "You don't have any tasks"
        if len(split_msg) > 1 and split_msg[1][0] == '-':
            if split_msg[1] == '-s':
                return 0xffc200, 'Tasks', simple_ans(tasks)
        else:
            return 0xffc200, 'Tasks', ans(tasks)
    
    if split_msg[0] == 'change':
        try:
            task_ID = int(split_msg[1])
            status = str(split_msg[2])
        except:
            error = '**Correct usage of command:** \
                    `-change <Task-ID> <TODO / InProg / DONE / None>`\
                    \n`TODO` - TODO ⭕️\
                    \n`InProg` - In Progress ⏳\
                    \n`DONE` - DONE ✅\
                    \n`None` -  No status'
            return 0xFF0000, 'Error', error
        x = change_status(task_ID, status, message, is_private)
        return x

    # TODO dodac usuwanie wybranie taskow
    # When there is no command like provided
    else:
        return 0xFF0000, 'Error', 'wrong command, use -help for help'


def simple_ans(tasks):
    emoji = {'TODO': 'TODO ⭕️',
             'InProgress': 'In Progress ⏳',
             'DONE': 'DONE ✅'}
    sep = '-' * 70
    sep = sep + '\n'
    answ = sep
    for task in tasks:
        line = "ID: `{}` Task: `{}`".format(task[0], task[1])
        if task[2] != 'None':
            line = line + " Status: `{}`".format(emoji[task[2]])
        if task[3] != 0:
            line = line + " Deadline: `{}`".format(task[3])
        answ = answ + line + '\n' + sep
    return answ


def ans(tasks):
    emoji = {'TODO': 'TODO ⭕️',
             'InProgress': 'In Progress ⏳',
             'DONE': 'DONE ✅'}
    sep = '-' * 70
    answ = sep
    for task in tasks:
        line = "```ID: {}``` ```Task: {}```".format(task[0], task[1])
        if task[2] != 'None':
            line = line + " ```Status: {}```".format(emoji[task[2]])
        if task[3] != 0:
            line = line + " ```Deadline: {}```".format(task[3])
        answ = answ + line + sep
    return answ
