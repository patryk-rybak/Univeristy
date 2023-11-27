#include "csapp.h"
#include <linux/limits.h>
#include <stdio.h>

#define DIRBUFSZ 256

static void print_mode(mode_t m) {
	char t;

	if (S_ISDIR(m))
		t = 'd';
	else if (S_ISCHR(m))
		t = 'c';
	else if (S_ISBLK(m))
		t = 'b';
	else if (S_ISREG(m))
		t = '-';
	else if (S_ISFIFO(m))
		t = 'f';
	else if (S_ISLNK(m))
		t = 'l';
	else if (S_ISSOCK(m))
		t = 's';
	else
		t = '?';

	char ur = (m & S_IRUSR) ? 'r' : '-';
	char uw = (m & S_IWUSR) ? 'w' : '-';
	char ux = (m & S_IXUSR) ? 'x' : '-';
	char gr = (m & S_IRGRP) ? 'r' : '-';
	char gw = (m & S_IWGRP) ? 'w' : '-';
	char gx = (m & S_IXGRP) ? 'x' : '-';
	char or = (m & S_IROTH) ? 'r' : '-';
	char ow = (m & S_IWOTH) ? 'w' : '-';
	char ox = (m & S_IXOTH) ? 'x' : '-';

	/* TODO: Fix code to report set-uid/set-gid/sticky bit as 'ls' does. */
	// S_ISUID     04000   set-user-ID bit (see execve(2))
	// S_ISGID     02000   set-group-ID bit (see below)
	// S_ISVTX     01000   sticky bit (see below)
	ux = (m & S_ISUID) ? ((m & S_IXUSR) ? 's' : 'S') : ux;
	gx = (m & S_ISGID) ? ((m & S_IXGRP) ? 's' : 'S') : gx;
	ox = (m & S_ISVTX) ? ((m & S_IXOTH) ? 't' : 'T') : ox;


	printf("%c%c%c%c%c%c%c%c%c%c", t, ur, uw, ux, gr, gw, gx, or, ow, ox);
}

static void print_uid(uid_t uid) {
	struct passwd *pw = getpwuid(uid);
	if (pw)
		printf(" %10s", pw->pw_name);
	else
		printf(" %10d", uid);
}

static void print_gid(gid_t gid) {
	struct group *gr = getgrgid(gid);
	if (gr)
		printf(" %10s", gr->gr_name);
	else
		printf(" %10d", gid);
}

static void file_info(int dirfd, const char *name) {
	struct stat sb[1]; // dalczego jest sb[1] zamiast sb?

	/* TODO: Read file metadata. */
	if (fstatat(dirfd, name, sb, AT_SYMLINK_NOFOLLOW) == -1) {
		perror("fstatat");
		exit(EXIT_FAILURE);
	}

	print_mode(sb->st_mode);
	printf("%4ld", sb->st_nlink);
	print_uid(sb->st_uid);
	print_gid(sb->st_gid);

	/* TODO: For devices: print major/minor pair; for other files: size. */
	if (S_ISCHR(sb->st_mode) || S_ISBLK(sb->st_mode)) {
		printf("%3u, %3u", major(sb->st_rdev), minor(sb->st_rdev));
	} else {
		printf("%6lu", sb->st_size);
	}

	char *now = ctime(&sb->st_mtime);
	now[strlen(now) - 1] = '\0';
	printf("%26s", now);

	printf("  %s", name);

	if (S_ISLNK(sb->st_mode)) {
		/* TODO: Read where symlink points to and print '-> destination' string. */
		char buf[PATH_MAX];
		if (readlinkat(dirfd, name, buf, PATH_MAX)) {
			printf(" -> %s", buf);
		} else {
			perror("readlinkat");
			exit(EXIT_FAILURE);
		}
	}

	putchar('\n');
}

int main(int argc, char *argv[]) {
	if (!argv[1])
		argv[1] = ".";

	int dirfd = Open(argv[1], O_RDONLY | O_DIRECTORY, 0);
	char buf[DIRBUFSZ];
	int n;

	while ((n = Getdents(dirfd, (void *)buf, DIRBUFSZ))) {
		struct linux_dirent *d;
		/* TODO: Iterate over directory entries and call file_info on them. */
		long bytes_counter = 0;
		while (bytes_counter < n) {
			d = (struct linux_dirent *) (buf + bytes_counter);
			bytes_counter += d->d_reclen;
			file_info(dirfd, d->d_name);
		}
	}

	Close(dirfd);
	return EXIT_SUCCESS;
}
