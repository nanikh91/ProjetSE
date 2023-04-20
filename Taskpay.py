# Importe les différents modules nécessaires :

import timeit # permet de mesurer le temps d'exécution d'une fonction
import random # permet de générer des nombres aléatoires
from typing import List, Dict # permet d'importer les types List et Dict
import multiprocessing # permet d'exécuter les tâches en parallèle

# Classe pour représenter une tâche avec un nom, des entrées, des sorties et la fonction à exécuter :

class Task :
    def __init__(self, name: str, reads: List[str], writes: List[str], run) : # méthode d'initialisation à 4 arguments : nom de la tâche (chaîne de caractères str, vide par défaut), liste des noms des variables lues par la tâche (liste de chaînes de caractères List[str] vide par défaut), liste des noms des variables écrites par la tâche (liste de chaînes de caractères List[str] vide par défaut) et la fonction qui doit être exécutée pour effectuer la tâche (pas de type spécifié, None par défaut).
        # Tests de validation des arguments passés :
        if not isinstance(name, str) or len(name) == 0 :
            raise ValueError("La tâche doit pas être vide et doit être en String") # teste si l'argument name est une chaîne de caractères non vide. Si ce n'est pas le cas, une ValueError est levée avec un message d'erreur clair
        self.name = name # si l'argument name est valide, il est affecté à la variable d'instance name.
        if not isinstance(reads, list) :
            raise ValueError("la tâche reads domain doit être une liste") # teste si l'argument reads est une liste. Si ce n'est pas le cas, une ValueError est levée avec un message d'erreur clair
        self.reads = reads # si l'argument reads est valide, il est affecté à la variable d'instance reads
        if not isinstance(writes, list) :
            raise ValueError("la tâche writes domain doit être une liste") # teste si l'argument writes est une liste. Si ce n'est pas le cas, une ValueError est levée avec un message d'erreur clair
        self.writes = writes # si l'argument writes est valide, il est affecté à la variable d'instance writes
        self.run = run # aucune validation de type n'est effectuée ici

# Classe pour représenter un système de tâches composé de plusieurs tâches et de leurs dépendances associées :

class TaskSystem :
    def __init__(self, tasks: List[Task], dependences: Dict[str, List[str]]) : # méthode d'initialisation à 2 arguments : une liste d’objets de classe Task List[Task] représentant les tâches du système et un dictionnaire Dict[str, List[str]]
        self.tasks = tasks
        self.dependences = dependences

        # Vérification de doublons :
        task_names = [task.name for task in tasks]
        if len(task_names) != len(set(task_names)) :
            raise ValueError("Doublon dans le Tasksystem")

            # Verification d'existence de dépendances :
        for task_name, deps in dependences.items() :
            if task_name not in task_names :
                raise ValueError(f"La tâche '{task_name}' est introuvable dans le TaskSystem.")
            for dep in deps :
                if dep not in task_names :
                    raise ValueError(f"Dependence '{dep}' pour la tâche '{task_name}' est introuvable dans le TaskSystem.")
        self.dependences = dependences

# Méthode qui retourne les dépendances d'une tâche sous la forme d'une liste de noms de tâches :
# Elle est utilisée pour obtenir la liste des tâches préalables nécessaires à l'exécution d'une tâche donnée.

    def getDependencies(self, name) :
        Tab_dependence = []
        for task in self.tasks :
            if name in task.writes :
                for depend in task.reads :
                    if depend not in Tab_dependence :
                        Tab_dependence.append(depend)
        return Tab_dependence

    # Méthode qui exécute séquentiellement les tâches du projet dans l'ordre spécifié par les dépendances.
    # Elle garantit que les tâches sont exécutées de manière séquentielle, c'est-à-dire qu'une tâche ne démarre pas tant que toutes ses tâches préalables ne sont pas terminées.

    def runSeq(self) :
        for task in self.tasks :
            task.run()

    # Méthode utilisée comme cible de la fonction de map dans la méthode run(self).
    # Elle est responsable de l'exécution d'une tâche spécifique avec les valeurs de variables fournies en argument.

    def executer_tache(self, task_name) :
        task = next(task for task in self.tasks if task.name == task_name)
        task.run()

    # Méthode qui exécute les tâches du projet en parallèle en utilisant la multiprogrammation. Elle identifie les tâches qui sont prêtes à être exécutées,
    # c'est-à-dire celles dont toutes les tâches préalables sont terminées, et les exécute en parallèle en utilisant un pool de processus.

    def run(self) :
        GrapheTask = {} # dictionnaire
        for task in self.tasks :
            GrapheTask[task.name] = {'reads' : task.reads, 'writes' : task.writes, 'run' : task.run}
        TaskDone = []
        while len(TaskDone) != len(self.tasks) :
            TaskDisponible = []
            for task_name in GrapheTask.keys() :
                if task_name not in TaskDone :
                    Getdep = self.getDependencies(task_name) # obtient les dépendances de la tâche en appelant la méthode getDependencies
                    if all(dep in TaskDone for dep in Getdep) :
                        TaskDisponible.append(task_name)

            with multiprocessing.Pool() as pool :
                pool.map(self.executer_tache, TaskDisponible)

            TaskDone.extend(TaskDisponible)

    # Méthode qui effectue un test de détermination en générant des valeurs aléatoires pour les variables associées aux tâches du projet, et en vérifiant si les résultats des tâches sont cohérents.
    # Elle prend en paramètre le nombre de fois que le test doit être répété.

    def detTestRnd(self, n) :
        for i in range(n) :
            DicoVar = {}
            for task in self.tasks :
                for var in task.reads + task.writes :
                    if var not in DicoVar :
                        DicoVar[var] = random.randint(0, 100)
                # Appeler la méthode de la tâche directement avec les valeurs générées aléatoirement
                task(DicoVar)
            # Vérifier les résultats de chaque tâche
            results = [task() for task in self.tasks]
            if len(set(results)) > 1 :
                return False
        return True

    # Méthode qui compare les temps d'exécution séquentielle et parallèle du système de tâches :
    # Le coût de chaque tâche est déterminé en fonction de ses lectures et écritures, ainsi que du coût d'exécution de la tâche lui-même.

    def parCost(self) :
        # Exécution séquentielle :
        Seqtimer = timeit.timeit(self.runSeq, number=1)
        # Exécution parallèle :
        Partimer = timeit.timeit(self.run, number=1)
        # Différence de temps absolue :
        print("Temps d'éxecution sequential:  ", Seqtimer)
        print("Temps d'éxecution parallel:  ", Partimer)
        print("Time Difference: ", abs(Partimer - Seqtimer))


