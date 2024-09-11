import os
import pathlib
import logging
from watchdog.observers import Observer
from watchdog.events import (
    FileSystemEventHandler,
    FileModifiedEvent,
    FileCreatedEvent,
    DirModifiedEvent,
    DirCreatedEvent,
)
from flask import Flask
from threading import Timer
from typing import Callable
import atexit


logger = logging.getLogger()


class __WorldFileEventHandler(FileSystemEventHandler):
    """Listener for .wld file creation/modifications on the filesystem"""

    def __init__(
        self,
        directory: str,
        callback: Callable[[pathlib.Path], None],
        idle_time: float = 5.0,
    ):
        super().__init__()
        self.modified_files = {}
        self.base_directory = directory
        self.callback = callback
        self.idle_time = idle_time

    def is_world_file_event(
        self,
        event: (
            DirModifiedEvent | FileModifiedEvent | DirCreatedEvent | FileCreatedEvent
        ),
    ):
        return not event.is_directory and pathlib.Path(event.src_path).suffix == ".wld"

    def on_modified(self, event):
        if self.is_world_file_event(event):
            self.schedule_processing(event.src_path)

    def on_created(self, event):
        if self.is_world_file_event(event):
            self.schedule_processing(event.src_path)

    def schedule_processing(self, file_path):
        if file_path in self.modified_files:
            self.modified_files[file_path].cancel()

        timer = Timer(self.idle_time, self.process_world, [file_path])
        self.modified_files[file_path] = timer
        timer.start()

    def process_world(self, file_path):
        del self.modified_files[file_path]

        logger.info(f"WLD file idle, calling callback for: {file_path}")
        self.callback(pathlib.Path(os.path.join(self.base_directory, file_path)))


def init(app: Flask, callback: Callable[[pathlib.Path], None]):
    global __observer

    logger.info(
        f"Starting world event listener in directory: {app.config['TERRASCOPE_WORLD_DIRECTORY']}"
    )
    event_handler = __WorldFileEventHandler(
        directory=app.config["TERRASCOPE_WORLD_DIRECTORY"], callback=callback
    )
    __observer = Observer()
    __observer.schedule(
        event_handler, app.config["TERRASCOPE_WORLD_DIRECTORY"], recursive=False
    )
    try:
        __observer.start()
    except Exception as e:
        logger.error("Failed to start the world observer!", exc_info=e)
        logger.error(
            "This may be due to the wrong directory being set. Please verify the configured world location."
        )
        return
    atexit.register(lambda: __observer.stop())
