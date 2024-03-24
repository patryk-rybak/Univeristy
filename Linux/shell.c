#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <string.h>
#include <sys/wait.h>
#include <readline/readline.h>
#include <readline/history.h>

#define MAX_ARGS 64

extern char **environ;
int sh_cd(char **args);
int sh_exit(char **args);

char *builtin_str[] = {"cd", "exit"};

int (*builtin_func[]) (char **) = {&sh_cd, &sh_exit};

int sh_num_builtins() {
		return sizeof(builtin_str) / sizeof(char *);
}

int sh_cd(char **args) {
		if (args[1] == NULL) {
				fprintf(stderr, "expected argument to \"cd\"\n");
		} else {
				if (chdir(args[1]) != 0) {
						perror("sh");
				}
		}
		return 1;
}

int sh_exit(char **args) {
		exit(0);
}

char *find_executable_path(char *command) {
		char *path = getenv("PATH");
		char *path_copy = strdup(path); // Tworzenie kopii ciągu znaków PATH
		if (path_copy == NULL) {
				perror("strdup");
				exit(EXIT_FAILURE);
		}

		char *token = strtok(path_copy, ":");
		char *executable_path = NULL;

		while (token != NULL) {
				char *candidate_path = (char *) malloc(strlen(token) + strlen(command) + 2);
				strcpy(candidate_path, token);
				strcat(candidate_path, "/");
				strcat(candidate_path, command);

				if (access(candidate_path, X_OK) == 0) {
						executable_path = candidate_path;
						break;
				}

				free(candidate_path);
				token = strtok(NULL, ":");
		}

		free(path_copy); // Zwolnienie bufora kopii ciągu znaków PATH
		return executable_path;
}

void launch_command(char **args) {
		char *executable_path = find_executable_path(args[0]);
		if (executable_path == NULL) {
				perror("Command not found\n");
				return;
		}

		pid_t pid = fork();

		if (pid == -1) {
				perror("fork");
				exit(EXIT_FAILURE);
		} else if (pid == 0) {
				execve(executable_path, args, environ);
				perror("execve");
				exit(EXIT_FAILURE);
		} else {
				int status;
				waitpid(pid, &status, 0);
		}
}

int execute_command(char **args) {
		int i;

		if (args[0] == NULL) {
				return 1;
		}

		for (i = 0; i < sh_num_builtins(); i++) {
				if (strcmp(args[0], builtin_str[i]) == 0) {
						return (*builtin_func[i])(args);
				}
		}

		launch_command(args);
		return 1;
}

int main() {
		char *input;
		while (1) {
				input = readline("> ");
				if (!input) {
						break;
				}

				if (strlen(input) > 0) {
						add_history(input);
				}

				char *args[MAX_ARGS];
				int i = 0;

				char *token = strtok(input, " \t\n");
				while (token != NULL && i < MAX_ARGS - 1) {
						args[i] = token;
						token = strtok(NULL, " \t\n");
						i++;
				}
				args[i] = NULL;

				execute_command(args);
				free(input);
		}

		return 0;
}

