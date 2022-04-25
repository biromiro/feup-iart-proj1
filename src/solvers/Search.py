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
    def dls(node, condition, depth, visited=None):
        if not visited:
            visited = []

        if node in visited:
            return (False, False)
        yield node
        if condition(node):
            return (True, False)
        if depth == 0:
            return (False, visited != [])

        for child in node.child_states():
            if child in visited:
                continue

            solved, remaining = yield from Search.dls(child, condition, depth - 1,
                                      visited + [node])
            if not remaining:
                return (solved, False)

        return (False, visited == [])

    @staticmethod
    def it_deep(initial, condition):
        curDepth = 1

        while True:

            _, remaining = yield from Search.dls(initial, condition, curDepth)

            if not remaining:
                return

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

            yield currentNode

            visited.append(currentNode)

            if condition(currentNode):
                return

            edgeNodes = currentNode.child_states()

            for node in edgeNodes:
                nodesToVisit.put((heuristic(node), node))

    @staticmethod
    def astar(initial, condition, heuristic):

        nodesToVisit = PriorityQueue()
        nodesToVisit.put((heuristic(initial), initial))
        visited = []

        while not nodesToVisit.empty():
            _, currentNode = nodesToVisit.get()

            if currentNode in visited:
                continue
        
            yield currentNode

            visited.append(currentNode)

            if condition(currentNode):
                return
            edgeNodes = currentNode.child_states()

            for node in edgeNodes:
                heuristicNode = len(node.commands) + heuristic(node)
                nodesToVisit.put((heuristicNode, node))
