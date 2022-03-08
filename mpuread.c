#include "Wire.h"
#include "I2Cdev.h"
#include "MPU6050.h"

MPU6050 accelgyro;

int16_t ax, ay, az;
int16_t gx, gy, gz;

#define G_GAIN 0.00875
#define AA 0.98

float acelx, acely, acelz, rate_gyr_x, rate_gyr_y, rate_gyr_z, gyroXangle, gyroYangle, gyroZangle;
float AccXangle, AccYangle, AccZangle, CFangleX, CFangleY, CFangleZ;
float const_calib = 16071.82;
float const_gravid = 9.81;

unsigned long pT;

void setup() {
Wire.begin(); // Inicia barramento I2C

// initializa conexão serial
Serial.begin(9600);
Serial.println("Initializing I2C devices…");

// verifica conexão com sensores
Serial.println("Testing device connections…");
Serial.println(accelgyro.testConnection() ? "MPU6050 connection successful" : "MPU6050 connection failed");

unsigned long pT = 0; // contador para determinar tempo de inicialização
}

void loop() {
unsigned long cT = micros(); // contar tempo de loop

accelgyro.getMotion6(&ax, &ay, &az, &gx, &gy, &gz); // obtem valores brutos dos sensores

unsigned long dT = cT – pT;
pT = cT;

acelx = ax * const_gravid / const_calib;
acely = ay * const_gravid / const_calib;
acelz = az * const_gravid / const_calib;

// Converte valor do acelerometro com base nos 3 eixos
AccXangle = (atan2(ax, sqrt(pow(ay,2) + pow(az,2)))*180) / 3.14;
AccYangle = (atan2(ay, sqrt(pow(ax,2) + pow(az,2)))*180) / 3.14;
AccZangle = (atan2(az, sqrt(pow(ax,2) + pow(ay,2)))*180) / 3.14;

// Converte valor do giro em graus por seg
// multiplicando uma contante relacionada à taxa de amostragem do sensor
// nesse caso, a taxa é +-250g -> 0.00875
rate_gyr_x = gx*G_GAIN;
rate_gyr_y = gy*G_GAIN;
rate_gyr_z = gz*G_GAIN;

// Calcula a distância percorrida por integração simples
// com base no tempo de loop (dT = cT – pT)
gyroXangle+=rate_gyr_x*dT;
gyroYangle+=rate_gyr_y*dT;
gyroZangle+=rate_gyr_z*dT;

// Fusão dos dados: giro + accel
// Métodos: filtro complementar ou filtro de kalman
// Optei pelo Filtro Complementar por ser mais simples de se aplicar do que o Filtro de Kalman.
// Eficiencia bastante satisfatoria, segundo teoria
// Atribui peso de 0.98 ao valor do giro e 0.02 ao acelerometro
// O giroscópio tem leitura muito boa, mas também apresenta oscilação do valor.
// Acelerômetro, por outro lado, é muito ruidoso, mas o desvio é zero.

CFangleX=AA*(CFangleX+rate_gyr_x*(dT/1000000)) +(1 – AA) * AccXangle;
CFangleY=AA*(CFangleY+rate_gyr_y*(dT/1000000)) +(1 – AA) * AccYangle;
CFangleZ=AA*(CFangleZ+rate_gyr_z*(dT/1000000)) +(1 – AA) * AccZangle;
}