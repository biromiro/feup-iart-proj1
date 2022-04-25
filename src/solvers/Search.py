from queue import PriorityQueue


class Search:
    """Search algorithms. The algorithms yield the sequence of every visited state."""

    @staticmethod
    def bfs(initial, condition):
        """Breadth-first search."""
        nodesToVisit = [initial]
        visited = []

        while nodesToVisit:
            currentNode = nodesToVisit.pop(0)

            if currentNode in visited:
                continue
            yield currentNode
            if condition(currentNode):
                return

            nodesToVisit += currentNode.child_states()

            visited.append(currentNode)
        return None

    @staticmethod
    def dls(node, condition, depth, visited=None):
        """Depth-limited search. Returns whether a solution was found and whether there are still nodes that should be visited."""
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

            solved, _ = yield from Search.dls(child, condition, depth - 1,
                                      visited + [node])
            if solved:
                return (solved, False)

        return (False, visited == [])

    @staticmethod
    def it_deep(initial, condition):
        """Iterative deepening search."""
        curDepth = 1
        while True:
            _, remaining = yield from Search.dls(initial, condition, curDepth)
            if not remaining:
                return
            curDepth += 1

    @staticmethod
    def greedy(initial, condition, heuristic):
        """Greedy search."""
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
        """A* search."""
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
