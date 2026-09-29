"""Adapters normalize input only. Real mission intelligence belongs on R01."""
from typing import Protocol, AsyncIterator, Any
from ..models import Event, Command
class TelemetryProvider(Protocol):
    def events(self) -> AsyncIterator[Event]: ...
class RoverTelemetryProvider(TelemetryProvider, Protocol): pass
class WorkerTelemetryProvider(TelemetryProvider, Protocol): pass
class MapProvider(TelemetryProvider, Protocol): pass
class PointCloudProvider(TelemetryProvider, Protocol): pass
class VideoProvider(TelemetryProvider, Protocol): pass
class AIInferenceProvider(TelemetryProvider, Protocol): pass
class ThermalProvider(TelemetryProvider, Protocol): pass
class NetworkTopologyProvider(TelemetryProvider, Protocol): pass
class CommandProvider(Protocol):
    async def send(self,command: Command) -> dict[str,Any]: ...
class UnconfiguredCommandProvider:
    async def send(self,command):
        raise RuntimeError('R01 command transport is not configured; nothing was sent')
class Ros2RoverProvider:
    """Implement events() on R01 bridge; normalize odometry, diagnostics and mission states."""
    async def events(self):
        raise NotImplementedError('ROS 2 bridge not connected')
        yield
class Ros2MapProvider(Ros2RoverProvider): pass
class PiAIProvider(Ros2RoverProvider): pass
class RealNetworkProvider(Ros2RoverProvider): pass
