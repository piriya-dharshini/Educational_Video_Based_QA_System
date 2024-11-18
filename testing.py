questions = [
    ("What is the shortest path from the source node to all other nodes?", "bellman_ford(graph, source)"),
    ("What is the shortest path to node X?", "bellman_ford(graph, source)['X']"),
    ("What is the total distance to the destination node?", "bellman_ford(graph, source)[destination]"),
    ("Did the Bellman-Ford algorithm detect a negative weight cycle?", "check_negative_cycle(graph)"),
    ("What is the distance to node X after running Bellman-Ford?", "bellman_ford(graph, source)['X']"),
    ("How many negative weight cycles are present in the graph?", "count_negative_cycles(graph)"),
    ("What is the longest shortest path from the source?", "max(bellman_ford(graph, source).values())"),
    ("What is the distance between node A and node B?", "bellman_ford(graph, source)['A'] + bellman_ford(graph, source)['B']"),
    ("What is the shortest path from node A to node B?", "get_shortest_path(graph, 'A', 'B')"),
    ("What is the path followed to reach the destination node?", "get_shortest_path(graph, source, destination)"),
]
