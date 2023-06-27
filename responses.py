from datetime import date, timedelta
import sqlite3
from database import insertValues


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
        date = 'None'
        endmsg = 0
        time = (0, date)
        for i, word in enumerate(split_msg[1:]):
            if i == 0:
                tsk_msg = tsk_msg + word
            if word[0] != '-' and endmsg == 0:
                tsk_msg = tsk_msg + ' ' + word
            else:
                endmsg = 1
                if word == '-td':
                    todo_status = 'TODO'
                if word == '-time':
                    print(split_msg[i+2])
                    if split_msg[i+2] and split_msg[i+2][0] != '-':
                        date_list = split_msg[i+1].split('.')
                        date_list = [eval(j) for j in date_list]
                        dt = date(date_list[0], date_list[1], date_list[2])
                        time = (1, dt)
                    else:
                        dt = date.today() + timedelta(days=1)
                        time = (1, dt)
        insertValues(message, tsk_msg, todo_status, time, is_private)
        return 0xffc200, 'SUCCCESS', 'NEW TASK ADDED CORRECTLY'

    # When there is no command like provided
    else:
        return 0xFF0000, 'Error', 'wrong command, use -help for help'
