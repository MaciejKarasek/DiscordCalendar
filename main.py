from bot import run_bot
import database

# Runing the bot
if __name__ == '__main__':
    database.CreateTables()
    run_bot()
