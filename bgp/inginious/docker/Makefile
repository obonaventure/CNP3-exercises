all: build run

build:
	docker build -t inginious-c-qemu ./

run:
	docker run -t -i --rm inginious-c-qemu /bin/bash

clean:
	docker rmi inginious-c-qemu

rmproper: clean
	docker rmi $$(docker images -q)
