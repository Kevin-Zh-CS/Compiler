

#include <stdio.h>

/* Bootstrapping code for a stand-alone executable */

#ifdef NEED_MAIN
extern void __main(void);

int main() {
  __main();
  return 0;
}
#endif
