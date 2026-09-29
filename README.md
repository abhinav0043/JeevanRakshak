# JeevanRakshak

**AI-Powered Underground Mine Safety, Monitoring & Rescue System**  
Smart India Hackathon 2026 · Problem Statement **SIH26039**

JeevanRakshak is an autonomous underground rescue ecosystem centered on the **R01 Rescue Rover**. It combines onboard perception, SLAM, autonomous navigation, environmental monitoring, worker wearables and a resilient relay network so rescue teams can obtain actionable intelligence before entering hazardous mine sections.

## Core mission

R01 is designed to:

- map unknown underground passages with LiDAR + depth sensing;
- localize without GPS using ICP / RTAB-Map;
- navigate with ROS 2 Nav2 and frontier exploration;
- detect possible victims with RGB AI + depth ranging + thermal evidence;
- monitor environmental and rover-health telemetry;
- publish live mission intelligence to a Base Station Command Center;
- keep mission-critical autonomy onboard during communication loss;
- support a temporary **JR_BYPASS** route when the wired relay path fails.

## Architecture

```text
YDLIDAR + D435 + AMG8833 + Environmental Sensors
                         |
                         v
                Raspberry Pi 5 / R01
        ROS 2 + ICP + RTAB-Map + Nav2 + AI
                         |
              +----------+----------+
              |                     |
              v                     v
            ESP32               Base Station
   motor watchdog/control      Command Center
              |                     ^
              v                     |
      SmartElex + 4WD          Relay Network
                                    |
                       Ethernet / JR_BYPASS / LoRa
```

## Prototype capabilities

- Raspberry Pi 5 + ESP32 split-control architecture
- UART sensor/motor bridge with watchdog
- 4WD differential-drive control
- YDLIDAR G2 ROS 2 integration
- Intel RealSense D435 RGB/depth integration
- LiDAR ICP odometry + RTAB-Map pipeline
- Nav2 navigation software pipeline
- frontier-exploration integration
- YOLOv4-tiny person detection using OpenCV DNN
- D435 depth fusion for person distance
- AMG8833 8×8 thermal target evidence
- multi-sensor victim-fusion state
- real ESP32 telemetry into the Base Station dashboard
- React + FastAPI command center with WebSocket updates
- normal relay path and JR_BYPASS recovery architecture

## Base Station Command Center

The dashboard is designed to show:

- RGB / night-vision feed
- depth perception
- AMG8833 thermal view
- environment telemetry
- AI detections, confidence and person distance
- victim-fusion status
- 2D / 3D mine map
- rover pose and navigation state
- worker wearable events
- relay topology
- network-break / bypass-node state
- mission timeline and alerts

## Repository layout

```text
JeevanRakshak/
├── README.md
├── command-center/       # React + FastAPI Base Station application
├── rover/                # Pi / ROS 2 runtime and integration scripts
├── firmware/             # ESP32 / wearable firmware
├── network/              # relay and failover configuration/scripts
├── hardware/             # wiring and hardware documentation
├── docs/                 # architecture and validation records
└── showcase/             # public Vercel project page
```

## Technology

**Rover:** ROS 2 Jazzy, RTAB-Map, Nav2, OpenCV, Python, Docker  
**Compute/control:** Raspberry Pi 5, ESP32  
**Perception:** Intel RealSense D435, YDLIDAR G2, OV5647 day/night camera, AMG8833  
**Command Center:** React, TypeScript, Vite, FastAPI, SQLite, WebSockets  
**Communication:** Ethernet/local Wi-Fi relay network, LoRa fallback, JR_BYPASS recovery path

## Prototype boundaries

JeevanRakshak is a research prototype. Raw MQ readings are not presented as certified gas concentrations. AMG8833 output is treated as coarse thermal evidence, not a medical measurement. Structural sensing is described as obstruction / structural-condition awareness rather than collapse prediction. Mine deployment would require industrial calibration, intrinsic-safety design, ruggedization and certification.

## Public showcase

A static public project showcase is provided from the `showcase/` directory for Vercel deployment.  
The operational hardware dashboard remains local to the Base Station because it consumes live rover telemetry over the JeevanRakshak LAN.

---

**JeevanRakshak — from blind human-first entry to autonomous, sensor-rich rescue reconnaissance.**
