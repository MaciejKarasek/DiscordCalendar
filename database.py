import sqlite3


def CreateTables():
    conn = sqlite3.connect('tasks.db')
    db = conn.cursor()

    db.execute('''
               CREATE TABLE IF NOT EXISTS Main
               (
                [ID] INTEGER,
                [User_ID] TEXT NOT NULL,
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
                SELECT * FROM Main WHERE User_ID = ?
                ''', [str(message.author.id)])
    user = db.fetchall()
    if len(user) == 0:
        db.execute('''
                    INSERT INTO Main (User_ID) VALUES (?)
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
