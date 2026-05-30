CC = gcc
CFLAGS = -Wall -fPIC -shared
LIBS = -lpam
TARGET = pam_hyprface.so
SOURCE = pam_hyprface.c

all: $(TARGET)

$(TARGET): $(SOURCE)
	$(CC) $(CFLAGS) -o $(TARGET) $(SOURCE) $(LIBS)

clean:
	rm -f $(TARGET)