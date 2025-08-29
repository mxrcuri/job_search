#include "servo.h"
#include "driver/ledc.h"
#include "freertos/FreeRTOS.h"
#include "freertos/task.h"

/* ==================== Servo ==================== */

void servo_init() {
    ledc_timer_config_t t = {
        .speed_mode = LEDC_LOW_SPEED_MODE,
        .timer_num = LEDC_TIMER_0,
        .duty_resolution = LEDC_TIMER_16_BIT,
        .freq_hz = 50
    };
    ledc_timer_config(&t);

    ledc_channel_config_t ch = {
        .gpio_num = SERVO_PIN,
        .speed_mode = LEDC_LOW_SPEED_MODE,
        .channel = LEDC_CHANNEL_0,
        .timer_sel = LEDC_TIMER_0,
        .duty = 0
    };
    ledc_channel_config(&ch);
}

void servo_set_us(uint16_t us) {
    uint32_t duty = (us * (1 << 16) * 50) / 1000000;
    ledc_set_duty(LEDC_LOW_SPEED_MODE, LEDC_CHANNEL_0, duty);
    ledc_update_duty(LEDC_LOW_SPEED_MODE, LEDC_CHANNEL_0);
}

void dispense_treat() {
    servo_set_us(1000); // 1 ms pulse
    vTaskDelay(pdMS_TO_TICKS(DISPENSE_DURATION_MS));
    servo_set_us(0);
}
