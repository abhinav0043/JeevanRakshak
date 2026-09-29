# Validation report

Verified in the build environment on 2026-09-26 UTC.

## Passed

- TypeScript strict type checking and Vite production compilation.
- Production HTML, bundled CSS/JavaScript assets, SPA route fallback and health endpoint smoke check.
- Nine automated backend integration tests:
  1. Full 20-step scenario, bypass state, payload consumption, worker SOS, semantic markers, persisted snapshot and JSON/CSV export.
  2. Emergency command confirmation, stop latch, blocked resume and explicit all-clear.
  3. Demo/hardware isolation, empty hardware startup, worker ingestion, mismatched IDs, invalid thermal data, real-command rejection.
  4. Alert acknowledgement and relay inventory exhaustion.
  5. Existing LoRa packet parsing and binary float32 point-cloud ingestion.
  6. WebSocket initial snapshot and reconnect after a hazard event.
  7. Navigation to an operator-specified demo goal.
  8. Ingestion token rejection and validation of incomplete rover telemetry.
  9. Occupancy-grid ingestion and invalid timestamp rejection.

## Limitations of verification

- Browser visual/interaction QA could not be completed here. The available cloud browser blocked workspace localhost access. A local headless-browser package download also failed. No browser screenshots or pixel-level claims are supplied.
- Responsive CSS covers laptop/projector and narrower displays, but actual 1920×1080 and 1366×768 visual verification remains to be performed on the base laptop.
- Windows launcher was authored and reviewed but cannot be executed on this Linux environment.
- No real hardware, ROS graph, gas calibration, radio failover or physical relay deployment was tested.
- Production build reports a large JavaScript bundle (~1.6 MB uncompressed) due to Three.js and charting. It is local and requires no internet; further code splitting is optional.
- Test runner emits a dependency deprecation warning from Starlette/AnyIO; all tests pass.

## Base-laptop acceptance check

1. Run start-jeevanrakshak.bat and confirm http://127.0.0.1:8000 loads.
2. Confirm DEMO MODE, six workers and moving R01.
3. Try 3D orbit/zoom, Top, Follow and 2D tactical map.
4. Play FULL RESCUE DEMO; confirm gas warning, possible victim, W04 SOS, R2–R3 break and bypass recovery.
5. Confirm STOP freezes movement and requires clear + resume.
6. Open a worker, focus its last confirmed zone, acknowledge an alert.
7. Export JSON/CSV and inspect the saved mission after restarting.
8. Switch to REAL HARDWARE MODE; confirm the demo data disappears and missing sensors show waiting.
9. Verify a real movement command explicitly fails until a hardware transport is installed.
