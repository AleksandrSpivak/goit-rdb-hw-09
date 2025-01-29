import random
import math


# Визначення функції Сфери
def sphere_function(x):
    return sum(xi ** 2 for xi in x)


# Hill Climbing
def hill_climbing(func, bounds, iterations=1000, epsilon=1e-6):
    # Ініціалізація випадкової точки всередині меж
    current_point = [random.uniform(low, high) for (low, high) in bounds]
    current_value = func(current_point)
    
    for iteration in range(iterations):
        neighbors = []
        # Генерація сусідів шляхом зміщення кожної координати на невеликий крок
        step_size = 0.1  # Розмір кроку може бути налаштований
        for i in range(len(current_point)):
            for delta in [-step_size, step_size]:
                neighbor = current_point.copy()
                neighbor[i] += delta
                # Перевірка меж
                neighbor[i] = max(min(neighbor[i], bounds[i][1]), bounds[i][0])
                neighbors.append(neighbor)
        
        # Вибір сусіда з найменшим значенням функції (мінімізація)
        next_point = min(neighbors, key=lambda x: func(x))
        next_value = func(next_point)
        
        # Перевірка умов зупинки
        if abs(current_value - next_value) < epsilon:
            break
        
        current_point, current_value = next_point, next_value
    
    return current_point, current_value


# Random Local Search
def random_local_search(func, bounds, iterations=1000, epsilon=1e-6):
    # Ініціалізація випадкової точки всередині меж
    current_point = [random.uniform(low, high) for (low, high) in bounds]
    current_value = func(current_point)
    
    for iteration in range(iterations):
        # Генерація випадкового сусіда
        step_size = 0.5  # Розмір кроку може бути налаштований
        new_point = []
        for i in range(len(current_point)):
            delta = random.uniform(-step_size, step_size)
            coord = current_point[i] + delta
            # Перевірка меж
            coord = max(min(coord, bounds[i][1]), bounds[i][0])
            new_point.append(coord)
        
        new_value = func(new_point)
        
        # Прийняття нового сусіда, якщо він краще або з певною ймовірністю
        probability = 0.2  # Ймовірність прийняття гіршого рішення
        if new_value < current_value or random.random() < probability:
            if abs(current_value - new_value) < epsilon:
                break
            current_point, current_value = new_point, new_value
    
    return current_point, current_value


# Simulated Annealing
def simulated_annealing(func, bounds, iterations=1000, temp=1000, cooling_rate=0.95, epsilon=1e-6):
    # Ініціалізація випадкової точки всередині меж
    current_point = [random.uniform(low, high) for (low, high) in bounds]
    current_value = func(current_point)
    best_point = current_point.copy()
    best_value = current_value
    
    for iteration in range(iterations):
        # Генерація сусіда
        step_size = 1.0  # Розмір кроку може бути налаштований
        new_point = []
        for i in range(len(current_point)):
            delta = random.uniform(-step_size, step_size)
            coord = current_point[i] + delta
            # Перевірка меж
            coord = max(min(coord, bounds[i][1]), bounds[i][0])
            new_point.append(coord)
        
        new_value = func(new_point)
        delta_energy = new_value - current_value
        
        # Прийняття нового сусіда
        if delta_energy < 0 or random.random() < math.exp(-delta_energy / temp):
            current_point, current_value = new_point, new_value
            # Оновлення найкращого рішення
            if new_value < best_value:
                best_point, best_value = new_point, new_value
        
        # Перевірка умов зупинки
        if temp < epsilon or abs(delta_energy) < epsilon:
            break
        
        # Охолодження
        temp *= cooling_rate
    
    return best_point, best_value


if __name__ == "__main__":
    # Межі для функції
    bounds = [(-5, 5), (-5, 5)]
    
    # Параметри алгоритмів
    iterations = 10000
    epsilon = 1e-6
    
    # Виконання алгоритму Hill Climbing
    print("Hill Climbing:")
    hc_solution, hc_value = hill_climbing(sphere_function, bounds, iterations=iterations, epsilon=epsilon)
    print("Розв'язок:", hc_solution, "Значення:", hc_value)
    
    # Виконання алгоритму Random Local Search
    print("\nRandom Local Search:")
    rls_solution, rls_value = random_local_search(sphere_function, bounds, iterations=iterations, epsilon=epsilon)
    print("Розв'язок:", rls_solution, "Значення:", rls_value)
    
    # Виконання алгоритму Simulated Annealing
    print("\nSimulated Annealing:")
    sa_solution, sa_value = simulated_annealing(sphere_function, bounds, iterations=iterations, temp=1000, cooling_rate=0.95, epsilon=epsilon)
    print("Розв'язок:", sa_solution, "Значення:", sa_value)
