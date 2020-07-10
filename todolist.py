from sqlalchemy import create_engine, Column, Integer, String, Date
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime, timedelta
import sys

engine = create_engine('sqlite:///todo.db?check_same_thread=False')
Base = declarative_base()


class Table(Base):
    __tablename__ = 'task'
    id = Column(Integer, primary_key=True)
    task = Column(String)
    # Deadline contains date note datetime
    deadline = Column(Date, default=datetime.today().date())

    def __repr__(self):
        return self.task


Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
session = Session()


# Return task_list from Query Date
def tasks_at_date(query_date):
    task_rows = session.query(Table).filter(Table.deadline == query_date).all()
    if not task_rows:
        return []
    else:
        return [f"{x.task}" for x in task_rows]


# Main Loop
menu = {0: 'exit', 1: 'today_tasks', 2: 'week_tasks', 3: 'all_tasks',
        4: 'missed_tasks', 5: 'add_task', 6: 'delete_task',
        7:'delete_all_missed', 8: 'reset'}
while True:
    print('''
1) Today's tasks
2) Week's tasks
3) All tasks
4) Missed tasks
5) Add task
6) Delete task
7) Delete All Missed
8) Reset
0) Exit''')

    try:
        user_input = int(input())
    except ValueError:
        print('\nInvalid Input: Choose a Number')
        continue
    if user_input not in menu:
        print('\nInvalid Input: Choose valid numbers from menu')
        continue
    action = menu[user_input]
    today = datetime.today()

    if action == 'exit':
        print('\nBye!')
        sys.exit()

    elif action == 'today_tasks':
        task_list = tasks_at_date(today.date())
        if not task_list:
            print(f"\nToday {today.strftime('%d %b')}:")
            print('Nothing to do!')
        else:
            print(f"\nToday {today.strftime('%d %b')}:")
            for index, task in enumerate(task_list):
                print(f"{index + 1}. {task}")

    elif action == 'week_tasks':
        for i in range(7):
            query_date = (today + timedelta(days=i)).date()
            task_list = tasks_at_date(query_date)
            if not task_list:
                print(f'\n{query_date.strftime("%A %d %b")}:')
                print('Nothing to do!')
            else:
                print(f'\n{query_date.strftime("%A %d %b")}:')
                for index, task in enumerate(task_list):
                    print(f"{index + 1}. {task}")

    elif action == 'all_tasks':
        all_rows = session.query(Table).all()
        print("\nAll tasks:")
        for row in all_rows:
            print(f"{row.id}. {row.task}. {row.deadline.strftime('%d %b')}")

    elif action == 'add_task':
        in_task = input('\nEnter task\n')
        in_deadline = datetime.strptime(input('Enter deadline\n'),
                                        '%Y-%m-%d').date()
        session.add(Table(task=in_task, deadline=in_deadline))
        session.commit()
        print('The task has been added!')

    elif action == 'reset':
        x = input('''
This action would reset all tasks!!
Enter 'y' to confirm:
''')
        if x == 'y':
            session.query(Table).delete()
            print('All tasks deleted')
            session.commit()
        else:
            print('Reset Operation Cancelled')
            continue

    # missed_tasks and delete_task uses different if else chain so missed_row
    # is not repeated
    missed_rows = session.query(Table).filter(
        Table.deadline < datetime.today().date()).order_by(
        Table.deadline).all()
    if action == 'missed_tasks':
        print('\nMissed tasks:')
        if not missed_rows:
            print('Nothing is missed!')
        else:
            for ind, row in enumerate(missed_rows):
                print(
                    f"{ind + 1}. {row.task} {row.deadline.strftime('%d %b')}")

    elif action == 'delete_task':
        if not missed_rows:
            print('\nNothing to delete')
        else:
            print('\nChose the number of the task you want to delete:')
            for ind, row in enumerate(missed_rows):
                print(
                    f"{ind + 1}. {row.task} {row.deadline.strftime('%d %b')}")
            # "- 1" term because indexing starts from 1 in print output
            in_del_num = int(input()) - 1
            session.delete(missed_rows[in_del_num])
            session.commit()

    elif action == 'delete_all_missed':
        for row in missed_rows:
            session.delete(row)
        session.commit()
        print('\nAll missed tasks deleted!')