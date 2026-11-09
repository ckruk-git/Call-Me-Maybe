import pygame
import parser
pygame.init()
        
class Visualizer:
    def __init__(self, hubs: list, connections: list):
        self.hubs: dict[str, parser.Hub] = hubs
        self.connections: dict[frozenset[str], parser.Connection] = connections
        self.margin: int = 60
        self.min_x: int = min(h.x for h in hubs.values())
        self.min_y: int = min(h.y for h in hubs.values())
        self.max_x: int = max(h.x for h in hubs.values())
        self.max_y: int = max(h.y for h in hubs.values())
        self.cell_size: int = 200
        self.screen_width: int = 1280
        self.screen_height: int = 720
        range_x: int = max(self.max_x - self.min_x, 1)
        range_y: int = max(self.max_y - self.min_y, 1)
        available_w: int = self.screen_width - 2 * self.margin
        available_h: int = self.screen_height - 2 * self.margin
        self.cell_size: int = min(available_w // range_x, available_h // range_y)
        self.cell_size: int = max(self.cell_size, 40)
        map_w: int = range_x * self.cell_size
        map_h: int = range_y * self.cell_size
        self.offset_x: int = (self.screen_width - map_w) // 2
        self.offset_y: int = (self.screen_height - map_h) // 2
        self.font: pygame.font.Font = pygame.font.SysFont("Arial", 18)
        self.drone_img: pygame.Surface = pygame.image.load("drone.png")
        self.drone_img: pygame.Surface = pygame.transform.scale(self.drone_img, (100, 100))

    def to_pixels(self, hub: parser.Hub) -> tuple[int, int]:
        px = self.offset_x + (hub.x - self.min_x) * self.cell_size
        py = self.offset_y + (self.max_y - hub.y) * self.cell_size
        return px, py

    def color_parser(self, color: str) -> tuple[int, int, int]:
        mapping = {
            "orange": (255, 160, 16),
            "red": (255, 0, 0),
            "blue": (0, 32, 255),
            "green": (0, 192, 0),
            "yellow": (255, 255, 0),
        }
        return mapping.get(color, (255, 255, 255))

    def draw_hub(self, screen: pygame.Surface, sim: Simulation) -> None:
        turn_font = pygame.font.SysFont("Arial", 32, bold=True)
        for hub in self.hubs.values():
            px, py = self.to_pixels(hub)
            size = self.cell_size // 2
            color = self.color_parser(hub.color)
            pygame.draw.rect(screen, color, [px - size // 2, py - size // 2, size, size])
        text = turn_font.render(f"Turn {sim.turn}", True, (255, 255, 255))
        text_position = text.get_rect(center=(self.screen_width // 2, 80))
        screen.blit(text, text_position)
        
    def draw_connection(self, screen: pygame.Surface) -> None:
        for conn in self.connections.values():
            x1, y1 = self.to_pixels(self.hubs[conn.a])
            x2, y2 = self.to_pixels(self.hubs[conn.b])
            pygame.draw.line(screen, (255, 255, 255), (x1, y1), (x2, y2), 4)

    def draw_names(self, screen: pygame.Surface) -> None:
        for hub in self.hubs.values():
            px, py = self.to_pixels(hub)
            text = self.font.render(hub.name, True, (255, 255, 255))
            text_position = text.get_rect(center=(px, py - 35))
            screen.blit(text, text_position)

    def draw_drone(self, screen: pygame.Surface, sim: Simulation) -> None:
        animation = {}
        for drone in sim.drones:
            hub = self.hubs[drone.position]
            prev_hub = self.hubs[drone.prev_position]
            x, y = self.to_pixels(hub)
            prev_x, prev_y = self.to_pixels(prev_hub)
            if x == prev_x and y == prev_y:
                continue
            direction_x = x - prev_x
            direction_y = y - prev_y
            sign_x = 1
            sign_y = 1
            if direction_x < 0:
                direction_x = direction_x * (-1)
                sign_x = -1
            if direction_y < 0:
                direction_y = direction_y * (-1)
                sign_y = -1
            if direction_x > direction_y:
                step_x = 1
                step_y = direction_y / direction_x
            elif direction_x < direction_y:
                step_x = direction_x / direction_y
                step_y = 1
            elif direction_y == direction_x and direction_x != 0:
                step_x = 1
                step_y = 1
            else:
                step_x = 0
                step_y = 0
            if step_x != 0 and sign_x < 0:
                step_x = step_x * sign_x
            if step_y != 0 and sign_y < 0:
                step_y = step_y * sign_y

            animation[drone.id] = {
                'x': x,
                'y': y,
                'prev_x': prev_x,
                'prev_y': prev_y,
                'step_x': step_x,
                'step_y': step_y,
            }

        while animation:
            screen.fill((0, 0, 0))
            self.draw_connection(screen)
            self.draw_hub(screen, sim)
            self.draw_names(screen)

            for id, data in list(animation.items()):
                if data['prev_x'] != data['x']:
                    data['prev_x'] += data['step_x']
                if data['prev_y'] != data['y']:
                    data['prev_y'] += data['step_y']
                if abs(data['prev_x'] - data['x']) < 1 and abs(data['prev_y'] - data['y']) < 1:
                    data['prev_x'] = data['x']
                    data['prev_y'] = data['y']
                    animation.pop(id)
                    continue  

            for id, data in list(animation.items()):
                drone_position = self.drone_img.get_rect(center=(data['prev_x'], data['prev_y']))
                text = self.font.render(id, True, (255, 255, 255))
                text_position = text.get_rect(center=(data['prev_x'], data['prev_y'] - 75))
                screen.blit(text, text_position)
                screen.blit(self.drone_img, drone_position)

                if data['prev_x'] == data['x'] and data['prev_y'] == data['y']:
                    animation.pop(id)

            for drone in sim.drones:
                if drone.delivered:
                    continue
                if drone.id in animation:
                    continue
                hub = self.hubs[drone.position]
                px, py = self.to_pixels(hub)
                drone_position = self.drone_img.get_rect(center=(px, py))
                text = self.font.render(drone.id, True, (255, 255, 255))
                text_position = text.get_rect(center=(px, py - 75))
                screen.blit(text, text_position)
                screen.blit(self.drone_img, drone_position)

            pygame.display.flip()
            pygame.time.delay(2)


    def draw_score(self, screen: pygame.Surface, sim: Simulation) -> None:
        font = pygame.font.SysFont("Arial", 64, bold=True)
        y_pos = self.screen_height // 2
        text = font.render("All drones delivered!", True, (0, 192, 0))
        text_position = text.get_rect(center=(self.screen_width // 2, y_pos - 100))
        screen.blit(text, text_position)
        text = font.render("Total number of turns:", True, (255, 255, 255))
        text_position = text.get_rect(center=(self.screen_width // 2, y_pos))
        screen.blit(text, text_position)
        text = font.render(str(sim.turn), True, (255, 255, 255))
        text_position = text.get_rect(center=(self.screen_width // 2, y_pos + 100))
        screen.blit(text, text_position)

    def draw_start_screen(self, screen: pygame.Surface) -> None:
        font = pygame.font.SysFont("Arial", 55, bold=True)
        font2 = pygame.font.SysFont("Arial", 48, bold=True)
        y_pos = self.screen_height // 2
        text = font.render("For next turn press right arrow", True, (255, 255, 255))
        text_position = text.get_rect(center=(self.screen_width // 2, y_pos - 100))
        screen.blit(text, text_position)
        text = font2.render("To quit press q", True, (255, 255, 255))
        text_position = text.get_rect(center=(self.screen_width // 2, y_pos + 100))
        screen.blit(text, text_position)

def game_loop(sim: Simulation, hubs: dict[str, parser.Hub], connections: dict[frozenset[str], parser.Connection]) -> None:
    viz = Visualizer(hubs, connections)
    screen = pygame.display.set_mode((viz.screen_width, viz.screen_height))
    pygame.display.set_caption("Fly_in")
    clock = pygame.time.Clock()
    running = True
    viz.draw_start_screen(screen)
    pygame.display.flip()
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN and event.key == pygame.K_q:
                running = False
            if event.type == pygame.KEYDOWN and event.key == pygame.K_RIGHT:
                if not all(d.delivered for d in sim.drones):
                    moves = sim.step()
                    if moves:
                        for m in moves:
                            print(f"  {m}")           
                    screen.fill((0,0,0))
                    viz.draw_connection(screen)
                    viz.draw_hub(screen, sim)
                    viz.draw_names(screen)
                    viz.draw_drone(screen, sim)
                if all(d.delivered for d in sim.drones):
                    screen.fill((0,0,0))
                    viz.draw_score(screen, sim)
                pygame.display.flip()
                clock.tick(60)