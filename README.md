# JeevanRakshak

Underground rescue rover, worker safety network and local base-station command center.

## Repository structure

| Directory | Purpose |
|---|---|
| command-center/ | React dashboard, FastAPI backend, simulation and ingestion interfaces |
| rover/ | Raspberry Pi / ROS 2 / perception / mapping / navigation |
| firmware/ | ESP32 motor and encoder control, worker wearables |
| network/ | Relay network and PowerShell startup/failover scripts |
| hardware/ | Wiring, components and mechanical designs |
| docs/ | Architecture, setup and test records |

## Current contents

The command center is the original demo application built in this conversation. It is not asserted to include subsequent changes made on the team laptops. Its full setup and validation notes are in command-center/README.md and command-center/VALIDATION.md.

The other component folders are import destinations; their real working code has not yet been supplied. No placeholder is claimed to be deployed rover firmware.

## Run the demo

On Windows, open command-center/start-jeevanrakshak.bat. Python 3.10+ is required; first-time package installation needs internet. Open http://127.0.0.1:8000 after startup.

## Architecture

R01 owns real autonomy, safety responses and motion. The base supervises, visualizes and records. Real hardware mode remains separate from simulation. The current rover has two encoder motors at the rear; encoder wiring and acquisition status must be verified when importing firmware.

## Team workflow

Create a branch for each subsystem change, preserve the known-good network launcher, and merge reviewed changes. Import actual tested files rather than reconstructing them from descriptions. Do not commit private keys, passwords, tokens, local databases, recordings, ROS bags or installed dependencies. No open-source license is assigned pending a team decision.
