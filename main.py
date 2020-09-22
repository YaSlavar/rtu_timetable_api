import uvicorn
from typing import Optional
from fastapi import FastAPI
from threading import Thread
import schedule
import time


class ScheduleUpdater(Thread):

    def __init__(self):
        """Инициализация потока"""
        Thread.__init__(self)
        self.name = "Обновление расписания"

    def run(self):
        """Запуск потока Обновления расписания"""

        def schedule_update():
            pass

        schedule.every().day.at("10:30").do(schedule_update)

        while True:
            schedule.run_pending()
            time.sleep(1)





api = FastAPI()

@api.get("/")
def read_root():
    return {"Hello": "World"}


@api.get("/items/{item_id}")
def read_item(item_id: int, q: Optional[str] = None):
    return {"item_id": item_id, "q": q}


if __name__ == "__main__":
    my_thread = ScheduleUpdater()
    my_thread.start()
    uvicorn.run("main:api", host="127.0.0.1", port=5000, log_level="debug")