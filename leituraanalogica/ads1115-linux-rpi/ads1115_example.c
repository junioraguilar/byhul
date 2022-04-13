
#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <linux/i2c-dev.h>
#include <sys/ioctl.h>
#include <fcntl.h>

#include "ads1115_rpi.h"

#include <time.h>

int map(float x, float in_min, float in_max, float out_min, float out_max);

//gcc ads1115_example.c ads1115_rpi.c -o ads1115_example

int main(void) {
	//ponteiro para struct que armazena data e hora  
	struct tm *data_hora_atual;     
	
	//variável do tipo time_t para armazenar o tempo em segundos  
	time_t segundos;
	FILE *fptr;
	if(openI2CBus("/dev/i2c-1") == -1)
	{
		return EXIT_FAILURE;
	}
	setI2CSlave(0x48);
	while(1)
	{
		time(&segundos);

		data_hora_atual = localtime(&segundos);
		float ch_1 = readVoltage(0);
		float ch_2 = readVoltage(1);
		float ch_3 = readVoltage(2);
		// use appropriate location if you are using MacOS or Linux
		fptr = fopen("/home/pi/Desktop/byhull2/batterylevel.txt","w");

		if(fptr == NULL)
		{
			printf("Error!");   
			exit(1);             
		}
		//printf("CH_0 = %.2f V | ", readVoltage(0) + 0.6);
		//printf("\nHorario: %d:%d:%d Tensao Bateria: %.2f",data_hora_atual->tm_hour, data_hora_atual->tm_min,data_hora_atual->tm_sec, ch_1 * 3);
		//fprintf(fptr, "\nHorario: %d:%d:%d Tensao Bateria: %.2f",data_hora_atual->tm_hour, data_hora_atual->tm_min,data_hora_atual->tm_sec, ch_1 * 3);
		//fprintf(fptr, "%d", porcentagem);
		fprintf(fptr, "%d", map(readVoltage(0) + 0.6, 1.2, 2.12, 0 ,100));
		
		//fprintf(fptr,"%.2f", porcentagem);
		fclose(fptr);
	}

	return EXIT_SUCCESS;
}

int map(float x, float in_min, float in_max, float out_min, float out_max)
{
  return (x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min;
}
