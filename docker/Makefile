VERSION ?= 0.2.0
FULLVERSION ?= ${VERSION}
archs = s390x arm32v7 amd64 i386 arm64v8 arm32v6

.PHONY: all build latest
latest: build
	FULLVERSION=latest VERSION=${VERSION} make build
build:
	cp /usr/bin/qemu-*-static .
	$(foreach arch,$(archs), \
		cat Dockerfile | sed "s/FROM python:alpine/FROM ${arch}\/python:alpine/g" > .Dockerfile; \
		docker build -t torrench:${VERSION}-$(arch) -f .Dockerfile .;\
	)
