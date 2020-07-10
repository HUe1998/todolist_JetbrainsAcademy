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
        4: 'add_task'}
while True:
    print('''
1) Today's tasks
2) Week's tasks
3) All tasks
4) Add task
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
