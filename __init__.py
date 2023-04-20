from mxpay import Task, TaskSystem

# Creation des tâches
task1 = Task("Task1", ["Task2"], ["Task3"], lambda: print("A"))
task2 = Task("Task2", ["Task4"], ["Task5"], lambda: print("B"))
task3 = Task("Task3", [], [], lambda: print("C"))
task4 = Task("Task4", ["Task3"], [], lambda: print("D"))
task5 = Task("Task5", ["Task2"], [], lambda: print("E"))
task6 = Task("Task6", ["Task7"], ["Task8"], lambda: print("F"))
task7 = Task("Task7", [], [], lambda: print("G"))
task8 = Task("Task8", ["Task7"], [], lambda: print("H"))
task9 = Task("Task9", ["Task8"], ["Task1"], lambda: print("I"))
task10 = Task("Task10", [], [], lambda: print("J"))


# Creation du TaskSystem
tasks = [task1, task2, task3, task4, task5, task6, task7, task8, task9, task10]

# Définition des dépendences
dependences = {
    "Task1": [],
    "Task2": ["Task4"],
    "Task3": ["Task1", "Task5"],
    "Task4": ["Task2"],
    "Task5": ["Task1"],
    "Task6": ["Task7"],
    "Task7": [],
    "Task8": ["Task7"],
    "Task9": ["Task8"],
    "Task10": []
}

# Creation d'une instance TaskSystem avec Tasks et dependences
System = TaskSystem(tasks, dependences)

# Test getDependencies() method
task_name = "Task5"
dependencies = System.getDependencies(task_name)
print("Dependencies of task", task_name, ":", dependencies)
print("******************************************")

# Test detTestRnd(n) method
result = System.detTestRnd(5)
print(result)
print("******************************************")


# Execution séquentielle
System.runSeq()
# Execution parallèle
System.run()

print("******************************************")

# Test parCost() method
System.parCost()
