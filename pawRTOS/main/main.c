#include "freertos/FreeRTOS.h"
#include "freertos/task.h"
#include "freertos/queue.h"
#include "freertos/timers.h"
#include "esp_task_wdt.h"
#include "esp_sleep.h"
#include "logger.h"
#include "servo.h"
#include "gatekeeper.h"
#include "wifi.h"
#include "isr.h"

QueueHandle_t logQueue;
TaskHandle_t gatekeeperTaskHandle;
TimerHandle_t dispenseTimer;

void vApplicationIdleHook(void) {
    if (uxQueueMessagesWaiting(logQueue) == 0) {
        esp_light_sleep_start();
    }
}

void app_main(void) {
    // Init filesystem (if implemented)
    fs_init();

    // Init logger first
    logQueue = xQueueCreate(LOG_QUEUE_LENGTH, sizeof(char[128]));
    xTaskCreate(LoggerTask, "Logger", 2048, NULL, 1, NULL);

    // Servo
    servo_init();

    // Gatekeeper task
    xTaskCreate(GatekeeperTask, "Gatekeeper", 2048, NULL, 3, &gatekeeperTaskHandle);


    esp_task_wdt_config_t wdt_config = {
        .timeout_ms = 10000,      // 10 seconds
        .trigger_panic = true
    };
    esp_task_wdt_init(&wdt_config);

    esp_task_wdt_add(gatekeeperTaskHandle);

    // Timer for auto-dispense (60s periodic)
    dispenseTimer = xTimerCreate("DispenseTimer",
                                 pdMS_TO_TICKS(60000),
                                 pdTRUE,
                                 NULL,
                                 DispenseTimerCallback);
    xTimerStart(dispenseTimer, 0);

    // Now safe to start Wi-Fi + webserver
    wifi_init_and_start();

    // Init ISR button (BOOT pin example)
    isr_button_init(GPIO_NUM_0, GPIO_INTR_NEGEDGE);
}
