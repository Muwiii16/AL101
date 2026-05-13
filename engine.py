import heapq
from collections import deque
from dataclasses import dataclass, field
from typing import Optional
from datetime import datetime
import uuid

LRT1_STATIONS = [
    "Fernando Poe Jr.", "Balintawak", "Monumento", "5th Avenue",
    "R. Papa", "Abad Santos", "Blumentritt", "Tayuman", "Bambang",
    "Doroteo Jose", "Carriedo", "Central Terminal", "United Nations",
    "Pedro Gil", "Quirino", "Vito Cruz", "Gil Puyat", "Libertad",
    "EDSA", "Baclaran"
]

LRT2_STATIONS = [
    "Antipolo", "Marikina", "Santolan", "Katipunan", "Anonas",
    "Cubao", "Betty Go-Belmonte", "Gilmore", "J. Ruiz",
    "V. Mapa", "Pureza", "Legarda", "Recto"
]

MRT3_STATIONS = [
    "North Avenue", "Quezon Avenue", "GMA-Kamuning", "Araneta-Cubao",
    "Santolan-Annapolis", "Ortigas", "Shaw Boulevard", "Boni",
    "Guadalupe", "Buendia", "Ayala", "Magallanes", "Taft Avenue"
]

LINES = {
    "LRT1": LRT1_STATIONS,
    "LRT2": LRT2_STATIONS,
    "MRT3": MRT3_STATIONS
}


def build_graph(stations: list[str]) -> dict[str, dict[str, int]]:
    graph = dict[str, dict[str, int]] = {s: {} for s in stations}
    for i in range(len(stations) - 1):
        a, b = stations[i], stations[i + 1]
        graph[a][b] = 1
        graph[b][a] = 1
    return graph


LINE_GRAPHS = dict[str, dict[str, dict[str, int]]] = {
    line: build_graph(stations) for line, stations in LINES.items()}


def dijkstra(graph: dict, origin: str, destination: str) -> tuple[int, list[str]]:

    dist = {node: float('inf') for node in graph}
    prev: dict[str, Optional[str]] = {node: None for node in graph}
    dist[origin] = 0
    heap: list[tuple[int, str]] = [(0, origin)]

    while heap:
        current_dist, u = heapq.heappop(heap)
        if current_dist > dist[u]:
            continue
        for neighbor, weight in graph[u].items():
            alt = dist[u]+weight
            if alt < dist[neighbor]:
                dist[neighbor] = alt
                prev[neighbor] = u
                heapq.heappush(heap, (alt, neighbor))

    path: list[str] = []
    node: Optional[str] = destination
    while node is not None:
        path.append(node)
        node = prev[node]
    path.reverse()

    stops = dist[destination]
    return (int(stops) if stops != float('inf')else -1, path)


BOARDING_ZONES = {
    "ZONE A — Door 1 (Interior)":  "Long trip (≥7 stops). Board first, move deep into carriage.",
    "ZONE B — Door 2 (Middle)":    "Medium trip (4–6 stops). Board second, stand mid-carriage.",
    "ZONE C — Door 3 (Near Exit)": "Short trip (1–3 stops). Board last, stay near doors.",
}


def get_zone(stops: int) -> tuple[str, str]:
    if stops >= 7:
        zone = "ZONE A — Door 1 (Interior)"
    elif stops >= 4:
        zone = "ZONE B — Door 2 (Middle)"
    else:
        zone = "ZONE C — Door 3 (Near Exit)"
    return zone, BOARDING_ZONES[zone]


@dataclass(order=True)
class Passenger:

    priority: int
    stops: int = field(compare=False)
    passenger_id: str = field(compare=False)
    name: str = field(compare=False)
    origin: str = field(compare=False)
    destination: str = field(compare=False)
    line: str = field(compare=False)
    path: list[str] = field(compare=False, default_factory=list)
    zone: str = field(compare=False, default="")
    zone_desc: str = field(compare=False, default="")
    timestamp: str = field(compare=False, default="")
    status: str = field(compare=False, default="On Platform")


class PlatformQueue:
    """Standard FIFO queue representing passengers waiting on the platform."""

    def __init__(self):
        self._queue: deque[Passenger] = deque()

    def enqueue(self, p: Passenger):
        self._queue.append(p)

    def dequeue(self) -> Optional[Passenger]:
        return self._queue.popleft() if self._queue else None

    def peek(self) -> Optional[Passenger]:
        return self._queue[0] if self._queue else None

    def size(self) -> int:
        return len(self._queue)

    def all(self) -> list[Passenger]:
        return list(self._queue)

    def clear(self):
        self._queue.clear()


class BoardingPriorityQueue:
    """
    Priority Queue where highest-stop passengers board first.
    Implements the 'Destination Grouping' concept from the paper.
    """

    def __init__(self):
        self._heap: list[Passenger] = []

    def push(self, p: Passenger):
        heapq.heappush(self._heap, p)

    def pop(self) -> Optional[Passenger]:
        return heapq.heappop(self._heap) if self._heap else None

    def peek(self) -> Optional[Passenger]:
        return self._heap[0] if self._heap else None

    def size(self) -> int:
        return len(self._heap)

    def all(self) -> list[Passenger]:
        return sorted(self._heap)   # sorted by priority (boarding order)

    def clear(self):
        self._heap.clear()


