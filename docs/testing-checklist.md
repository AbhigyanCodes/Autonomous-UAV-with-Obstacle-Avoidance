# Testing & Safety Checklist

Before powering up and flight testing, follow this checklist.

## Bench tests (props removed)
1. Confirm Raspberry Pi boots and has network (SSH recommended)
2. Confirm `/dev/serial0` exists: `ls -l /dev/serial*`
3. Confirm Pixhawk connected to TELEM2 and QGroundControl receives MAVLink messages
4. Run `python3 src/companion/main.py` and check logs:
   - Sensor readings (HC-SR04 distances)
   - Camera initializes (if present)
   - MAVSDK connection established
5. Validate Offboard/velocity commands are sent when simulated obstacle present (monitor in QGC)
6. Use `mavproxy.py` as secondary monitor: `mavproxy.py --master=/dev/serial0 --baudrate 57600`

## Ground tests (props on, safe area, tethered optional)
1. Run hover test at minimal altitude with failsafe present
2. Verify obstacle avoidance triggers appropriate lateral/heading response
3. Check for overheating, odd vibrations, or degraded responses

## Flight tests
1. Only after successful bench & ground tests
2. Keep flight area clear, have spotter and kill-switch
3. Start with short, low-altitude flights (props on)
4. Verify mission fail-safe settings

## Emergency actions
- If controls misbehave: immediately switch to manual / stabilize
- Always have an RC transmitter override enabled
