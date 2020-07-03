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
    deadline = Column(Date, default=datetime.today())

    def __repr__(self):
        return self.task


Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
session = Session()


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
        print('Invalid Input: Choose a Number')
        continue
    if user_input not in menu:
        print('Invalid Input: Choose valid numbers from menu')
        continue
    action = menu[user_input]
    today = datetime.today()

    if action == 'exit':
        print('\nBye!')
        sys.exit()
    elif action == 'today_tasks':
        rows = session.query(Table).all()
        if not rows:
            print(f"\nToday {today.day} {today.strftime('%b')}:")
            print('Nothing to do!')
        else:
            for row in rows:
                print(str(row.id) + '.', row.task) #TODO: replace with fstring
    elif action == 'add_task':
        #TODO: Bookmark
        input_task = input('\nEnter task\n')
        session.add(Table(task=input_task))
        session.commit()
        print('The task has been added!')