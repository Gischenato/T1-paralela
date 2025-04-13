CC = gcc
CFLAGS = -Wall -Wextra -O2
TARGET2 = n_queens
SRC2 = n_queens.c
TARGET3 = n_queens_threads
SRC3 = n_queens_threads.c

all: $(TARGET) $(TARGET2) $(TARGET3)

$(TARGET2): $(SRC2)
	$(CC) $(CFLAGS) -o $@ $<

$(TARGET3): $(SRC3)
	$(CC) $(CFLAGS) -fopenmp -o $@ $<

clean:
	rm -f $(TARGET) $(TARGET).exe $(TARGET2) $(TARGET2).exe

run:
	./$(TARGET) 8

run_queens:
	./$(TARGET2) 8

.PHONY: all clean run run_queens
