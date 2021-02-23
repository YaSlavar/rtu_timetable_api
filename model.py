from peewee import *


class BaseModel(Model):
    """Базовая модель"""

    class Meta:
        database = SqliteDatabase('output/timetable.db')  # соединение с базой


class Groups(BaseModel):
    """Группы"""
    group_id = AutoField(column_name='group_id', primary_key=True, index=True)
    group_name = TextField(column_name='group_name', null=True)

    class Meta:
        table_name = 'groups'


class LessonTypes(BaseModel):
    """Типы занятий"""
    lesson_type_id = AutoField(column_name='lesson_type_id', primary_key=True, index=True)
    lesson_type_name = TextField(column_name='lesson_type_name', null=True)

    class Meta:
        table_name = 'lesson_types'


class Disciplines(BaseModel):
    """Названия дисциплин"""
    discipline_id = AutoField(column_name='discipline_id', primary_key=True, index=True)
    discipline_name = TextField(column_name='discipline_name', null=True)

    class Meta:
        table_name = 'disciplines'


class Occupations(BaseModel):
    """Тип расписания"""
    occupation_id = AutoField(column_name='occupation_id', primary_key=True, index=True)
    occupation = TextField(column_name='occupation', null=True)

    class Meta:
        table_name = 'occupations'


class Rooms(BaseModel):
    """Аудитории"""
    room_id = AutoField(column_name='room_id', primary_key=True, index=True)
    room_num = TextField(column_name='room_num', null=True)

    class Meta:
        table_name = 'rooms'


class ScheduleCalls(BaseModel):
    """Расписание звонков"""
    call_id = AutoField(column_name='call_id', primary_key=True, index=True)
    call_time = TimeField(column_name='call_time', null=True)

    class Meta:
        table_name = 'schedule_calls'


class Teachers(BaseModel):
    """Преподаватели"""
    teacher_id = AutoField(column_name='teacher_id', primary_key=True, index=True)
    teacher_name = TextField(column_name='teacher_name', null=True)

    class Meta:
        table_name = 'teachers'


class Lessons(BaseModel):
    """Занятия"""
    lesson_id = AutoField(column_name='lesson_id', primary_key=True, index=True)
    group_num = ForeignKeyField(Groups, column_name='group_num', lazy_load=False)
    occupation = ForeignKeyField(Occupations, column_name='occupation', lazy_load=False)
    discipline = ForeignKeyField(Disciplines, column_name='discipline', lazy_load=False)
    teacher = ForeignKeyField(Teachers, column_name='teacher', lazy_load=False)
    date = TextField(column_name='date', null=True)
    day = IntegerField(column_name='day')
    call_num = ForeignKeyField(ScheduleCalls, column_name='call_num', lazy_load=False)
    week = IntegerField(column_name='week')
    lesson_type = ForeignKeyField(LessonTypes, column_name='lesson_type', lazy_load=False)
    room = ForeignKeyField(Rooms, column_name='room', lazy_load=False)
    include = TextField(column_name='include', null=True)
    exception = TextField(column_name='exception', null=True)

    class Meta:
        table_name = 'lessons'


if __name__ == "__main__":
    query = Lessons.select()
    print(query)
    lessons_selected = query.dicts().execute()
    print(lessons_selected)
