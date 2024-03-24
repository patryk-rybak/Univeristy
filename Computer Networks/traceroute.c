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

u_int16_t compute_icmp_checksum(const void *buff, int length) {
	const u_int16_t* ptr = buff;
	u_int32_t sum = 0;
	assert (length % 2 == 0);
	for (; length > 0; length -= 2)
		sum += *ptr++;
	sum = (sum >> 16U) + (sum & 0xffffU);
	return (u_int16_t)(~(sum + (sum >> 16U)));
}

void prepare_header(struct icmp* header, int ttl, u_int16_t id ) {
	bzero(header, sizeof(*header)); // czy to jest potrzebne to zerowoanie wgl wszedzie ?
	header->icmp_type = ICMP_ECHO; 
	header->icmp_code = 0;
	header->icmp_hun.ih_idseq.icd_id = id;
	header->icmp_hun.ih_idseq.icd_seq = (u_int16_t)ttl;
	header->icmp_cksum = 0;
	header->icmp_cksum = compute_icmp_checksum((u_int16_t*)header, sizeof(*header));
}

void send_packets(int fd, struct icmp* header, struct sockaddr_in* dest_addr) {
	for (int i = 0; i < 3; i++) {
		if (sendto(fd, header, sizeof(*header), 0, dest_addr, sizeof(*dest_addr)) < 0) {
			fprintf(stderr, "sendto\n");
			exit(1);
		}
	}
}

int is_unique(char tab[][20], int last) {
	for (int i = 0; i < last; i++) {
		if (!strcmp(tab[i], tab[last])) { return 0; }
	}
	return 1;
}

double calculate_elapsed_ms(struct timeval *start, struct timeval *end) {
	return (end->tv_sec - start->tv_sec) * 1000.0 + (end->tv_usec - start->tv_usec) / 1000.0;
}


void process_icmp_packet(struct icmp* icmp_header, struct sockaddr_in* sender_addr,
                         char senders_ip[][20], int *unique, struct timeval *start_time,
                         double *elapsed_times, int *received, int id, int ttl) {

    if (icmp_header->icmp_id == id && icmp_header->icmp_seq == ttl) {
        inet_ntop(AF_INET, &(sender_addr->sin_addr), senders_ip[*unique], sizeof(senders_ip[0]));
        if (is_unique(senders_ip, *unique)) { (*unique)++; }

        struct timeval end_time;
        gettimeofday(&end_time, NULL);
        double elapsed_ms = calculate_elapsed_ms(start_time, &end_time);
        elapsed_times[*received] = elapsed_ms;
        (*received)++;
    }
}

int main(int argc, char *argv[]) {
	if (argc != 2) {
		fprintf(stderr, "Usage: traceroute <destination_ip>\n");
		return 1;
	}

	char *dest_ip = argv[1];
	struct sockaddr_in dest_addr;
	bzero(&dest_addr, sizeof(dest_addr)); // sprawdzic czy dobrze zeruje
	dest_addr.sin_family = AF_INET;

	if (inet_pton(AF_INET, dest_ip, &dest_addr.sin_addr) <= 0) {
		fprintf(stderr, "Usage: traceroute <destination_ip>\n");
		return 1;
	}

	int sockfd;

	if ((sockfd = socket(AF_INET, SOCK_RAW, IPPROTO_ICMP)) < 0) {
		fprintf(stderr, "socket\n");
		return 1;
	}

	struct pollfd ps;
	ps.fd = sockfd;
	ps.events = POLLIN;
	ps.revents = 0;

	u_int16_t id = (u_int16_t)(getpid() & 0xFFFF);
	u_int8_t buffor[MAX_PACKET_SIZE];  
	struct ip* ip_header = (struct ip*)&buffor;
	struct icmp* icmp_header = (struct icmp*)malloc(sizeof(struct icmp));
	int success = 0;

	struct sockaddr_in sender;
	socklen_t sender_len = sizeof(sender);
	char senders_ip_str[3][20];

	struct timeval send_time;
	double elapsed_time;
	double recv_times[3];

	for (int ttl = 1; ttl <= MAX_TTL; ttl++) {

		if (success) { break; }
		setsockopt(sockfd, IPPROTO_IP, IP_TTL, &ttl, sizeof(int));

		int received = 0;
		int unique = 0;

		prepare_header(icmp_header, ttl, id);
		send_packets(sockfd, icmp_header, &dest_addr);
		gettimeofday(&send_time, NULL);
		
		double wait_time = 1000.0;
		while ((wait_time > 0.0) && received < 3 && poll(&ps, 1, (int)wait_time)) {

			while (recvfrom(sockfd, ip_header, sizeof(buffor), MSG_DONTWAIT, (struct sockaddr*)&sender, &sender_len) >= 0) {

				struct icmp* recv_icmp_header = (struct icmp*)(buffor + 4 * ip_header->ip_hl);

				if (recv_icmp_header->icmp_type == 11) {

					struct ip* capsulated_ip_header = (struct ip*)((u_int8_t*)recv_icmp_header + 8);
					struct icmp* capsulated_recv_icmp_header = (struct icmp*)((u_int8_t*)capsulated_ip_header + 4 * capsulated_ip_header->ip_hl);

					process_icmp_packet(capsulated_recv_icmp_header, &sender, senders_ip_str, &unique, &send_time, recv_times, &received, id, ttl);

				} else if (recv_icmp_header->icmp_type == 0) {

					process_icmp_packet(recv_icmp_header, &sender, senders_ip_str, &unique, &send_time, recv_times, &received, id, ttl);
					if (received == 3) { success = 1; }

				}

			}

			if (!(errno == EAGAIN) && !(errno == EWOULDBLOCK)) {
				fprintf(stderr, "recvfrom\n");
				return 1;
			}

			wait_time -= elapsed_time;
		}

		if (!received) {
			printf("%d)\t*\n", ttl);
		} else if (received == 3) {
			printf("%d)", ttl);
			for (int i = 0; i < unique; i++) { printf("\t%s", senders_ip_str[i]); }
			printf("\t\t%.3f ms\n", (recv_times[0] + recv_times[1] + recv_times[2])/3);
		} else {
			printf("%d)", ttl);
			for (int i = 0; i < unique; i++) { printf("\t%s", senders_ip_str[i]); }
			printf("\t\t???\n");
		}
	}
	free(icmp_header);
	return 0;
}

