#include "gatekeeper.h"
#include "logger.h"
#include "servo.h"
#include "esp_task_wdt.h"
#include "esp_timer.h"
#include <inttypes.h>


// extern handle defined in app_main.c
extern TaskHandle_t gatekeeperTaskHandle;

static uint32_t last_dispense_time = 0;
#define DISPENSE_INTERVAL_MS (3*60*60*1000) // 3 hours

void GatekeeperTask(void *pvParameters) {
    while (1) {
        ulTaskNotifyTake(pdTRUE, portMAX_DELAY);  // wait for dispense signal

        uint32_t now = (uint32_t)(esp_timer_get_time() / 1000);
        if (now - last_dispense_time >= DISPENSE_INTERVAL_MS) {
            LOG_MSG("Dispensing treat at %" PRIu32 " ms", now);

            dispense_treat();
            last_dispense_time = now;
        } else {
            LOG_MSG("Dispense skipped, interval not reached");
        }

        esp_task_wdt_reset(); // feed watchdog
    }
}

void DispenseTimerCallback(TimerHandle_t xTimer) {
    // Notify the Gatekeeper task
    xTaskNotifyGive(gatekeeperTaskHandle);
}
