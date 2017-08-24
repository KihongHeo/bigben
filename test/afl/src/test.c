#include <stdio.h>

void bug()
{
  char buffer[20];
  scanf("%s", buffer);
}

int main()
{
  bug();
  return 0;
}
