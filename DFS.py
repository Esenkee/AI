import time
from pyamaze import maze, agent, textLabel


def DFS(m):
    start = (m.rows, m.cols)
    goal = (1, 1)

    explored = [start]
    frontier = [start]
    dfsPath = {}

    while frontier:
        currCell = frontier.pop()

        if currCell == goal:
            break

        for d in 'ESNW':
            if m.maze_map[currCell][d]:

                if d == 'E':
                    childCell = (currCell[0], currCell[1] + 1)
                elif d == 'W':
                    childCell = (currCell[0], currCell[1] - 1)
                elif d == 'S':
                    childCell = (currCell[0] + 1, currCell[1])
                elif d == 'N':
                    childCell = (currCell[0] - 1, currCell[1])

                if childCell in explored:
                    continue

                explored.append(childCell)
                frontier.append(childCell)
                dfsPath[childCell] = currCell

    fwdPath = {}
    cell = goal

    while cell != start:
        fwdPath[dfsPath[cell]] = cell
        cell = dfsPath[cell]

    return fwdPath, explored


m = maze(5, 5)
m.CreateMaze()

start_time = time.perf_counter()
path, explored = DFS(m)
elapsed_ms = (time.perf_counter() - start_time) * 1000

print("DFS path:", path)
print(f"DFS execution time: {elapsed_ms:.3f} ms")
print(f"Visited nodes: {len(explored)}")
print(f"Path length: {len(path) + 1}")

a = agent(m, footprints=True)
m.tracePath({a: path})
l = textLabel(m, 'Length of Path', len(path) + 1)
l2 = textLabel(m, 'Execution Time (ms)', round(elapsed_ms, 3))
l3 = textLabel(m, 'Visited Nodes', len(explored))

m.run()