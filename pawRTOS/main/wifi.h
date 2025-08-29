#pragma once

#ifdef __cplusplus
extern "C" {
#endif

#include "freertos/FreeRTOS.h"
#include "freertos/task.h"

/* Public function to initialize Wi-Fi and start HTTP server */
void wifi_init_and_start(void);

/* Public function to stop Wi-Fi/HTTP server if needed */
void wifi_stop(void);

#ifdef __cplusplus
}
#endif
