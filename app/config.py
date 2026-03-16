PORT_LIST = [80, 443, 25, 53, 3306, 6379]

UPSTREAM_TARGETS = [
    ("127.0.0.1", 8009),
]

REFRESH_INTERVAL = 10

DSM_PROXY_CONFIG_PATHS = [
    "/usr/syno/etc/nginx/app.d",
    "/usr/local/etc/nginx/conf.d",
    "/etc/nginx/conf.d",
]
