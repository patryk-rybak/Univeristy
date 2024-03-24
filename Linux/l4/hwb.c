#include <stdio.h>
#include <ctype.h>
#include <unistd.h>
#include <string.h>
#include <getopt.h>

void print_usage() {
    printf("Usage: hwb [OPTIONS]\n");
    printf("Options:\n");
    printf("  -c, --capitalize\t\tPrint the name or 'world' in uppercase.\n");
    printf("  --color=[never | auto | always]\tColorize names (never, auto if the standard output is a terminal, always), similar to the option in the ls(1) program.\n");
    printf("  -g text, --greeting=text\tReplace the word 'Hello' with the provided text.\n");
    printf("  -h, --help\t\t\tPrint a brief help message.\n");
    printf("  -v, --version\t\tPrint the program's name, version, and copyright.\n");
    printf("  -w, --world\t\t\tAdditionally print the line 'Hello, world'.\n");
}

void print_version() {
		printf("hwb version 1.0\n");
}

int is_colorizable() {
	return isatty(1) ? 1 : 0;
}

void print_output(char *greeting, char *name, char *color, int capitalize) {
		if (capitalize) {
				for (char *ptr = name; *ptr; ++ptr) {
						*ptr = toupper(*ptr);
				}
		}
	printf("%s ", greeting);
	if (!strcmp(color, "always") || (!strcmp(color, "auto") && is_colorizable()))
		printf("\033[0;34m");

	printf("%s\033[0m!\n", name);
}

int main(int argc, char *argv[]) {
    int option;
    int capitalize = 0;
    char *color = "auto";
    char *greeting = "Hello";
	char world[] = "world";
	int hello_world = 0;

    struct option long_options[] = {
        {"capitalize", no_argument, NULL, 'c'},
        {"color", required_argument, NULL, 'r'},
        {"greeting", required_argument, NULL, 'g'},
        {"help", no_argument, NULL, 'h'},
        {"version", no_argument, NULL, 'v'},
        {"world", no_argument, NULL, 'w'},
        {NULL, 0, NULL, 0}
    };

    while ((option = getopt_long(argc, argv, "cr:g:hvw", long_options, NULL)) != -1) {
        switch (option) {
            case 'c':
                capitalize = 1;
                break;
            case 'r':
                color = optarg;
                break;
            case 'g':
                greeting = optarg;
                break;
            case 'h':
                print_usage();
                return 0;
            case 'v':
				print_version();
                return 0;
            case 'w':
				hello_world = 1;
                break;
            default:
                print_usage();
                return 1;
        }
    }

	for (int i = optind; i < argc; i++) {
			print_output(greeting, argv[i], color, capitalize);
	}
	if (hello_world) {
			print_output(greeting, world, color, capitalize);
	}

    return 0;
}

