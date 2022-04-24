import pygame
from typing import Callable
from game_engine.helpers import Singleton


PyGame_EventType = int
class EventListenerInstance:
    def __init__(self):
        self.event_listener: dict[PyGame_EventType, dict[int, Callable]] = {}
        self._remove_queue: dict[PyGame_EventType, list[int]] = {}
        self._add_queue: dict[PyGame_EventType, dict[int, Callable]] = {}

    def update(self, event_type: PyGame_EventType, obj:object, callback: Callable):
        # Check if callback have 1 argument
        if len(callback.__code__.co_varnames) != 2:
            raise ValueError("Callback must have 1 argument")
        if event_type not in self.event_listener:
            self.event_listener[event_type] = {}
        elif id(obj) in self.event_listener[event_type]:
            self.event_listener[event_type][id(obj)] = callback
        else:
            self._add_queue[event_type][id(obj)] = callback
        self.event_listener[event_type][id(obj)] = callback

    def remove(self, obj:object):
        for event_type in self.event_listener:
            if id(obj) in self.event_listener[event_type]:
                if event_type not in self._remove_queue:
                    self._remove_queue[event_type] = []
                self._remove_queue[event_type].append(id(obj))


    def get(self, event_type: PyGame_EventType):
        # Append add queue to on_event_listener
        for add_type in self._add_queue:
            self.event_listener[add_type].update(self._add_queue[add_type])
        self._add_queue = {}
        # Remove remove queue from on_event_listener
        for remove_type in self._remove_queue:
            for id_to_remove in self._remove_queue[remove_type]:
                self.event_listener[remove_type].pop(id_to_remove)
        self._remove_queue = {}
        if event_type in self.event_listener:
            return self.event_listener[event_type]
        return {}


@Singleton[EventListenerInstance]
class EventListener(EventListenerInstance):
    pass
