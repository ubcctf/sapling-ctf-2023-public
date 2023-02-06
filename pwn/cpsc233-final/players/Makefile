EXE = cpsc233_final
CC = gcc
CFLAG = 
PLAYER_FILES = starter.py main.c
HOST_FILES = flag.txt
SOLVE_FILES = 
PLAYER_DIR = static
HOST_DIR = deployment

chall:
	$(CC) $(CFLAG) src/main.c -o $(EXE)
	python src/patch.py
	echo "flag{test_flag_lol}" > flag.txt

players: chall
	mkdir -p $(PLAYER_DIR)
	cp $(EXE) $(PLAYER_DIR)/$(EXE)
	for u in $(PLAYER_FILES); do cp -f src/$$u $(PLAYER_DIR)/$$u; done

host: chall
	mkdir -p $(HOST_DIR)
	cp $(EXE) $(HOST_DIR)/$(EXE)
	for u in $(HOST_FILES); do cp -f src/$$u $(HOST_DIR)/$$u; done

solve: chall
	mkdir -p solve
	for u in $(SOLVE_FILES); do cp -f src/$$u solve/$$u; done

clear:
	rm -f $(EXE) flag.txt

clean: clear
	rm -rf $(PLAYER_DIR) $(HOST_DIR) solve

all: players host solve clear
.PHONY: chall player host solve all clean clear