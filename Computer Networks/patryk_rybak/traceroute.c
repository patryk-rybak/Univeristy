// patryk_rybak 333139
#include "util.h"

int main(int argc, char *argv[]) {
	if (argc != 2) {
		fprintf(stderr, "Usage: traceroute <destination_ip>\n");
		return 1;
	}

	// Get destination IP address from command line argument
	char *dest_ip = argv[1]; 
	struct sockaddr_in dest_addr;
	bzero(&dest_addr, sizeof(dest_addr)); 
	dest_addr.sin_family = AF_INET;
	
	// Convert IP address string to binary form
	if (inet_pton(AF_INET, dest_ip, &dest_addr.sin_addr) <= 0) { 
		fprintf(stderr, "Usage: traceroute <destination_ip>\n");
		return 1;
	}

	int sockfd;

	// Create raw socket for ICMP protocol
	if ((sockfd = socket(AF_INET, SOCK_RAW, IPPROTO_ICMP)) < 0) { 
		fprintf(stderr, "socket\n");
		return 1;
	}

	// Define a poll structure for socket monitoring
	struct pollfd ps; 
	ps.fd = sockfd;
	ps.events = POLLIN;
	ps.revents = 0;

	// Generate identifier based on process ID
	u_int16_t id = (u_int16_t)(getpid() & 0xFFFF); 

	// Define headers structures
	u_int8_t buffor[MAX_PACKET_SIZE];  
	struct ip* ip_header = (struct ip*)&buffor;
	struct icmp* icmp_header = (struct icmp*)malloc(sizeof(struct icmp));

	// Define structures for receiving IP
	struct sockaddr_in sender;
	socklen_t sender_len = sizeof(sender);
	char senders_ip_str[3][20];

	// Define structures for time monitoring
	struct timeval send_time;
	double elapsed_time = 0;
	double recv_times[3];
	
	// Received all packets from destination ip
	int success = 0;

	// Loop over TTL values
	for (int ttl = 1; ttl <= MAX_TTL; ttl++) { 

		if (success) { break; } 

		// Set TTL for outgoing packets
		if (setsockopt(sockfd, IPPROTO_IP, IP_TTL, &ttl, sizeof(int)) < 0) {
				fprintf(stderr, "setsocketopt\n");
				return 1;
		}

		int received = 0;
		int unique = 0;

		// Prepare and send ICMP packet for current TTL, get current time
		prepare_header(icmp_header, ttl, id); 
		send_packets(sockfd, icmp_header, &dest_addr);
		gettimeofday(&send_time, NULL);

		// Initialize wait time for receiving packets and poll
		double wait_time = 1000.0;
		while ((wait_time > 0.0) && received < 3 && poll(&ps, 1, (int)wait_time)) {

			// Receive ICMP packets
			while (recvfrom(sockfd, ip_header, sizeof(buffor), MSG_DONTWAIT, (struct sockaddr*)&sender, &sender_len) >= 0) { 

				// Extract ICMP header
				struct icmp* recv_icmp_header = (struct icmp*)(buffor + 4 * ip_header->ip_hl); 

				// Process ICMP Time Exceeded messages
				if (recv_icmp_header->icmp_type == 11) { 

					// Extract encapsulated headers
					struct ip* capsulated_ip_header = (struct ip*)((u_int8_t*)recv_icmp_header + 8); 
					struct icmp* capsulated_recv_icmp_header = (struct icmp*)((u_int8_t*)capsulated_ip_header + 4 * capsulated_ip_header->ip_hl);

					process_icmp_packet(capsulated_recv_icmp_header, &sender, senders_ip_str, &unique, &send_time, recv_times, &received, id, ttl); 

				// Process ICMP Echo Reply
				} else if (recv_icmp_header->icmp_type == 0) { 

					process_icmp_packet(recv_icmp_header, &sender, senders_ip_str, &unique, &send_time, recv_times, &received, id, ttl);
					
					// If three replies received, set success flag
					if (received == 3) { success = 1; } 
				}
			}

			// Check for errors in receiving packets
			if (!(errno == EAGAIN) && !(errno == EWOULDBLOCK)) { 
				fprintf(stderr, "recvfrom\n");
				return 1;
			}

			// Update remaining wait time
			wait_time -= elapsed_time; 
		}

		// Print results
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

