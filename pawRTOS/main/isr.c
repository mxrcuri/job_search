#include "isr.h"
#include "freertos/FreeRTOS.h"
#include "freertos/task.h"
#include "driver/gpio.h"
#include "gatekeeper.h"
#include "logger.h"
#include "esp_log.h"

static const char *TAG = "isr";

/* ISR handler: notify gatekeeper */
static void IRAM_ATTR gpio_isr_handler(void* arg)
{
    BaseType_t xHigher = pdFALSE;
    // Notify the gatekeeper task from ISR context
    vTaskNotifyGiveFromISR(gatekeeperTaskHandle, &xHigher);
    if (xHigher == pdTRUE) {
        portYIELD_FROM_ISR();
    }
}

/* Initialize the GPIO input and attach ISR */
void isr_button_init(int gpio_pin, int trigger_type)
{
    gpio_config_t io_conf = {
        .pin_bit_mask = (1ULL << gpio_pin),
        .mode = GPIO_MODE_INPUT,
        .pull_up_en = GPIO_PULLUP_ENABLE,
        .pull_down_en = GPIO_PULLDOWN_DISABLE,
        .intr_type = trigger_type
    };
    gpio_config(&io_conf);

    // install ISR service with default config
    gpio_install_isr_service(0);
    gpio_isr_handler_add(gpio_pin, gpio_isr_handler, (void*)(uintptr_t)gpio_pin);

    LOG_MSG("ISR button on GPIO %d initialized", gpio_pin);
}
