// patryk_rybak 333139
#include <assert.h>
#include <stdio.h>
#include <stdlib.h>
#include <arpa/inet.h>
#include <unistd.h>

#include <netinet/ip_icmp.h>
#include <poll.h>
#include <errno.h>
#include <sys/time.h>
#include <string.h>

#define MAX_TTL 30
#define MAX_PACKET_SIZE 100
#define MAX_WAIT_TIME 1000

u_int16_t compute_icmp_checksum(const void *buff, int length);

void prepare_header(struct icmp* header, int ttl, u_int16_t id);

void send_packets(int fd, struct icmp* header, struct sockaddr_in* dest_addr);

int is_unique(char tab[][20], int last);

double calculate_elapsed_ms(struct timeval *start, struct timeval *end);

void process_icmp_packet(struct icmp* icmp_header, struct sockaddr_in* sender_addr,
                         char senders_ip[][20], int *unique, struct timeval *start_time,
                         double *elapsed_times, int *received, int id, int ttl);

