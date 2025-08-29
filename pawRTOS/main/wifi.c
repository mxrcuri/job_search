#include "wifi.h"
#include "logger.h"
#include "gatekeeper.h"    // for gatekeeperTaskHandle
#include "esp_event.h"
#include "esp_log.h"
#include "esp_netif.h"
#include "esp_wifi.h"
#include "nvs_flash.h"
#include "esp_http_server.h"
#include <string.h>
#include <inttypes.h>

/* Replace these with your credentials or load from menuconfig/NVS */
#ifndef WIFI_SSID
#define WIFI_SSID "YOUR_SSID"
#endif
#ifndef WIFI_PASS
#define WIFI_PASS "YOUR_PASS"
#endif

static const char *TAG = "wifi_module";
static httpd_handle_t server_handle = NULL;

/* ========== HTTP handler (same behavior as before) ========== */
static esp_err_t dispense_handler(httpd_req_t *req)
{
    // notify the gatekeeper from ISR context path: use FromISR API
    BaseType_t xHigher = pdFALSE;
    vTaskNotifyGiveFromISR(gatekeeperTaskHandle, &xHigher);
    if (xHigher == pdTRUE) {
        portYIELD_FROM_ISR();
    }
    httpd_resp_send(req, "OK", HTTPD_RESP_USE_STRLEN);
    return ESP_OK;
}

static const httpd_uri_t dispense_uri = {
    .uri      = "/dispense",
    .method   = HTTP_GET,
    .handler  = dispense_handler
};

/* ========== start/stop HTTP server ========== */
static void start_http_server(void)
{
    if (server_handle) return;

    httpd_config_t config = HTTPD_DEFAULT_CONFIG();
    if (httpd_start(&server_handle, &config) == ESP_OK) {
        httpd_register_uri_handler(server_handle, &dispense_uri);
        LOG_MSG("HTTP Server started");
    } else {
        LOG_MSG("Failed to start HTTP server");
    }
}

void wifi_stop()
{
    if (server_handle) {
        httpd_stop(server_handle);
        server_handle = NULL;
    }
}

/* ========== Wi-Fi event handlers ========== */
static void on_got_ip(void* arg, esp_event_base_t event_base,
                      int32_t event_id, void* event_data)
{
    ip_event_got_ip_t* event = (ip_event_got_ip_t*) event_data;
    char ip_str[16]; // enough for "xxx.xxx.xxx.xxx"
    esp_ip4addr_ntoa(&event->ip_info.ip, ip_str, sizeof(ip_str));
    LOG_MSG("WiFi connected, IP: %s", ip_str);

    start_http_server();
}

static void on_wifi_event(void* arg, esp_event_base_t event_base,
                          int32_t event_id, void* event_data)
{
    if (event_id == WIFI_EVENT_STA_DISCONNECTED) {
        LOG_MSG("WiFi disconnected, retrying...");
        esp_wifi_connect();
    }
}

/* ========== Public init function ========== */
void wifi_init_and_start()
{
    esp_err_t ret = nvs_flash_init();
    if (ret == ESP_ERR_NVS_NO_FREE_PAGES || ret == ESP_ERR_NVS_NEW_VERSION_FOUND) {
        nvs_flash_erase();
        nvs_flash_init();
    }

    esp_netif_init();
    esp_event_loop_create_default();
    esp_netif_create_default_wifi_sta();

    wifi_init_config_t cfg = WIFI_INIT_CONFIG_DEFAULT();
    esp_wifi_init(&cfg);

    esp_event_handler_instance_t instance_any_id;
    esp_event_handler_instance_t instance_got_ip;
    esp_event_handler_instance_register(WIFI_EVENT, ESP_EVENT_ANY_ID, &on_wifi_event, NULL, &instance_any_id);
    esp_event_handler_instance_register(IP_EVENT, IP_EVENT_STA_GOT_IP, &on_got_ip, NULL, &instance_got_ip);

    wifi_config_t wifi_config = { 0 };
    strncpy((char*)wifi_config.sta.ssid, WIFI_SSID, sizeof(wifi_config.sta.ssid)-1);
    strncpy((char*)wifi_config.sta.password, WIFI_PASS, sizeof(wifi_config.sta.password)-1);

    esp_wifi_set_mode(WIFI_MODE_STA);
    esp_wifi_set_config(WIFI_IF_STA, &wifi_config);
    esp_wifi_start();
    esp_wifi_connect();

    LOG_MSG("WiFi init started (ssid=%s)", WIFI_SSID);
}
