#pragma once
#include <stdint.h>

#define SERVO_PIN 18
#define DISPENSE_DURATION_MS 1000

void servo_init(void);
void servo_set_us(uint16_t us);
void dispense_treat(void);
