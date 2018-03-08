// epoll server source code
#include <assert.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <sys/socket.h>
#include <sys/types.h>
#include <sys/epoll.h>
#include <arpa/inet.h>
#include <fcntl.h>
#include <unistd.h>

#pragma pack(1)

typedef struct DATANODE
{
    int fd; 
    char buffer[1024];
    uint32_t buffer_len;
}DataNode;

#pragma pack()



int main(int argc, char **argv) 
{

    int conn_fd = 0;

    int listen_fd = socket(AF_INET, SOCK_STREAM, IPPROTO_TCP);
    if (listen_fd == -1) {
        assert (0);
    }

    int on = 1; 
    if (setsockopt(listen_fd, SOL_SOCKET, SO_REUSEADDR, &on, sizeof(on)) < 0) {
        assert (0);
    }

    int32_t old_flag = fcntl(listen_fd, F_GETFL, 0);
    int32_t new_flag = old_flag | O_NONBLOCK;
    fcntl(listen_fd, F_SETFL, new_flag);

    char *host_ip = "10.144.29.22";
    uint16_t host_port = 8752;
    struct sockaddr_in addr_sever;
    memset(&addr_sever, 0, sizeof(addr_sever));
    addr_sever.sin_family = AF_INET;
    inet_pton(AF_INET, host_ip, &addr_sever.sin_addr);
    addr_sever.sin_port = htons(host_port);

    // bind
    if (bind(listen_fd, (struct sockaddr*)&addr_sever, sizeof(addr_sever)) < 0) {
        assert (0);
    }

    // listen
    if (listen(listen_fd, 10) < 0) {
        assert(0);
    }

    int epoll_fd = epoll_create(1024);

    DataNode *node_ptr = new DataNode;
    node_ptr->fd = listen_fd;
    struct epoll_event ev;
    ev.data.ptr = node_ptr;
    ev.events = EPOLLIN;
    epoll_ctl(epoll_fd, EPOLL_CTL_ADD, listen_fd, &ev);

    int nfds = 0;
    struct epoll_event ev_list[20];
    while (1) {
        nfds = epoll_wait(epoll_fd, ev_list, 20, -1);
        for (int idx = 0; idx < nfds; idx++ ) {
            DataNode *nd_ptr = (DataNode*)(ev_list[idx].data.ptr);
            int fd = nd_ptr->fd;
            if (fd == listen_fd) { // connect
                conn_fd = accept(listen_fd, NULL, NULL);
                assert(conn_fd != -1);
                printf ("accept succ, connfd=%d.\n", conn_fd);
                DataNode *node_ptr = new DataNode;
                node_ptr->fd = conn_fd;
                ev.data.ptr = node_ptr;
                ev.events = EPOLLIN;
                epoll_ctl(epoll_fd, EPOLL_CTL_ADD, conn_fd, &ev);
            } else {
                if (ev_list[idx].events &EPOLLIN) {
                    int read_len = 0;
                    char buffer[1024] = {0};
                    read_len = read(fd, buffer, 1024);
                    if (read_len < 0) {
                        close(fd);
                        epoll_ctl(epoll_fd, EPOLL_CTL_DEL, fd, NULL);
                        printf ("EPOLL_CTL_DEL %u\n", __LINE__);
                        if (nd_ptr !=  NULL) {
                            delete nd_ptr;
                        }
                    } else if (read_len == 0) {
                        close(fd);
                        epoll_ctl(epoll_fd, EPOLL_CTL_DEL, fd, NULL);
                        printf ("EPOLL_CTL_DEL %u\n", __LINE__);
                        if (nd_ptr != NULL) {
                            delete nd_ptr;
                        }
                    } else {
                        buffer[read_len] = 0;
                        printf ("recv_buffer:%s\n", buffer);
                        strcpy(nd_ptr->buffer, buffer);
                        nd_ptr->buffer_len = read_len;
                        ev.data.ptr = nd_ptr;
                        ev.events = EPOLLOUT;
                        epoll_ctl(epoll_fd, EPOLL_CTL_MOD, fd, &ev);
                        printf ("EPOLL_CTL_MOD %u\n", __LINE__);
                    }
                } else if (ev_list[idx].events &EPOLLOUT) {
                    // write(fd, "12345", 5);
                    write(fd, nd_ptr->buffer, nd_ptr->buffer_len);
                    ev.data.ptr = nd_ptr;
                    ev.events = EPOLLIN;
                    epoll_ctl(epoll_fd, EPOLL_CTL_MOD, fd, &ev);
                    printf ("EPOLL_CTL_MOD %u\n", __LINE__);
                }
            }
        }
    }
    close (epoll_fd);
    close (listen_fd);
    return 0;
}