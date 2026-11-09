import parser
from graph import dijkstra, find_paths
from simulation import Drone, Simulation
from visualier import game_loop
import pygame

MAPS: list[tuple[str, str]] = [
        ("Easy 1 - Linear path", "maps/easy/01_linear_path.txt"),
        ("Easy 2 - Simple fork", "maps/easy/02_simple_fork.txt"),
        ("Easy 3 - Basic capacity", "maps/easy/03_basic_capacity.txt"),
        ("Medium 1 - Dead end trap", "maps/medium/01_dead_end_trap.txt"),
        ("Medium 2 - Circular loop", "maps/medium/02_circular_loop.txt"),
        ("Medium 3 - Priority puzzle", "maps/medium/03_priority_puzzle.txt"),
        ("Hard 1 - Maze nightmare", "maps/hard/01_maze_nightmare.txt"),
        ("Hard 2 - Capacity hell", "maps/hard/02_capacity_hell.txt"),
        ("Hard 3 - Ultimate challenge", "maps/hard/03_ultimate_challenge.txt"),
        ("Challenger - Impossible dream", "maps/challenger/01_the_impossible_dream.txt"),
    ]

def run_map(path: str) -> None:
    p = parser.Parser()
    try:
        p.parse_file(path)
    except parser.ParseError as e:
        print(f"Parsing error: {e}")
        return
    p.start_hub.max_drones = p.nb_drones
    p.end_hub.max_drones = p.nb_drones
    adjacency_list = {}
    adjacency_list[p.start_hub.name] = []
    adjacency_list[p.end_hub.name] = []
    for name in p.hubs:
        adjacency_list[name] = []
    for conn in p.connections:
        adjacency_list[conn.a].append(conn.b)
        adjacency_list[conn.b].append(conn.a)

    hubs = dict(p.hubs)
    hubs[p.start_hub.name] = p.start_hub
    hubs[p.end_hub.name] = p.end_hub

    result = dijkstra(adjacency_list, hubs, p.start_hub.name, p.end_hub.name)
    if result:
        cost, path = result
        print(f"Koszt: {cost}, ścieżka: {path}")
    paths = find_paths(adjacency_list, hubs, p.start_hub.name, p.end_hub.name)
    if not paths:
        print("Error: Path missing")
        return
    drones = []
    for i in range(p.nb_drones):
        path = paths[i % len(paths)]
        drones.append(Drone(f"D{i + 1}", path))
    connections = {}
    for conn in p.connections:
        connections[frozenset({conn.a, conn.b})] = conn
    sim = Simulation(drones, adjacency_list, hubs, connections, p.end_hub.name)
    game_loop(sim, hubs, connections)

def menu() -> str | None:
    screen = pygame.display.set_mode((1280, 720))
    font = pygame.font.SysFont("Arial", 32, bold=True)
    clock = pygame.time.Clock()
    selected = 0
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return None
            if event.type == pygame.KEYDOWN and event.key == pygame.K_q:
                return None
            if event.type == pygame.KEYDOWN and event.key == pygame.K_DOWN:
                selected = (selected + 1) % len(MAPS)
            if event.type == pygame.KEYDOWN and event.key == pygame.K_UP:
                selected = (selected - 1) % len(MAPS)
            if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                return MAPS[selected][1]
        screen.fill((0, 0, 0))
        text = font.render("Choose map and press ENTER", True, (255, 255, 255))
        text_position = text.get_rect(center=(1280 // 2, 100))
        screen.blit(text, text_position)
        y_pos = 200
        for i, (name, _) in enumerate(MAPS):
            if i == selected:
                bg_rect = pygame.Rect(1280 // 2 - 250, y_pos - 20, 500, 40)
                pygame.draw.rect(screen, (255, 0, 0), bg_rect)
            text = font.render(name, True, (0, 192, 0))
            text_position = text.get_rect(center=(1280 // 2, y_pos))
            screen.blit(text, text_position)
            y_pos += 50
        pygame.display.flip()
    return None

if __name__ == "__main__":
    while True:
        chosen = menu()
        if chosen is None:
            break
        run_map(chosen)
