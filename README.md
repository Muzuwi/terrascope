[icon]: terrascope/static/images/favicon.ico
# ![icon] Terrascope

A simple self-hosted, web-based Terraria world viewer and timelapser.
Example modification.

[present]: docs/present.png
![present]

# Features

- Automatically monitors the world directory for new worlds and updates to existing ones
- Generates world snapshots on change that can be viewed using a simple web interface
- Allows viewing all past and present world snapshots

# Running

The supported way of running Terrascope is using a Docker container.

> [!CAUTION]
> **SECURITY NOTICE: Terrascope is in heavy work-in-progress stage, do not expose it directly to the internet**.
> **There is currently no access control provided within Terrascope itself**.
> If you wish to expose Terrascope publicly, put it behind a reverse proxy of your choice (e.g Nginx, NginxProxyManager) with an external authorization server (e.g Authelia) to provide access control.

## Recommended: using docker-compose

For persistent deployments that will run alongside a Terraria server (constantly monitoring the server for world updates and providing up-to-date snapshots).

```yaml
services:
  terrascope:
    image: "muzuwi/terrascope:latest"
    restart: always
    command: run -h 0.0.0.0
    volumes:
      - data:/data
      - <path-to-your-worlds>:/worlds
    environment:
      TERRASCOPE_DATA_DIRECTORY: /data
      TERRASCOPE_WORLD_DIRECTORY: /worlds
      SQLALCHEMY_DATABASE_URI: sqlite:////data/terrascope.db
      SECRET_KEY: <replace-with-random-hex-string>
    ports:
      - 5000:5000

volumes:
  data:
```

Use the above template as a base for configuring the container in your Docker container management platform of choice ([Dockge](https://github.com/louislam/dockge), [Portainer](https://github.com/portainer/portainer/), etc.).

Or, if you're deploying this locally, save the above template as `docker-compose.yaml`, and then run with:

```yaml
docker-compose -f docker-compose.yaml up
```

Terrascope will be available at `http://127.0.0.1:5000/`.
> [!IMPORTANT]
> Please note that currently snapshots will only be created when a world is updated (i.e when the Terraria server saves the map) while Terrascope is running.
> As such, the snapshot menu will appear empty on first start.
> You can force an update by manually saving the world from the Terraria server console (or by `touch`ing the world file).

## Using `docker run`

For quick-and-dirty testing, you can use `docker run`.

```bash
sudo docker run \
    -p 5000:5000 \
    -v terrascope_data:/data \
    -v <path-to-your-worlds-directory>:/worlds \
    -e TERRASCOPE_DATA_DIRECTORY=/data \
    -e TERRASCOPE_WORLD_DIRECTORY=/worlds \
    -e SQLALCHEMY_DATABASE_URI=sqlite:////data/terrascope.db \
    -e SECRET_KEY=<replace-with-random-hex-string> \
    --rm -it muzuwi/terrascope:latest \
    run -h 0.0.0.0
```

Terrascope will be available at `http://127.0.0.1:5000/`.
> [!IMPORTANT]
> Please note that currently snapshots will only be created when a world is updated (i.e when the Terraria server saves the map) while Terrascope is running.
> As such, the snapshot menu will appear empty on first start.
> You can force an update by manually saving the world from the Terraria server console (or by `touch`ing the world file).

# License

This software is licensed under the AGPL-3.0 license.
For more information, consult the [LICENSE](./LICENSE) file.
