DOCKER_IMAGE_TAG := muzuwi/terrascope
DOCKER_IMAGE_VER := latest
DOCKER_IMAGE_TAG_FULL := ${DOCKER_IMAGE_TAG}:${DOCKER_IMAGE_VER}

default: docker-image

docker-image:
	docker build -f deploy/Dockerfile -t "${DOCKER_IMAGE_TAG_FULL}" .
