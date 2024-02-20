#include "csapp.h"

static __unused void outc(char c) {
  Write(STDOUT_FILENO, &c, 1);
}

#define N 3
#define M 2

static struct {
  /* TODO: Put semaphores and shared variables here. */
	sem_t empty_pot;
	sem_t full_pot;
	sem_t pot_acces;
	int servings;
} *shared = NULL;


static void savage(void) {
  for (;;) {
    /* TODO Take a meal or wait for it to be prepared. */
	Sem_wait(&shared->pot_acces);
	printf("%d: takes pot acces\n", getpid());
	if (shared->servings == 0) {
		printf("%d: pot is empty !!!!!!!!!\n", getpid());
		Sem_post(&shared->empty_pot);
		Sem_wait(&shared->full_pot);
	}
	printf("%d: starts eating\n", getpid());
	shared->servings--;
	Sem_post(&shared->pot_acces);
    /* Sleep and digest. */
    usleep(rand() % 1000 + 1000);
  }

  exit(EXIT_SUCCESS);
}

static void cook(void) {
  for (;;) {
    /* TODO Cook is asleep as long as there are meals.
     * If woken up they cook exactly M meals. */
	Sem_wait(&shared->empty_pot);
	shared->servings = M;
	Sem_post(&shared->full_pot);
	printf("Cook: pot is full\n");

  }
}

/* Do not bother cleaning up after this process. Let's assume that controlling
 * terminal sends SIGINT to the process group on CTRL+C. */
int main(void) {
  shared = Mmap(NULL, getpagesize(), PROT_READ|PROT_WRITE, MAP_ANON|MAP_SHARED,
                -1, 0);

  /* TODO: Initialize semaphores and other shared state. */
  Sem_init(&shared->empty_pot, 1, 0);
  Sem_init(&shared->full_pot, 1, 0);
  Sem_init(&shared->pot_acces, 1, 1);
  shared->servings = M;

  for (int i = 0; i < N; i++)
    if (Fork() == 0)
      savage();

  cook();

  return EXIT_SUCCESS;
}
