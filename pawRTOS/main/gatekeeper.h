#pragma once
#include "freertos/FreeRTOS.h"
#include "freertos/task.h"
#include "freertos/timers.h"

extern TaskHandle_t gatekeeperTaskHandle;
extern TimerHandle_t dispenseTimer;

void GatekeeperTask(void *pvParameters);
void DispenseTimerCallback(TimerHandle_t xTimer);
