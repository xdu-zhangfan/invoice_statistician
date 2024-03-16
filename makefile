SRC_FILE = invoice_statistician

all: $(SRC_FILE).py
	pyinstaller --onefile $(SRC_FILE).py
	mv ./dist/$(SRC_FILE) ./
	rm -rf ./build ./dist ./$(SRC_FILE).spec

.PHONY:clean
clean:
	rm -rf ./$(SRC_FILE)
