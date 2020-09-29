
# IMPORTS:
import sqlite3


# TASK CLASS:
class Task:
    #Attributes:
    def __init__(self, title: str, duration: int, progress: int):
        self.title = title
        self.duration = duration
        self.progress = progress
    #Methods:
    def __str__(self):
        return self.title + " " + str(self.duration) + "mins " + str(self.progress) + "%"
    def tup(self):
        return (self.title, self.duration, self.progress)

# TASKMAN CLASS:
class TaskMan:
    #Attributes:
    def __init__(self):
        self.tasklist = []
    #Methods to modify the taskmanager:
    def show(self):
        for ind,task in enumerate(self.tasklist):
            print(ind,',', str(task))
    def save_single(self,task):
        conn = sqlite3.connect('taskmanager_database.sqlite')
        c = conn.cursor()
        c.execute('INSERT INTO taskmanager_tab(taskTitle,taskDuration,taskProgress) VALUES (?,?,?)',task.tup())
        c.execute('SELECT * FROM taskmanager_tab')  
        conn.commit()
        c.close()
    def add(self,new_task):
        self.tasklist.append(new_task)
        self.save_single(new_task)
    def rm(self,index):
        self.tasklist.pop(index)
        conn = sqlite3.connect('taskmanager_database.sqlite')
        c = conn.cursor()
        c.execute('''DELETE FROM taskmanager_tab
                   WHERE id = (?)''',(index,))
        conn.commit()
        c.close()
    def tup(self):
        tasklist_copy = self.tasklist.copy()
        for ind,task in enumerate(self.tasklist):
            task_tup = task.tup()
            tasklist_copy.pop(ind)
            tasklist_copy.insert(ind,task_tup)
        return tasklist_copy

        
    #Methods for import/exports:
    def import_from_database(self):
        conn = sqlite3.connect('taskmanager_database.sqlite')
        c = conn.cursor()
        c.execute('SELECT * FROM taskmanager_tab')
        self.tasklist = []
        for row in c.fetchall():
            new_task = Task(row[1],row[2],row[3])
            self.tasklist.append(new_task)
        c.close()
    def export_to_database(self):
        taskman_tup = self.tup()
        conn = sqlite3.connect('taskmanager_database.sqlite')
        c = conn.cursor()
        
        c.executemany('INSERT INTO taskmanager_tab(taskTitle,taskDuration,taskProgress) VALUES (?,?,?)',taskman_tup)
        c.execute('SELECT * FROM taskmanager_tab')  
        print('Your database..')
        for row in c.fetchall():
            print(row)
        conn.commit()
        c.close()  

def main():
    
    conn = sqlite3.connect('taskmanager_database.sqlite')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS taskmanager_tab
                    (id INTEGER PRIMARY KEY, taskTitle TEXT, taskDuration INTEGER, taskProgress INTEGER)
                 ''')

    my_taskman = TaskMan()
    my_taskman.import_from_database()

    contr = 1
    while contr == 1:
        menu_choice = input('''Choose an option:
        1-Show the current tasklist
        2-Add a new task to the tasklist
        3-Remove a task from the tasklist
        4-Quit
        >> ''')

        if menu_choice == '1':
            my_taskman.show()
        
        elif menu_choice == '2':
            title_to_add = input('task title >> ')
            duration_to_add = input('duration mins >> ')
            progress_to_add = input('progress % >> ')
            to_add = Task(title_to_add,duration_to_add,progress_to_add)
            my_taskman.add(to_add)
            
        elif menu_choice == '3':
            index_to_rm = int(input('task index >> '))
            my_taskman.rm(index_to_rm)

        elif menu_choice == '4':
            print('Bye!')
            contr = '0'  

        else: 
            print('This option is not available! Please try again..')  


if __name__ == "__main__":
    main()

