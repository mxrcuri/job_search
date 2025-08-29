#pragma once
#include "freertos/FreeRTOS.h"
#include "freertos/queue.h"
#include "esp_spiffs.h"
#include <stdio.h>

#define LOG_QUEUE_LENGTH 20

extern QueueHandle_t logQueue;

void fs_init();
void LoggerTask(void *pvParameters);

#define LOG_MSG(fmt, ...) do {                        \
    char msg[128];                                    \
    snprintf(msg, sizeof(msg), fmt, ##__VA_ARGS__);   \
    xQueueSend(logQueue, &msg, 0);                    \
} while(0)
