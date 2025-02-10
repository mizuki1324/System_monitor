import psutil

if hasattr(psutil, "sensors_temperatures"):
    temps = psutil.sensors_temperatures()
    print(temps)
else:
    print("Temperature monitoring is not supported on this system.")
