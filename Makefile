SHELL := /bin/bash

LIZ_HOME = ~/.liz

build: configure.py launch.py
	if [ ! -d $(LIZ_HOME) ]; then\
		mkdir $(LIZ_HOME);\
	fi
	python configure.py
	pyinstaller --onefile launch.py


install:
	mv dist/launch /usr/local/bin/liz
