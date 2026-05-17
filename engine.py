import heapq
from collections import deque
from dataclasses import dataclass, field
from typing import Optional
from datetime import datetime
import uuid
import math

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
    "LRT-1": LRT1_STATIONS,
    "LRT-2": LRT2_STATIONS,
    "MRT-3": MRT3_STATIONS
}

LRT1_WEIGHTS = [2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2]
LRT2_WEIGHTS = [3, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2]
MRT3_WEIGHTS = [2, 2, 3, 2, 2, 2, 2, 2, 2, 2, 2, 2]

LINE_WEIGHTS = {
    "LRT-1": LRT1_WEIGHTS,
    "LRT-2": LRT2_WEIGHTS,
    "MRT-3": MRT3_WEIGHTS,
}


def build_graph(stations, weights):
    graph = {}
    for s in stations:
        graph[s] = {}

    for i in range(len(stations)-1):
        a = stations[i]
        b = stations[i+1]
        w = weights[i]
        graph[a][b] = w
        graph[b][a] = w
    return graph


LINE_GRAPHS = {
    line: build_graph(stations, LINE_WEIGHTS[line]) for line, stations in LINES.items()
}


def dijkstra(graph, origin, destination):
    dist = {}
    for node in graph:
        dist[node] = float('inf')
    dist[origin] = 0

    prev = {}
    for node in graph:
        prev[node] = None

    heap = [(0, origin)]

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

    path = []
    node = destination
    while node is not None:
        path.append(node)
        node = prev[node]
    path.reverse()

    stops = dist[destination]
    if stops == float('inf'):
        return -1, []
    return stops, path


BOARDING_ZONES = {
    "ZONE A - DOOR 1": "Long trip (≥ 10 stops). Board through Door 1.",
    "ZONE B - DOOR 2": "Medium-long trip (6-9 stops). Board through Door 2.",
    "ZONE C - DOOR 3": "Medium trip (3-5 stops). Board through Door 3.",
    "ZONE D - DOOR 4": "Short trip (1-2 stops). Board through Door 4."
}

ZONE_RANGES = {
    "ZONE A - DOOR 1": (10, float('inf')),
    "ZONE B - DOOR 2": (6, 9),
    "ZONE C - DOOR 3": (3, 5),
    "ZONE D - DOOR 4": (1, 2)
}


def get_zone(stops):
    if stops >= 10:
        zone = "ZONE A - DOOR 1"
    elif stops >= 6:
        zone = "ZONE B - DOOR 2"
    elif stops >= 3:
        zone = "ZONE C - DOOR 3"
    else:
        zone = "ZONE D - DOOR 4"
    return zone, BOARDING_ZONES[zone]


def get_position_label(position, total):
    if total == 1:
        return "Center"
    if total == 2:
        if position == 1:
            return 'Far Back'
        else:
            return 'Near Door'

    third = total/3

    if position <= math.ceil(third):
        return "Far Back"
    elif position <= math.ceil(third*2):
        return "Middle"
    else:
        return "Near Door"


@dataclass(order=True)
class Passenger:
    priority: int

    stops: int = field(compare=False)
    passenger_id: str = field(compare=False)
    name: str = field(compare=False)
    line: str = field(compare=False)
    origin: str = field(compare=False)
    destination: str = field(compare=False)
    zone: str = field(compare=False, default="")
    zone_desc: str = field(compare=False, default="")
    position: int = field(compare=False, default=0)
    position_label: str = field(compare=False, default="")
    path: list = field(compare=False, default_factory=list)
    timestamp: str = field(compare=False, default="")
    status: str = field(compare=False, default="On Platform")
    car_number: int = field(compare=False, default=0)


class PlatformQueue:

    def __init__(self):
        self._queue = deque()

    def enqueue(self, passenger):
        self._queue.append(passenger)

    def dequeue(self):
        if self._queue:
            return self._queue.popleft()
        return None

    def peek(self):
        if self._queue:
            return self._queue[0]
        return None

    def size(self):
        return len(self._queue)

    def all(self):
        return list(self._queue)

    def clear(self):
        self._queue.clear()

    def remove(self, passenger_id):
        self._queue = deque(
            p for p in self._queue
            if p.passenger_id != passenger_id
        )


class BoardingPriorityQueue:
    def __init__(self):
        self._heap = []

    def push(self, passenger):
        heapq.heappush(self._heap, passenger)

    def pop(self):
        if self._heap:
            return heapq.heappop(self._heap)
        return None

    def peek(self):
        if self._heap:
            return self._heap[0]
        return None

    def size(self):
        return len(self._heap)

    def all(self):
        return sorted(self._heap)

    def clear(self):
        self._heap.clear()


class TrainCar:

    def __init__(self, car_number, capacity=50):
        self.car_number = car_number
        self.capacity = capacity

        self.zones = {
            "ZONE A - DOOR 1": [],
            "ZONE B - DOOR 2": [],
            "ZONE C - DOOR 3": [],
            "ZONE D - DOOR 4": []
        }

    def board(self, passenger):
        if self.total_passengers() >= self.capacity:
            return False

        self.zones[passenger.zone].append(passenger)

        self.zones[passenger.zone].sort(
            key=lambda p: LINES[p.line].index(p.destination), reverse=True)

        zone_passengers = self.zones[passenger.zone]
        total = len(zone_passengers)
        for i, p in enumerate(zone_passengers):
            p.position = i+1
            p.position_label = get_position_label(i+1, total)

        passenger.status = "Boarded"
        passenger.car_number = self.car_number
        return True

    def alight(self, passenger_id):
        for zone, zone_list in self.zones.items():
            for p in zone_list:
                if p.passenger_id == passenger_id:
                    zone_list.remove(p)
                    p.status = "Alighted"

                    total = len(zone_list)
                    for i, remaining in enumerate(zone_list):
                        remaining.position = i+1
                        remaining.position_label = get_position_label(
                            i+1, total)
                    return p
        return None

    def total_passengers(self):
        return sum(len(zone) for zone in self.zones.values())

    def is_full(self):
        return self.total_passengers() >= self.capacity

    def get_zone_passenger(self, zone):
        return self.zones[zone]

    def all(self):
        result = []
        for zone_list in self.zones.values():
            result.extend(zone_list)
        return result

    def clear(self):
        for zone in self.zones:
            self.zones[zone] = []


