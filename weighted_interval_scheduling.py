import heapq
import numpy
from copy import deepcopy

class WeightedJob():
    def __init__(self, name, start, finish, weight):
        self.name = name
        self.start = start
        self.finish = finish
        self.weight = weight
        self.time = self.finish - self.start

    def jobInfo(self):
        t = (self.name, self.start, self.finish, self.time, self.weight)
        print(t)

# Imprime todas as tarefas de um schedule
def schedule_info(schedule):
    print('nome, start, finish, time, weight')
    for j in schedule:
        j.jobInfo()

# Retorna True se existe conflito entre duas tarefas
def conflict(a, b):
    if a.finish == b.finish:
        if a.start < b.start:
            first = a
            last = b
        else:
            first = b
            last = a
    elif a.finish < b.finish:
        first = a
        last = b
    elif b.finish < a.finish:
        first = b
        last = a

    if first.start == last.start and first.finish == last.finish:
        return True
    elif first.finish < last.finish and first.finish > last.start:
        return True
    elif last.start < first.finish and last.start > first.start:
        return True
    else:
        return False

# Ordenar o shcedule por ordem crescente de término da tarefa
def order_by_finish(schedule):
    s = deepcopy(schedule)

    finishes = []
    for i in s:
        finishes.append(i.finish)
    heapq.heapify(finishes)
 
    ordered_schedule = []
    while len(ordered_schedule) < len(s):
        for job in s:
            if job.finish == finishes[0]:
                ordered_schedule.append(job)
                heapq.heappop(finishes)
                continue

    return ordered_schedule

# Retorna uma lista com o máximo de tarefas compatíveis em uma determinada schedule
def max_compatible(schedule):
    ordered = order_by_finish(schedule)
    target = ordered[0]

    jobs = []
    jobs.append(target)

    for job in ordered:
        if target == job:
            continue
        elif conflict(target, job):
            continue
        else:
            target = job
            jobs.append(target)
            continue

    return jobs

# Praticamente (WeightedJob a == WeightedJob b)
# Retorna True se dois objetos WeightedJob são iguais
def isEqual(a, b):
    if a.name != b.name:
        return False

    if a.start != b.start:
        return False

    if a.finish != b.finish:
        return False

    if a.weight != b.weight:
        return False

    return True

# Retorna o maior indice i > j tal que os jobs i e j são compatíveis
def closest_compatible(schedule, j):
    schedule = order_by_finish(schedule)

    index = 0
    for i, job in enumerate(schedule):
        if isEqual(job, j):
            return index
        else:
            if conflict(job, j) is False:
                index = i

# As soluções dos subproblemas ficam salvas em um array
# A resposta final é a última posição deste array
def subproblems_array(schedule):
    n = len(schedule)
    m = numpy.zeros(n)

    i = 1
    while i < n:
        j = schedule[i]
        m[i] = max(j.weight + m[closest_compatible(schedule, j)],
                   m[i-1])
        i += 1

    return m

# Retorna o melhor valor possível para uma determinada schedule
# Em outras palavras, retorna o último elemento do array de subproblemas
def best_value(schedule):
    m = subproblems_array(schedule)
    n = len(m)-1

    return m[n]

# Imprime as tarefas que formaram a solução final
def find(schedule, j):
    m = subproblems_array(schedule)

    if j == 0:
        return
    elif schedule[j].weight + m[closest_compatible(schedule, schedule[j])] > m[j-1]:
        print(j)
        find(schedule, closest_compatible(schedule, schedule[j]))
    else:
        find(schedule, closest_compatible(schedule, schedule[j-1]))

# Mostra o resultado de todas as operações
def result(schedule):
    schedule_info(schedule)

    print('O melhor valor possível é {}'.format(best_value(schedule)))
    print('Tarefas escolhidos: ')
    
    find(schedule, len(schedule)-1)

# Retorna uma lista de tarefas que será processada por outras funções
# A primeira tarefa tem que ser nulo
def create_schedule(schedule):
    new_schedule = [WeightedJob('null', 0, 0, 0)]

    for job in schedule:
        new_schedule.append(job)

    return new_schedule

j1 = WeightedJob('a', 0, 3, 1)
j2 = WeightedJob('b', 2, 5, 2)
j3 = WeightedJob('c', 4, 7, 3)
j4 = WeightedJob('d', 6, 9, 4)
j5 = WeightedJob('e', 8, 11, 5)

schedule = create_schedule([j1, j2, j3, j4, j5])
result(schedule)