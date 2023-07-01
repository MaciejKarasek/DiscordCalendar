from datetime import datetime, timedelta
from database import insertValues, getValues, change_status, remove_task


def handle_response(message, usr_message, is_private) -> str:
    split_msg = usr_message.split()
    split_msg[0] = split_msg[0].lower()
    # TODO more commands and functionality
    # Test command
    if split_msg[0] == 'test run':
        return 0xffc200, 'Test', 'test run 1 2 3...'

    # Command that returns usable commands and information about them
    if split_msg[0] == 'help':
        s = '**ADD TASK**\n\
            ```-add <Task info> <arguments>```\
                Arguments:\n\
                `-td` - Adds TODO status to your task\
                `\n-time` - Adds deadline to your task,\
                By default its tommorrow,\
                but You can change this by adding\
                date in format YYYY.MM.DD or DD.MM.YYYY\n\
                example: `-add "Task one" -td -time 2023.3.1` - Creates\
                task with info "Task one",\
                TODO status and deadline 2023.03.01\
                \n\n**SHOW TASKS**\
                ```-show```\
                Arguments:\n\
                `-s` - shows all tasks in compact version\
                \n\n**CHANGE STATUS**\
                ```-status <scope> <TODO / InProg / DONE / None>```\
                Scope:\
                \nUse `Task_ID` of exact task or `all`\
                to change status of all tasks\
                \nArguments:\
                \n`TODO` - TODO ⭕️\
                \n`InProg` - In Progress ⏳\
                \n`DONE` - DONE ✅\
                \n`None` -  No status\
                \n\n**REMOVE TASKS**\
                ```-remove <scope>```\
                Scope:\
                \n`Task_ID` - remove specific task,\
                \n`all` or `-a` to remove your all tasks,\
                \n`done` or `-d` to remove all\
                your DONE tasks,\
                \n`old` or `-o` to remove all your\
                out of date tasks\
                \n\n**PRIVATE TASKS**\
                \nTo create, show, change status\
                and remove private tasks\
                use double prefix `--`\
                \nExample: `--help` - Sends you private \
                message with bot instructions'
        return 0x87ceeb, '**Commands:**', s

    if split_msg[0] == 'add' or split_msg[0] == 'a':
        args = ['-time', '-td', '-todo']
        tsk_msg = ''
        todo_status = 'None'
        dt = 'None'
        endmsg = 0
        time = (0, dt)
        for i, word in enumerate(split_msg[1:]):
            lower_word = word.lower()
            if i == 0 and lower_word not in args:
                tsk_msg = tsk_msg + word
            elif lower_word not in args and endmsg == 0:
                tsk_msg = tsk_msg + ' ' + word
            elif lower_word == '-td' or lower_word == '-todo':
                endmsg = 1
                todo_status = 'TODO'
            elif lower_word == '-time':
                endmsg = 1
                if len(split_msg[1:]) > i+1 and split_msg[i+2] \
                        and split_msg[i+2][0] != '-':
                    try:
                        date_list = split_msg[i+2].split('.')
                        if len(date_list[0]) == 4:
                            date_format = '%Y.%m.%d'
                        elif len(date_list[2]) == 4:
                            date_format = '%d.%m.%Y'
                        else:
                            raise ValueError('Wrong date format')
                        dt = datetime.strptime(split_msg[i+2], date_format)
                        dt = dt.replace(second=0, microsecond=0)
                        time = (1, dt)
                    except ValueError:
                        return 0xff0000, 'Error', 'Wrong date format, \
                            correct date should look like this: `YYYY.MM.DD`\
                            / `DD.MM.YYYY`'
                else:
                    dt = datetime.today() + timedelta(days=1)
                    dt = dt.replace(second=0, microsecond=0)
                    time = (1, dt)
        insertValues(message, tsk_msg, todo_status, time, is_private)
        return 0xffc200, 'SUCCESS', 'NEW TASK ADDED CORRECTLY'

    if split_msg[0] == 'show':
        tasks = getValues(message, is_private)
        if tasks == 0:
            return 0xFF0000, 'Error', "You don't have any tasks"
        if len(split_msg) > 1 and split_msg[1][0] == '-':
            if split_msg[1].lower() == '-s':
                return 0xffc200, 'Tasks', simple_ans(tasks)
            else:
                errmsg = 'Wrong command argument, use `-show -s` to show\
                        tasks in compact version'
                return 0xff0000, 'Error', errmsg
        else:
            return 0xffc200, 'Tasks', ans(tasks)

    if split_msg[0] == 'status':
        try:
            split_msg[1] = split_msg[1].lower()
            split_msg[2] = split_msg[2].lower()
            if split_msg[1].isnumeric():
                task_ID = int(split_msg[1])
                status = str(split_msg[2])
            elif split_msg[1] == 'all' or split_msg[1] == '-a':
                task_ID = 'all'
                status = str(split_msg[2])
            else:
                error = 'Wrong task ID provided, use `<id>` to change\
                        status of specific task,\
                        or use `all` to change status of your all tasks'
                return 0xFF0000, 'Error', error
        except IndexError:
            error = '**Correct usage of command:** \
                    `-status <Task-ID> <TODO / InProg / DONE / None>`\
                    \n`TODO` - TODO ⭕️\
                    \n`InProg` - In Progress ⏳\
                    \n`DONE` - DONE ✅\
                    \n`None` -  No status'
            return 0xFF0000, 'Error', error
        x = change_status(task_ID, status, message, is_private)
        return x

    if split_msg[0] == 'remove' or split_msg[0] == 'r':
        try:
            arg = split_msg[1].lower()
            if arg.isnumeric():
                scope = int(arg)
            elif arg == 'all' or arg == '-a':
                scope = 'all'
            elif arg == 'done' or arg == '-d':
                scope = 'done'
            elif arg == '-o' or arg == 'old':
                scope = 'old'
            else:
                error = 'Wrong task ID provided, use `<id>` to remove\
                        specific task,\n\
                        Use `all` or `-a` to remove your all tasks,\n\
                        Use `done` or `-d` to remove all your DONE tasks,\n\
                        Use `old` or `-o` to remove all your out of date tasks'
                return 0xFF0000, 'Error', error
        except IndexError:
            error = '**Correct usage of command:** \
                    `-remove <Task-ID / all / done / old>`\
                    \n`all` - Removes all your tasks\
                    \n`done` - Removes all your DONE tasks\
                    \n`old` - Removes all your out of date tasks'
            return 0xFF0000, 'Error', error

        x = remove_task(scope, message, is_private)
        return x
    # When there is no command like provided
    else:
        return 0xFF0000, 'Error', 'wrong command, use -help for help'


