from config import CONFIG
from fastapi import FastAPI
from fastapi.responses import RedirectResponse, Response
import schedule
from parser_mirea.downloader import Downloader
from parser_mirea.reader import Reader
from timetable_generator import StudentTimetable, TeacherTimetable, ClassroomTimetable
import time
from threading import Thread
import uvicorn

import json


class ScheduleUpdater(Thread):

    def __init__(self, update_time_list=None):
        """Инициализация потока обновления"""
        Thread.__init__(self)

        self.name = "Обновление расписания"
        if update_time_list is None:
            update_time_list = ['01:00']
        self._update_time_list = update_time_list
        self._downloader = Downloader(path_to_error_log='logs/downloadErrorLog.csv', base_file_dir='xls/')
        self._reader = Reader(path_to_new_db="timetable.db")

    def run(self):
        """Запуск потока Обновления расписания"""

        def schedule_update():
            print('Обновление расписания.')
            self._downloader.download()
            self._reader.run('xls', write_to_new_db=True, write_to_db=True)
            print('Обновление завершено.')

        # Создаем задания на обновление
        for _time in self._update_time_list:
            schedule.every().day.at(_time).do(schedule_update)
        print('Задание на обновление расписания создано. Каждый день в {}'.format(self._update_time_list))

        # Выполняем обновление расписания при запуске
        schedule_update()

        # Запускаем демона обновления
        while True:
            schedule.run_pending()
            time.sleep(1)


api = FastAPI(title='rtu_timetable_api')


@api.get("/", tags=["index"])
def index() -> RedirectResponse:
    """
    Документация к API
    """
    return RedirectResponse("/docs")


@api.get("/student_timetable", tags=["student_timetable"], response_description="group_name, date")
def groups_get(group_name: str = 'ИНМО-01-20', date: str = '23.02.2021') -> Response:
    """
    Получение расписания студента на определенную дату
    - **group_name**: Название группы
    - **date**: Дата (d.m.Y)
    """
    timetable = StudentTimetable(CONFIG, group_name)
    result = timetable.get_timetable(date)
    formatted_result = json.dumps(result, ensure_ascii=False).encode('utf8')
    return Response(content=formatted_result, media_type="application/json")


@api.get("/teacher_timetable", tags=["teacher_timetable"], response_description="teacher_name, date")
def groups_get(teacher_name: str = 'Зуев А.С.', date: str = '23.02.2021') -> Response:
    """
    Получение расписания преподавателя на определенную дату
    - **teacher_name**: Фамилия/ФИО преподавателя
    - **date**: Дата (d.m.Y)
    """
    timetable = TeacherTimetable(CONFIG, teacher_name)
    result = timetable.get_timetable(date)
    formatted_result = json.dumps(result, ensure_ascii=False).encode('utf8')
    return Response(content=formatted_result, media_type="application/json")


@api.get("/classroom_timetable", tags=["classroom_timetable"], response_description="classroom, date")
def groups_get(classroom: str = 'Г-310', date: str = '23.02.2021') -> Response:
    """
    Получение расписания преподавателя на определенную дату
    - **classroom**: Номер аудитории
    - **date**: Дата (d.m.Y)
    """
    timetable = ClassroomTimetable(CONFIG, classroom)
    result = timetable.get_timetable(date)
    formatted_result = json.dumps(result, ensure_ascii=False).encode('utf8')
    return Response(content=formatted_result, media_type="application/json")


if __name__ == "__main__":
    my_thread = ScheduleUpdater(update_time_list=['01:00', '16:00', '21:00'])
    my_thread.start()

    uvicorn.run("main:api", host="127.0.0.1", port=5000, log_level="debug")
