import pygame
from typing import Callable
from game_engine.helpers import Singleton


PyGame_EventType = int
ObjectId = int
class EventListenerInstance:
    def __init__(self):
        self.on_event_listener: dict[PyGame_EventType, dict[ObjectId, Callable]] = {}

    def update(self, event_type: PyGame_EventType, object_id: ObjectId, callback: Callable):
        if event_type not in self.on_event_listener:
            self.on_event_listener[event_type] = {}
        # Check if callback have 1 argument
        if len(callback.__code__.co_varnames) != 2:
            raise ValueError("Callback must have 1 argument")
        self.on_event_listener[event_type][object_id] = callback

    def remove(self, object_id: ObjectId):
        for event_type in self.on_event_listener:
            if object_id in self.on_event_listener[event_type]:
                del self.on_event_listener[event_type][object_id]

    def get(self, event_type: PyGame_EventType):
        if event_type in self.on_event_listener:
            return self.on_event_listener[event_type]
        return {}


@Singleton[EventListenerInstance]
class EventListener(EventListenerInstance):
    pass
