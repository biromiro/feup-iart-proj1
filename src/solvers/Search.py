from queue import PriorityQueue


class Search:
    @staticmethod
    def getPath(node):
        path = [node]
        currentNode = node

        while True:
            currentNode = currentNode.previousNode
            if not currentNode:
                break
            path.append(currentNode)

        path.reverse()

        return path

    @staticmethod
    def bfs(initial, condition):

        nodesToVisit = [initial]
        visited = []
        count = 0
        while nodesToVisit:
            currentNode = nodesToVisit.pop(0)

            if currentNode in visited:
                continue
            yield currentNode
            if condition(currentNode):
                return

            if count == 100:
                count = 0
            else:
                count += 1

            nodesToVisit += currentNode.child_states()

            visited.append(currentNode)

        return None

    @staticmethod
    def dls(node, condition, depth, visited=[]):

        if node in visited:
            return (None, False)
        if condition(node):
            return (node, False)
        if depth == 0:
            return (None, visited != [])

        for child in node.child_states():
            if child in visited:
                continue

            finalNode, _ = Search.dls(child, condition, depth - 1,
                                      visited + [node])
            if finalNode:
                return (finalNode, False)

        return (None, visited == [])

    @staticmethod
    def it_deep(initial, condition):

        path = None
        curDepth = 1

        while True:

            path, remaining = Search.dls(initial, condition, curDepth)
            if path:
                return path
            if not remaining:
                return None

            curDepth += 1

    @staticmethod
    def greedy(initial, condition, heuristic):

        nodesToVisit = PriorityQueue()
        nodesToVisit.put((heuristic(initial), initial))

        visited = []

        while not nodesToVisit.empty():
            _, currentNode = nodesToVisit.get()

            if currentNode in visited:
                continue

            visited.append(currentNode)

            if condition(currentNode):
                return currentNode

            edgeNodes = currentNode.child_states()

            for node in edgeNodes:
                nodesToVisit.put((heuristic(node), node))

        return None

    @staticmethod
    def astar(initial, condition, heuristic):

        nodesToVisit = PriorityQueue()
        nodesToVisit.put((heuristic(initial), initial))
        visited = []

        while not nodesToVisit.empty():
            _, currentNode = nodesToVisit.get()

            if currentNode in visited:
                continue

            visited.append(currentNode)

            if condition(currentNode):
                return currentNode
            edgeNodes = currentNode.child_states()

            for node in edgeNodes:
                heuristicNode = len(node.commands) + heuristic(node)
                nodesToVisit.put((heuristicNode, node))

        return None
