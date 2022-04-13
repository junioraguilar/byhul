#include <stdio.h>
#include <stdlib.h>

int main()
{
   float num;
   FILE *fptr;

   // use appropriate location if you are using MacOS or Linux
   fptr = fopen("/home/pi/Desktop/byhull/batterylevel.txt","w");

   if(fptr == NULL)
   {
      printf("Error!");   
      exit(1);             
   }

    num = 2.33;
   fprintf(fptr,"%.2f",num);
   fclose(fptr);

   return 0;
}