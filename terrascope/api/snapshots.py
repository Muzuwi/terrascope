from typing import Iterable
from flask import Blueprint, abort, current_app, send_from_directory
from sqlalchemy import select

from terrascope.model.snapshot import WorldSnapshot
from ..db import getdb

blueprint = Blueprint("snapshots-api", __name__)


@blueprint.route("/api/v1/snapshots")
def get_snapshots():
    snapshots: Iterable[WorldSnapshot] = getdb().session.query(WorldSnapshot).all()
    return [
        {
            "id": s.id,
            "cause": s.cause,
            "world_name": s.world_name,
            "snapshot_name": s.snapshot_filename,
            "timestamp": s.timestamp,
        }
        for s in snapshots
    ]


@blueprint.route("/api/v1/snapshot/<int:id>/image")
def send_image(id: int):
    snapshot = (
        getdb()
        .session.execute(select(WorldSnapshot).where(WorldSnapshot.id == id))
        .scalar()
    )
    if snapshot is None:
        abort(404)

    return send_from_directory(
        current_app.config["TERRASCOPE_DATA_DIRECTORY"],
        snapshot.snapshot_filename,
    )


@blueprint.route("/api/v1/snapshot/<int:id>")
def get_snapshot(id: int):
    snapshot = (
        getdb()
        .session.execute(select(WorldSnapshot).where(WorldSnapshot.id == id))
        .scalar()
    )
    if snapshot is None:
        abort(404)

    return {
        "id": snapshot.id,
        "cause": snapshot.cause,
        "world_name": snapshot.world_name,
        "snapshot_name": snapshot.snapshot_filename,
        "timestamp": snapshot.timestamp,
    }