class TrainCarStack:
    """
    Simulates the unmanaged LIFO 'Stack' problem described in the paper.
    The last person to board blocks everyone behind them from exiting.
    """

    def __init__(self, capacity: int = 20):
        self._stack: list[Passenger] = []
        self.capacity = capacity

    def push(self, p: Passenger) -> bool:
        if len(self._stack) >= self.capacity:
            return False
        self._stack.append(p)
        p.status = "Boarded"
        return True

    def pop(self) -> Optional[Passenger]:
        if self._stack:
            p = self._stack.pop()
            p.status = "Alighted"
            return p
        return None

    def peek(self) -> Optional[Passenger]:
        return self._stack[-1] if self._stack else None

    def size(self) -> int:
        return len(self._stack)

    def is_full(self) -> bool:
        return len(self._stack) >= self.capacity

    def all(self) -> list[Passenger]:
        return list(reversed(self._stack))   # top of stack first

    def clear(self):
        self._stack.clear()


class TransitSystem:
    """
    Orchestrates all data structures and provides the main API
    consumed by the Flet frontend.
    """

    # for priority inversion
    MAX_STOPS = max(len(s) - 1 for s in LINES.values())

    def __init__(self):
        self.platform_queue = PlatformQueue()
        self.boarding_queue = BoardingPriorityQueue()
        self.train_car = TrainCarStack(capacity=20)
        self.history: list[Passenger] = []
        self.total_registered = 0
        self.total_boarded = 0
        self.total_alighted = 0

    def register_passenger(
        self,
        name: str,
        line: str,
        origin: str,
        destination: str,
    ) -> tuple[bool, str, Optional[Passenger]]:
        """
        Register a passenger:
        1. Run Dijkstra to get stop count & path.
        2. Compute priority score (inverted stops).
        3. Assign boarding zone.
        4. Enqueue on platform (FIFO arrival order).
        5. Push to priority boarding queue.
        """
        if line not in LINE_GRAPHS:
            return False, f"Unknown line: {line}", None

        graph = LINE_GRAPHS[line]

        if origin not in graph:
            return False, f"Station '{origin}' not found on {line}.", None
        if destination not in graph:
            return False, f"Station '{destination}' not found on {line}.", None
        if origin == destination:
            return False, "Origin and destination cannot be the same.", None

        stops, path = dijkstra(graph, origin, destination)
        if stops == -1:
            return False, "No path found between the selected stations.", None

        priority = self.MAX_STOPS - stops
        zone, zone_desc = get_zone(stops)

        passenger = Passenger(
            priority=priority,
            stops=stops,
            passenger_id=str(uuid.uuid4())[:8].upper(),
            name=name.strip() or "Passenger",
            origin=origin,
            destination=destination,
            line=line,
            path=path,
            zone=zone,
            zone_desc=zone_desc,
            timestamp=datetime.now().strftime("%H:%M:%S"),
            status="On Platform",
        )

        self.platform_queue.enqueue(passenger)
        self.boarding_queue.push(passenger)
        self.history.append(passenger)
        self.total_registered += 1

        return True, "Passenger registered successfully.", passenger

    def board_next(self) -> tuple[bool, str, Optional[Passenger]]:
        """
        Board the next passenger from the priority queue (not the FIFO platform queue).
        This is the 'Destination Grouping' optimized boarding.
        """
        if self.boarding_queue.size() == 0:
            return False, "No passengers waiting to board.", None
        if self.train_car.is_full():
            return False, "Train car is at full capacity.", None

        passenger = self.boarding_queue.pop()
        self.train_car.push(passenger)
        self.total_boarded += 1
        return True, f"{passenger.name} boarded → assigned to {passenger.zone}.", passenger

    def board_all(self) -> tuple[int, list[Passenger]]:
        """Board all queued passengers in priority order."""
        boarded = []
        while self.boarding_queue.size() > 0 and not self.train_car.is_full():
            ok, _, p = self.board_next()
            if ok and p:
                boarded.append(p)
        return len(boarded), boarded

    def alight_next(self) -> tuple[bool, str, Optional[Passenger]]:
        """
        Remove passenger from the top of the train stack (LIFO simulation).
        In the managed system this represents the person nearest the door exiting.
        """
        if self.train_car.size() == 0:
            return False, "Train car is empty.", None

        passenger = self.train_car.pop()
        self.total_alighted += 1
        return True, f"{passenger.name} alighted at {passenger.destination}.", passenger

    def reset(self):
        self.platform_queue.clear()
        self.boarding_queue.clear()
        self.train_car.clear()
        self.history.clear()
        self.total_registered = 0
        self.total_boarded = 0
        self.total_alighted = 0

    def get_stats(self) -> dict:
        return {
            "on_platform": self.platform_queue.size(),
            "in_boarding_queue": self.boarding_queue.size(),
            "in_train": self.train_car.size(),
            "train_capacity": self.train_car.capacity,
            "total_registered": self.total_registered,
            "total_boarded": self.total_boarded,
            "total_alighted": self.total_alighted,
            "efficiency": round(
                (self.total_alighted / self.total_boarded *
                 100) if self.total_boarded else 0, 1
            ),
        }
