from model import *


def get_group_names(group_name: str = ''):
    """
    Получение названия групп по шаблону
    :param group_name: название группы
    :return: названия групп dict
    """
    _query = Groups.select().where(Groups.group_name.contains(group_name))
    return _query.dicts().execute()


def get_teacher_names(teacher_name: str = ''):
    """
    Получение ФИО преподавателей по шаблону
    :param teacher_name: Фамилия И.О. преподавателя
    :return: Фамилия И.О. преподавателя dict
    """
    _query = Teachers.select().where(Teachers.teacher_name.contains(teacher_name))
    return _query.dicts().execute()


def get_timetable_for_group(group_name: str = 'ИНМО-01-20'):
    """
    Получение полного расписания для одной группы
    :param group_name: название группы
    :return: расписание dict
    """
    _query = Lessons.select(
        Groups.group_name.alias('group'), Occupations.occupation.alias('occupation'),
        Disciplines.discipline_name.alias("discipline"), Teachers.teacher_name.alias('teacher'),
        Lessons.date, Lessons.day,
        ScheduleCalls.call_time.alias('call_time'), Lessons.week, LessonTypes.lesson_type_name.alias('lesson_type'),
        Rooms.room_num.alias('room'), Lessons.include, Lessons.exception
    ) \
        .switch(Lessons).join(Disciplines, JOIN.LEFT_OUTER) \
        .switch(Lessons).join(Groups, JOIN.LEFT_OUTER) \
        .switch(Lessons).join(LessonTypes, JOIN.LEFT_OUTER) \
        .switch(Lessons).join(Occupations, JOIN.LEFT_OUTER) \
        .switch(Lessons).join(Rooms, JOIN.LEFT_OUTER) \
        .switch(Lessons).join(ScheduleCalls, JOIN.LEFT_OUTER) \
        .switch(Lessons).join(Teachers, JOIN.LEFT_OUTER) \
        .where(Groups.group_name == group_name)

    return _query.dicts().execute()


def get_timetable_for_teacher(teacher_name: str = 'Смирнов'):
    """
    Получение полного расписания для преподавателя
    :param teacher_name: Фамилия И.О. преподавателя
    :return: расписание dict
    """
    _query = Lessons.select(
        Groups.group_name.alias('group'), Occupations.occupation.alias('occupation'),
        Disciplines.discipline_name.alias("discipline"), Teachers.teacher_name.alias('teacher'),
        Lessons.date, Lessons.day,
        ScheduleCalls.call_time.alias('call_time'), Lessons.week, LessonTypes.lesson_type_name.alias('lesson_type'),
        Rooms.room_num.alias('room'), Lessons.include, Lessons.exception
    ) \
        .switch(Lessons).join(Disciplines, JOIN.LEFT_OUTER) \
        .switch(Lessons).join(Groups, JOIN.LEFT_OUTER) \
        .switch(Lessons).join(LessonTypes, JOIN.LEFT_OUTER) \
        .switch(Lessons).join(Occupations, JOIN.LEFT_OUTER) \
        .switch(Lessons).join(Rooms, JOIN.LEFT_OUTER) \
        .switch(Lessons).join(ScheduleCalls, JOIN.LEFT_OUTER) \
        .switch(Lessons).join(Teachers, JOIN.LEFT_OUTER) \
        .where(Teachers.teacher_name.contains(teacher_name))
    return _query.dicts().execute()


def get_timetable_for_classroom(classroom: str = '145б'):
    """
    Получение полного расписания для преподавателя
    :param classroom: Номер аудитории
    :return: расписание dict
    """
    _query = Lessons.select(
        Groups.group_name.alias('group'), Occupations.occupation.alias('occupation'),
        Disciplines.discipline_name.alias("discipline"), Teachers.teacher_name.alias('teacher'),
        Lessons.date, Lessons.day,
        ScheduleCalls.call_time.alias('call_time'), Lessons.week, LessonTypes.lesson_type_name.alias('lesson_type'),
        Rooms.room_num.alias('room'), Lessons.include, Lessons.exception
    ) \
        .switch(Lessons).join(Disciplines, JOIN.LEFT_OUTER) \
        .switch(Lessons).join(Groups, JOIN.LEFT_OUTER) \
        .switch(Lessons).join(LessonTypes, JOIN.LEFT_OUTER) \
        .switch(Lessons).join(Occupations, JOIN.LEFT_OUTER) \
        .switch(Lessons).join(Rooms, JOIN.LEFT_OUTER) \
        .switch(Lessons).join(ScheduleCalls, JOIN.LEFT_OUTER) \
        .switch(Lessons).join(Teachers, JOIN.LEFT_OUTER) \
        .where(Rooms.room_num.contains(classroom))
    return _query.dicts().execute()


if __name__ == "__main__":

    timetable_list = get_timetable_for_teacher("Зуев")
    for item in timetable_list:
        print(item)

    timetable_list = get_timetable_for_group("ИНМО-01-20")
    for item in timetable_list:
        print(item)

    timetable_list = get_timetable_for_classroom("Г-310")
    for item in timetable_list:
        print(item)