def simple_ans(tasks):
    emoji = {'TODO': 'TODO ⭕️',
             'InProgress': 'In Progress ⏳',
             'DONE': 'DONE ✅'}
    sep = '━' * 7
    sep = '▶' + sep + '━ ━ ━  ━  ━  ━   ━    ━' + '\n'
    answ = sep
    for task in tasks:
        line = 'ID: `{}` Task: `{}`'.format(task[0], task[1])
        if task[2] != 'None':
            line = line + ' Status: `{}`'.format(emoji[task[2]])
        if task[3] != 0:
            line = line + ' Deadline: `{}`'.format(task[3])
        answ = answ + line + '\n' + sep
    return answ


def ans(tasks):
    emoji = {'TODO': 'TODO ⭕️',
             'InProgress': 'In Progress ⏳',
             'DONE': 'DONE ✅'}
    sep = '━' * 7
    sep = '▶' + sep + '━ ━ ━  ━  ━  ━   ━    ━'
    answ = sep
    for task in tasks:
        line = '```ID: {}``` ```Task: {}```'.format(task[0], task[1])
        if task[2] != 'None':
            line = line + ' ```Status: {}```'.format(emoji[task[2]])
        if task[3] != 0:
            line = line + ' ```Deadline: {}```'.format(task[3])
        answ = answ + line + sep
    return answ
