.PHONY: base
base:
	pip3 install --user websockets requests tomlkit
.PHONY: extras
extras:
	pip3 install --user bs4 python_anticaptcha isodate
.PHONY: webcam
webcam:
	pip3 install --user aioice aiortc
.PHONY: baseextras
baseextras: base extras
.PHONY: all
all: baseextras webcam
