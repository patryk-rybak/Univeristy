// patryk_rybak 333139
#include "util.h"

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
	bzero(header, sizeof(*header));
	header->icmp_type = ICMP_ECHO;
	header->icmp_code = 0;
	header->icmp_hun.ih_idseq.icd_id = id;
	header->icmp_hun.ih_idseq.icd_seq = (u_int16_t)ttl;
	header->icmp_cksum = 0;
	header->icmp_cksum = compute_icmp_checksum((u_int16_t*)header, sizeof(*header));
}

void send_packets(int fd, struct icmp* header, struct sockaddr_in* dest_addr) {
	for (int i = 0; i < 3; i++) {
		if (sendto(fd, header, sizeof(*header), 0, (struct sockaddr *)dest_addr, sizeof(*dest_addr)) < 0) {
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

	// Check if ICMP packet matches identifier and sequence number
	if (icmp_header->icmp_id == id && icmp_header->icmp_seq == ttl) { 
		
		// Convert sender's IP address to string
		inet_ntop(AF_INET, &(sender_addr->sin_addr), senders_ip[*unique], sizeof(senders_ip[0]));

		if (is_unique(senders_ip, *unique)) { (*unique)++; } 

		// Calculate elapsed time
		struct timeval end_time;
		gettimeofday(&end_time, NULL);
		double elapsed_ms = calculate_elapsed_ms(start_time, &end_time);
		elapsed_times[*received] = elapsed_ms;

		(*received)++;
	}
}

