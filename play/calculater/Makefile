# 定义变量
CC=gcc
CFLAGS=-Wall
LDFLAGS=

BINDIR = bin

SOURCES = ./src/*

OBJECTS = $(SOURCES:%.c=$(BINDIR)/%.o)

EXE = myprogram

all: $(BINDIR)/$(EXE)

$(BINDIR)/%.o: %.c
	$(CC) $(LDFLAGS) -c $^ -o $@

$(BINDIR)/$(EXE): $(OBJECTS)
	$(CC) $(LDFLAGS) $^ -g -o $@

#.PHONY: run
#run: myprogram
#	./bin/myprogram

#.PHONY: clean
#clean:
#   rm -f /bin *.o