class Train:
    def __init__(self, cars=5, capacity_per_car=10):
        self.cars = [TrainCar(i+1, capacity_per_car) for i in range(cars)]

    def get_least_loaded_car(self):
        available = [car for car in self.cars if not car.is_full()]
        if not available:
            return None
        return min(available, key=lambda car: car.total_passengers())

    def board(self, passenger):
        car = self.get_least_loaded_car()
        if car is None:
            return False, "Train is full"
        success = car.board(passenger)
        if success:
            return True, f'{passenger.name} boarder Car {car.car_number} - {passenger.zone}'
        return False, "Could not board passenger"

    def alight(self, passenger_id):
        for car in self.cars:
            result = car.alight(passenger_id)
            if result:
                return True, f'{result.name} alighted at {result.destination}', result
        return False, 'Passenger not found', None

    def total_passengers(self):
        return sum(car.total_passengers() for car in self.cars)

    def is_full(self):
        return all(car.is_full() for car in self.cars)

    def clear(self):
        for car in self.cars:
            car.clear()


class TransitSystem:
    MAX_STOPS = max(len(stations)-1 for stations in LINES.values())

    def __init__(self):
        self.platform_queue = PlatformQueue()
        self.boarding_queue = BoardingPriorityQueue()
        self.train = Train(cars=5, capacity_per_car=10)
        self.history = []
        self.total_registered = 0
        self.total_boarded = 0
        self.total_alighted = 0

    def register_passenger(self, name, line, origin, destination):

        if line not in LINE_GRAPHS:
            return False, "Unknown transit line.", None

        graph = LINE_GRAPHS[line]

        if origin not in graph:
            return False, f'Stations "{origin}" not found on {line}.', None
        if destination not in graph:
            return False, f'Stations "{destination}" not found on {line}.', None
        if origin == destination:
            return False, "Origin and destination cannot be the same.", None

        stops, path = dijkstra(graph, origin, destination)
        if stops == -1:
            return False, "No valid path between origin and destination.", None

        zone, zone_desc = get_zone(stops)

        priority = self.MAX_STOPS - stops

        passenger = Passenger(
            priority=priority,
            stops=stops,
            passenger_id=str(uuid.uuid4())[:8].upper(),
            name=name.strip() or "Passenger",
            line=line,
            origin=origin,
            destination=destination,
            path=path,
            zone=zone,
            zone_desc=zone_desc,
            timestamp=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            status='On Platform'
        )

        self.platform_queue.enqueue(passenger)
        self.boarding_queue.push(passenger)
        self.history.append(passenger)
        self.total_registered += 1

        return True, 'Passenger registered successfully.', passenger

    def board_next(self):
        if self.boarding_queue.size() == 0:
            return False, 'No passengers waiting to board.', None
        if self.train.is_full():
            return False, 'Train is full.', None

        passenger = self.boarding_queue.pop()
        success, msg = self.train.board(passenger)

        if success:
            self.total_boarded += 1
            self.platform_queue.remove(passenger.passenger_id)
            return True, msg, passenger
        return False, msg, None

    def board_all(self):
        boarded = []
        while self.boarding_queue.size() > 0 and not self.train.is_full():
            ok, _, p = self.board_next()
            if ok and p:
                boarded.append(p)
        return len(boarded), boarded

    def alight_passenger(self, passenger_id):
        ok, msg, passenger = self.train.alight(passenger_id)
        if ok:
            self.total_alighted += 1
        return ok, msg, passenger

    def get_stats(self):
        return {
            'on_platform': self.platform_queue.size(),
            'in_boarding_queue': self.boarding_queue.size(),
            'total_in_train': self.train.total_passengers(),
            'total_registered': self.total_registered,
            'total_boarded': self.total_boarded,
            'total_alighted': self.total_alighted
        }

    def get_car_summary(self):
        return {
            f'Car {car.car_number}': car.total_passengers()
            for car in self.train.cars
        }

    def reset_system(self):
        self.platform_queue.clear()
        self.boarding_queue.clear()
        self.train.clear()
        self.history.clear()
        self.total_registered = 0
        self.total_boarded = 0
        self.total_alighted = 0

    def arrive_at_station(self, station_name):
        alighted = []

        for car in self.train.cars:
            for zone_list in car.zones.values():
                to_remove = [
                    p for p in zone_list
                    if p.destination == station_name
                ]
                for p in to_remove:
                    zone_list.remove(p)
                    p.status = 'Alighted'
                    self.total_alighted += 1
                    alighted.append(p)

                total = len(zone_list)
                for i, remaining in enumerate(zone_list):
                    remaining.position = i+1
                    remaining.position_label = get_position_label(i+1, total)
        return alighted
