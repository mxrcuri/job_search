#pragma once
#include <stdint.h>

/* Setup a GPIO input with interrupt to trigger gatekeeper.
   gpio_pin: pin number (use GPIO_NUM_x)
   trigger_type: GPIO_INTR_POSEDGE / NEGEDGE / ANYEDGE
*/
void isr_button_init(int gpio_pin, int trigger_type);
