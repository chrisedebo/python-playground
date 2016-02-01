import nginx_updater as n

r1 = n.Request()
r1.service = "r1"
r1.host = "http://r1"

r11 = n.Request()
r11.service = "r1"
r11.host = "http://r11"

r2 = n.Request()
r2.service = "r2"
r2.host = "http://r2"

requests = [r1, r2, r11]

