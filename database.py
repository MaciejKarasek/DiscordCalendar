from datetime import datetime
import sqlite3


def CreateTables():
    conn = sqlite3.connect('tasks.db')
    db = conn.cursor()

    db.execute('''
               CREATE TABLE IF NOT EXISTS Main
               (
                [ID] INTEGER,
                [User_ID] TEXT NOT NULL UNIQUE,
                PRIMARY KEY(ID)
               )
               ''')

    db.execute('''
               CREATE TABLE IF NOT EXISTS Tsk
               (
                [Task_ID] INTEGER NOT NULL PRIMARY KEY,
                [User_ID] INTEGER,
                [Channel_ID] TEXT NOT NULL,
                [isPrivate] INTEGER,
                FOREIGN KEY(User_ID) REFERENCES Main(ID)
               )
               ''')

    db.execute('''
               CREATE TABLE IF NOT EXISTS Msg
               (
                [Task_ID] INTEGER NOT NULL,
                [Message] TEXT,
                [TD] TEXT,
                [Deadline] INTEGER,
                FOREIGN KEY(Task_ID) REFERENCES Tsk(Task_ID)
               )
               ''')

    db.execute('''
               CREATE TABLE IF NOT EXISTS Time
               (
                [Task_ID] INTEGER NOT NULL,
                [Date] TEXT,
                [TimeZone] TEXT DEFAULT "GMT+2",
                FOREIGN KEY(Task_ID) REFERENCES Tsk(Task_ID)
               )
               ''')

    conn.commit()


def insertValues(message, taskmsg, todo, time, isprivate):
    conn = sqlite3.connect('tasks.db')
    db = conn.cursor()

    db.execute('''
                INSERT  OR IGNORE
                INTO Main (User_ID) VALUES (?)
        ''', [str(message.author.id)])
    db.execute('''
                SELECT ID FROM Main WHERE User_ID = ?
                ''', [str(message.author.id)])
    usrid = db.fetchall()[0][0]
    prv = 0
    if isprivate:
        prv = 1
    db.execute('''
                INSERT INTO Tsk (User_ID, Channel_ID, isPrivate)
                VALUES (?,?,?)
                ''', [usrid, str(message.channel.id), prv])
    tskid = int(db.lastrowid)
    db.execute('''
                INSERT INTO Msg (Task_ID, Message, TD, Deadline)
                VALUES (?, ?, ?, ?)
                ''', [tskid, taskmsg, todo, time[0]])
    if time[0] == 1:
        db.execute('''
                INSERT INTO Time (Task_ID, Date)
                VALUES (?, ?)
                ''', [tskid, time[1]])
    conn.commit()


def getValues(message, prv):
    authorID = str(message.author.id)

    conn = sqlite3.connect('tasks.db')
    db = conn.cursor()

    try:
        db.execute('''
                    SELECT ID FROM Main WHERE User_ID = ?
                    ''', [authorID])
        usrID = db.fetchall()[0][0]
    except ValueError:
        conn.commit()
        return 0
    if not prv:
        db.execute('''
                    SELECT Task_ID FROM Tsk WHERE User_ID = ?
                    AND isPrivate = ?
                    ''', [usrID, prv])
        tskID = db.fetchall()
    else:
        db.execute('''
                    SELECT Task_ID FROM Tsk WHERE User_ID = ?
                    ''', [usrID])
        tskID = db.fetchall()
    tskID = [i[0] for i in tskID]
    tskSummary = [[0] * 4 for i in range(len(tskID))]
    for i, id in enumerate(tskID):
        db.execute('''
                    SELECT Message, TD, Deadline FROM Msg
                    WHERE Task_ID = ?
                    ''', [id])
        tskInfo = db.fetchall()[0]
        tskSummary[i][0] = id
        tskSummary[i][1] = tskInfo[0]
        tskSummary[i][2] = tskInfo[1]
        if tskInfo[2] == 1:
            db.execute('''
                    SELECT Date FROM Time
                    WHERE Task_ID = ?
                    ''', [id])
            tskDate = db.fetchall()[0][0]
            tskSummary[i][3] = tskDate
        else:
            tskSummary[i][3] = 0
    conn.commit()
    return tskSummary


