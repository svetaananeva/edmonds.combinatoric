from collections import deque

# Класс для представления графа
class Graph:
    def __init__(self, vertices):
        self.V = vertices  # Количество вершин
        self.graph = {i: {} for i in range(vertices)}  # Граф в виде словаря {вершина: {сосед: пропускная способность}}

    def add_edge(self, u, v, capacity):
        self.graph[u][v] = capacity
        self.graph[v][u] = 0  # Добавление обратного рёбра с нулевой пропускной способностью

    def bfs(self, source, sink, parent):
        visited = [False] * self.V
        queue = deque([source])
        visited[source] = True

        while queue:
            u = queue.popleft()

            for v in self.graph[u]:
                if not visited[v] and self.graph[u][v] > 0:  # Остаточная пропускная способность > 0
                    queue.append(v)
                    visited[v] = True
                    parent[v] = u
                    if v == sink:
                        return True
        return False

    def edmonds_karp(self, source, sink):
        parent = [-1] * self.V  # Массив для восстановления пути
        max_flow = 0

        # Повторяем, пока существует увеличивающий путь
        while self.bfs(source, sink, parent):
            # Находим минимальную остаточную пропускную способность по пути
            path_flow = float('Inf')
            s = sink
            while s != source:
                path_flow = min(path_flow, self.graph[parent[s]][s])
                s = parent[s]

            # Обновляем остаточную сеть
            max_flow += path_flow
            v = sink
            while v != source:
                u = parent[v]
                self.graph[u][v] -= path_flow  # Уменьшаем пропускную способность прямого пути
                self.graph[v][u] += path_flow  # Увеличиваем пропускную способность обратного пути
                v = parent[v]

        return max_flow


# Пример использования алгоритма
if __name__ == "__main__":
    g = Graph(6)  # 6 вершин (0, 1, 2, 3, 4, 5)

    # Добавление рёбер с пропускной способностью
    g.add_edge(0, 1, 16)
    g.add_edge(0, 2, 13)
    g.add_edge(1, 2, 10)
    g.add_edge(1, 3, 12)
    g.add_edge(2, 1, 4)
    g.add_edge(2, 4, 14)
    g.add_edge(3, 2, 9)
    g.add_edge(3, 5, 20)
    g.add_edge(4, 3, 7)
    g.add_edge(4, 5, 4)

    # Нахождение максимального потока из источника 0 в сток 5
    source = 0
    sink = 5

    max_flow = g.edmonds_karp(source, sink)
    print(f"Максимальный поток из источника {source} в сток {sink}: {max_flow}")
