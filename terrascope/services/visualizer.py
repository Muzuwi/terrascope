import os
import pathlib
import logging
import datetime
import time
from subprocess import check_call
from flask import Flask
from sqlalchemy.orm import Session
from threading import Thread
import queue

from terrascope.model.snapshot import WorldSnapshot
from ..db import getdb


logger = logging.getLogger()
__jobqueue = queue.Queue(4)


def get_snapshot_directory() -> pathlib.Path:
    from flask import current_app

    return pathlib.Path(current_app.config["TERRASCOPE_DATA_DIRECTORY"])


def visualize(world: pathlib.Path):
    logger.info(f"Queueing visualization for world: {world}")
    timestamp = datetime.datetime.now(datetime.timezone.utc)
    job = (world, timestamp)
    __jobqueue.put(job)


def __visualizer_loop():
    while True:
        world: pathlib.Path
        timestamp: datetime.datetime
        world, timestamp = __jobqueue.get(block=True)

        # Append timestamp to the output filename
        worldname = world.stem
        timestamp_iso8601 = timestamp.isoformat()
        output_name = f"{worldname}-{timestamp_iso8601}.png"
        output_file = pathlib.Path(get_snapshot_directory(), output_name)
        if not os.path.isdir(get_snapshot_directory()):
            os.mkdir(get_snapshot_directory())

        # Call flyingsnake to do the visualization for us
        args = ["flyingsnake", str(world.absolute()), str(output_file.absolute())]

        logger.info(f"Worker: calling {' '.join(args)}")
        start = time.time_ns()
        check_call(args)
        dur = (time.time_ns() - start) // 1_000_000
        logger.info(f"Worker: visualization completed, took {dur}ms")

        snapshot = WorldSnapshot()
        snapshot.world_name = worldname
        snapshot.timestamp = timestamp
        snapshot.cause = "explicitly requested"
        snapshot.snapshot_filename = output_name
        getdb().session.add(snapshot)
        getdb().session.commit()


def __visualizer_main(app: Flask):
    with app.app_context():
        __visualizer_loop()


def init(app: Flask):
    Thread(target=__visualizer_main, args=(app,)).start()
