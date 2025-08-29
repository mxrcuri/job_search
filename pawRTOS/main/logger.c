#include "logger.h"
#include "freertos/queue.h"
#include "esp_spiffs.h"
#include <stdio.h>

// extern log queue declared in app_main.c
extern QueueHandle_t logQueue;

void fs_init() {
    esp_vfs_spiffs_conf_t conf = {
        .base_path = "/spiffs",
        .max_files = 4,
        .format_if_mount_failed = true
    };
    esp_err_t ret = esp_vfs_spiffs_register(&conf);
    if (ret != ESP_OK) {
        printf("Failed to mount SPIFFS\n");
    }
}

void LoggerTask(void *pvParameters) {
    char msg[128];
    FILE *f = fopen("/spiffs/log.txt", "a");
    if (!f) {
        printf("Failed to open log file\n");
    }

    while (1) {
        if (xQueueReceive(logQueue, &msg, portMAX_DELAY) == pdPASS) {
            printf("[LOG] %s\n", msg);
            if (f) {
                fprintf(f, "%s\n", msg);
                fflush(f);
            }
        }
    }

    if (f) fclose(f);
}
