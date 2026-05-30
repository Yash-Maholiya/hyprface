#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <sys/socket.h>
#include <sys/un.h>

#define PAM_SM_AUTH
#include <security/pam_modules.h>
#include <security/pam_ext.h>

#define SOCKET_PATH "/tmp/hyprface.sock"
#define TIMEOUT_SEC 10

static int connect_to_daemon(void) {
    int fd = socket(AF_UNIX, SOCK_STREAM, 0);
    if (fd < 0) return -1;

    struct sockaddr_un addr;
    memset(&addr, 0, sizeof(addr));
    addr.sun_family = AF_UNIX;
    strncpy(addr.sun_path, SOCKET_PATH, sizeof(addr.sun_path) - 1);

    if (connect(fd, (struct sockaddr *)&addr, sizeof(addr)) < 0) {
        close(fd);
        return -1;
    }

    return fd;
}

PAM_EXTERN int pam_sm_authenticate(pam_handle_t *pamh, int flags, int argc, const char **argv) {
    int fd = connect_to_daemon();
    if (fd < 0) return PAM_AUTHINFO_UNAVAIL;

    const char *msg = "AUTH\n";
    if (write(fd, msg, strlen(msg)) < 0) {
        close(fd);
        return PAM_AUTHINFO_UNAVAIL;
    }

    char buf[64];
    memset(buf, 0, sizeof(buf));

    struct timeval tv = { .tv_sec = TIMEOUT_SEC, .tv_usec = 0 };
    fd_set fds;
    FD_ZERO(&fds);
    FD_SET(fd, &fds);

    int ready = select(fd + 1, &fds, NULL, NULL, &tv);
    if (ready <= 0) {
        close(fd);
        return PAM_AUTH_ERR;
    }

    ssize_t n = read(fd, buf, sizeof(buf) - 1);
    close(fd);

    if (n <= 0) return PAM_AUTH_ERR;

    if (strncmp(buf, "OK", 2) == 0) return PAM_SUCCESS;

    return PAM_AUTH_ERR;
}

PAM_EXTERN int pam_sm_setcred(pam_handle_t *pamh, int flags, int argc, const char **argv) {
    return PAM_SUCCESS;
}