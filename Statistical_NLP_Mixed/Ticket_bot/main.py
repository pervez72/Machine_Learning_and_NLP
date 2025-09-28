import asyncio
import schedule
import time
from bot import run_bot

# সকাল ৮টায় বট চলবে
schedule.every().day.at("08:00").do(lambda: asyncio.run(run_bot()))

while True:
    schedule.run_pending()
    time.sleep(1)
