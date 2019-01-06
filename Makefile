IDIR = /usr/local/bin

blank:
	@echo "\`make build\` to build from source code ( Requires Golang Utilities )"
	@echo "\`sudo make install\` to install app"

build: main.go
	go build main.go
	@mv main ./bin/das

install: ./bin/das
	@sudo cp ./bin/das $(IDIR)
	@echo "Installed Successfully."
	
remove: ./bin/das
	@sudo rm $(IDIR)/das
	@echo "Uninstalled Successfully."
