DOCKER_IMAGE_TAG := muzuwi/terrascope
DOCKER_IMAGE_VER := latest
DOCKER_IMAGE_TAG_FULL := ${DOCKER_IMAGE_TAG}:${DOCKER_IMAGE_VER}

default: docker-image

docker-image:
	docker build -f deploy/Dockerfile -t "${DOCKER_IMAGE_TAG_FULL}" .


push-image:
	@[ ! -z "${REGISTRY}" ] || (echo "REGISTRY variable not specified, don't know where to push.." ; exit 1)
	docker image tag ${DOCKER_IMAGE_TAG_FULL} ${REGISTRY}/${DOCKER_IMAGE_TAG_FULL}
	docker push ${REGISTRY}/${DOCKER_IMAGE_TAG_FULL}
