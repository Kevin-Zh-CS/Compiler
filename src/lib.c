/* gonert.c

   This file contains runtime support functions for the Gone language
   as well as boot-strapping code related to getting the main program
   to run.
*/

#include <stdio.h>

/* Bootstrapping code for a stand-alone executable */

#ifdef NEED_MAIN
extern void __main(void);

int main() {
  __main();
  return 0;
}
#endif