def change_status(id, status, message, isPrivate):
    authorID = str(message.author.id)
    emoji = {'todo': 'TODO ⭕️',
             'inprog': 'In Progress ⏳',
             'done': 'DONE ✅',
             'none': 'None'}
    index = {'todo': 'TODO',
             'inprog': 'InProgress',
             'done': 'DONE',
             'none': 'None'}
    try:
        emoji_status = emoji[status]
        index_status = index[status]
    except KeyError:
        error = '**Wrong status, use one of those:** \
                    \n`TODO` - TODO ⭕️\
                    \n`InProg` - In Progress ⏳\
                    \n`DONE` - DONE ✅\
                    \n`None` -  No status'
        return 0xFF0000, 'Error', error
    conn = sqlite3.connect('tasks.db')
    db = conn.cursor()

    try:
        db.execute('''
                    SELECT ID FROM Main WHERE User_ID = ?
                    ''', [authorID])
        usrID = db.fetchall()[0][0]
    except KeyError:
        conn.commit()
        return 0xFF0000, 'Error', "You don't have any tasks"

    if id != 'all':
        if isPrivate:
            db.execute('''
                        SELECT * FROM Tsk WHERE
                        User_ID = ? AND
                        Task_ID = ?
                        ''', [usrID, id])
        else:
            db.execute('''
                        SELECT * FROM Tsk WHERE
                        User_ID = ? AND
                        Task_ID = ? AND
                        IsPrivate = ?
                        ''', [usrID, id, isPrivate])
        tsk = db.fetchall()
    else:
        if isPrivate:
            db.execute('''
                        SELECT Task_ID FROM Tsk WHERE
                        User_ID = ?
                        ''', [usrID])
        else:
            db.execute('''
                    SELECT Task_ID FROM Tsk WHERE
                    User_ID = ? AND
                    IsPrivate = ?
                    ''', [usrID, isPrivate])
        tsk = db.fetchall()
    tsk = [i[0] for i in tsk]
    if len(tsk) == 0:
        return 0xFF0000, 'Error', "You don't have task with id: `{}`\
                        \nIf your task is private, use:\
                        \n`--status {} {}`\
                        \nOr ensure that id You\
                        provided is correct".format(id, id, status)

    for tsk_ID in tsk:
        db.execute('''
                    UPDATE Msg SET TD = ?
                    WHERE Task_ID = ?
                    ''', [index_status, tsk_ID])

    conn.commit()
    if id == 'all':
        return 0xffc200, 'SUCCESS',\
            'Status of all tasks was changed\
            correctly to `{}`'.format(emoji_status)
    return 0xffc200, 'SUCCESS',\
        'Status of task `{}` was\
        changed correctly to `{}`'.format(id, emoji_status)


def remove_task(scope, message, isPrivate):
    authorID = str(message.author.id)
    error_notask = "You don't have task like that\
                    \nIf your task is private, use:\
                    \n`--remove <arg>`\
                    \nOr ensure that id You\
                    provided is correct\n\
                    Type `-help` for more info"

    conn = sqlite3.connect('tasks.db')
    db = conn.cursor()

    try:
        db.execute('''
                    SELECT ID FROM Main WHERE User_ID = ?
                    ''', [authorID])
        usrID = db.fetchall()[0][0]
    except KeyError:
        conn.commit()
        return 0xFF0000, 'Error', "You don't have any tasks"
    if isinstance(scope, int):
        if isPrivate:
            db.execute('''
                        SELECT Task_ID FROM Tsk WHERE
                        User_ID = ? AND
                        Task_ID = ?
                        ''', [usrID, scope])
        else:
            db.execute('''
                        SELECT Task_ID FROM Tsk WHERE
                        User_ID = ? AND
                        Task_ID = ? AND
                        IsPrivate = ?
                        ''', [usrID, scope, isPrivate])
        tsk = db.fetchall()

    else:
        if isPrivate:
            db.execute('''
                        SELECT Task_ID FROM Tsk WHERE
                        User_ID = ?
                        ''', [usrID])
        else:
            db.execute('''
                    SELECT Task_ID FROM Tsk WHERE
                    User_ID = ? AND
                    IsPrivate = ?
                    ''', [usrID, isPrivate])
        tsk = db.fetchall()

    tsk = [i[0] for i in tsk]

    if len(tsk) == 0:
        return 0xFF0000, 'Error', error_notask

    if scope == 'done':
        for tsk_ID in tsk:
            db.execute('''
                        SELECT Task_ID FROM Msg WHERE
                        Task_ID = ? AND
                        TD = 'DONE'
                        ''', [tsk_ID])
            id = db.fetchall()
            if len(id) != 0:
                rm_data(tsk_ID)
        conn.commit()
        return 0xffc200, 'SUCCCESS', 'All your DONE tasks has been removed'

    elif scope == 'old':
        for tsk_ID in tsk:
            db.execute('''
                        SELECT Task_ID FROM Msg WHERE
                        Task_ID = ? AND
                        Deadline = 1
                        ''', [tsk_ID])
            id = db.fetchall()
            if len(id) == 0:
                continue
            db.execute('''
                        SELECT Date FROM Time WHERE
                        Task_ID = ?
                        ''', [tsk_ID])
            dt = db.fetchall()[0][0]
            if datetime.strptime(dt, '%Y-%m-%d') < datetime.today():
                rm_data(tsk_ID)
        conn.commit()
        ans = 'All your out of date tasks has been removed'
        return 0xffc200, 'SUCCESS', ans
    for tsk_ID in tsk:
        rm_data(tsk_ID)
    conn.commit()
    all_ans = 'All your tasks has been removed'
    id_ans = 'Your task with id:`{}` has been removed'.format(scope)
    if scope == 'all':
        return 0xffc200, 'SUCCESS', all_ans
    else:
        return 0xffc200, 'SUCCESS', id_ans


def rm_data(task_id):
    conn = sqlite3.connect('tasks.db')
    db = conn.cursor()

    db.execute('''
                DELETE FROM Time WHERE
                Task_ID = ?
                ''', [task_id])
    db.execute('''
                DELETE FROM Msg WHERE
                Task_ID = ?
                ''', [task_id])
    db.execute('''
                DELETE FROM Tsk WHERE
                Task_ID = ?
                ''', [task_id])
    conn.commit()
