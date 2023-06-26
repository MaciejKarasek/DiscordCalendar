import sqlite3

def CreateTables():
    conn = sqlite3.connect('tasks.db')
    db = conn.cursor()

    db.execute('''
               CREATE TABLE IF NOT EXISTS Main
               (
                [ID] int NOT NULL PRIMARY KEY,
                [User_ID] TEXT NOT NULL
               )
               ''')

    db.execute('''
               CREATE TABLE IF NOT EXISTS Tsk
               (
                [Task_ID] INTEGER NOT NULL PRIMARY KEY,
                [User_ID] TEXT,
                FOREIGN KEY(User_ID) REFERENCES Main(ID)
               )
               ''')

    db.execute('''
               CREATE TABLE IF NOT EXISTS Msg
               (
                [Task_ID] INTEGER NOT NULL,
                [Message] TEXT,
                [TD] INTEGER,
                [Deadline] INTEGER,
                FOREIGN KEY(Task_ID) REFERENCES Tsk(Task_ID)
               )
               ''')

    db.execute('''
               CREATE TABLE IF NOT EXISTS Status
               (
                [Task_ID] INTEGER NOT NULL,
                [TODO] TEXT,
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