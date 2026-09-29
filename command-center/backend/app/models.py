from datetime import datetime, timezone
from typing import Literal, Any
from pydantic import BaseModel, Field, ConfigDict, field_validator

def now(): return datetime.now(timezone.utc).isoformat()
class Model(BaseModel):
    model_config = ConfigDict(extra='forbid', allow_inf_nan=False)
    @field_validator('*')
    @classmethod
    def timestamps(cls,value,info):
        if info.field_name in ('timestamp','last_seen','last_heartbeat','recovery_started') and value is not None:
            parsed=datetime.fromisoformat(value.replace('Z','+00:00'))
            if parsed.tzinfo is None: raise ValueError('Timestamp must include timezone')
        return value
class Vec3(Model):
    x: float = 0; y: float = 0; z: float = 0
class Zone(Model):
    checkpoint: str | None = None
    start_relay: str | None = None
    end_relay: str | None = None
class Rover(Model):
    timestamp: str = Field(default_factory=now)
    mode: str = 'UNKNOWN'
    mission_state: str = 'WAITING'
    position: Vec3
    orientation: float
    velocity_linear: float
    velocity_angular: float
    battery: float = Field(ge=0, le=100)
    connectivity: str = 'WAITING'
    primary_link: str = 'WAITING'
    lora_link: str = 'WAITING'
    slam_status: str = 'WAITING'
    localization_status: str = 'WAITING'
    nav2_status: str = 'WAITING'
    current_goal: Vec3 | None = None
    distance_to_goal: float
    relay_nodes_remaining: int = Field(ge=0)
    sensors: dict[str,str] = Field(default_factory=dict)
    health: dict[str,float | str] = Field(default_factory=dict)
class Worker(Model):
    worker_id: str = Field(pattern=r'^W[0-9]{2,4}$')
    heart_rate: float | None = Field(default=None, ge=0, le=250)
    spo2: float | None = Field(default=None, ge=0, le=100)
    temperature: float | None = None
    humidity: float | None = Field(default=None, ge=0, le=100)
    mq4: float | None = None
    mq135: float | None = None
    fall: bool = False
    sos: bool = False
    state: Literal['NORMAL','WARNING','EMERGENCY'] = 'NORMAL'
    last_seen: str = Field(default_factory=now)
    communication_status: str = 'CONNECTED'
    last_checkpoint: str | None = None
    zone_start_relay: str | None = None
    zone_end_relay: str | None = None
    rssi: float | None = None
class Reading(Model):
    value: float | None = None
    unit: str
    severity: Literal['SAFE','WARNING','CRITICAL','UNAVAILABLE'] = 'UNAVAILABLE'
    sensor: str
    timestamp: str = Field(default_factory=now)
class Environment(Model):
    readings: dict[str,Reading]
class Thermal(Model):
    timestamp: str = Field(default_factory=now)
    values: list[float] = Field(min_length=64,max_length=64)
    ambient: float
    interpretation: str = 'Unassessed'
    confidence: float | None = Field(default=None,ge=0,le=1)
class Detection(Model):
    detection_id: str
    timestamp: str = Field(default_factory=now)
    classification: Literal['person','blocked_passage','obstruction','water','smoke','fire','equipment']
    confidence: float = Field(ge=0,le=1)
    bounding_box: list[float] = Field(min_length=4,max_length=4)
    distance: float | None = None
    world_position: Vec3 | None = None
    thermal_confirmation: bool = False
    severity: str = 'WARNING'
    image_reference: str | None = None
    status: str = 'ACTIVE'
class Assessment(Model):
    timestamp: str = Field(default_factory=now)
    state: str
    trigger: str
    observations: list[str]
    decision: str
    action: str
    next_check: str
    model: str = 'UNCONFIGURED'
    fps: float | None = None
    latency_ms: float | None = None
    trained_classes: list[str] = Field(default_factory=list)
class Marker(Model):
    id: str
    type: Literal['VICTIM','GAS_HAZARD','THERMAL_ANOMALY','WATER','BLOCKED_PASSAGE','WORKER_ZONE','RELAY','NETWORK_BREAK','BYPASS_NODE','POINT_OF_INTEREST']
    timestamp: str = Field(default_factory=now)
    position: Vec3 | None = None
    zone: Zone | None = None
    severity: str = 'INFORMATION'
    description: str
    source: str
    confidence: float | None = Field(default=None,ge=0,le=1)
    status: str = 'ACTIVE'
class Node(Model):
    id: str; role: str; position: Vec3
    status: str = 'ONLINE'
    signal: float | None = None
    latency: float | None = None
    last_heartbeat: str = Field(default_factory=now)
class Link(Model):
    source: str; target: str; status: str = 'HEALTHY'
    kind: str = 'BROADBAND'
class Network(Model):
    nodes: list[Node]
    links: list[Link]
    status: str = 'HEALTHY'
    failed_segment: str | None = None
    recovery_step: int = Field(default=0,ge=0,le=8)
    recovery_started: str | None = None
    recovery_duration: float = 0
    deployment: str = 'IDLE'
    deployed: int = 0
class Path(Model):
    points: list[Vec3] = Field(max_length=10000)
    frame_id: str = 'map'
    kind: Literal['planned','trail','return_path','frontier'] = 'planned'
class PointCloud(Model):
    frame_id: str = 'map'
    sequence: int = Field(ge=0)
    xyz: list[float] = Field(max_length=150000)
    replace: bool = False
class Occupancy(Model):
    width: int = Field(ge=1,le=512)
    height: int = Field(ge=1,le=512)
    resolution: float = Field(gt=0,le=10)
    origin: Vec3
    cells: list[int] = Field(max_length=262144)
    frame_id: str = 'map'
class MapData(Model):
    frame_id: str = 'map'
    tunnels: list[list[Vec3]] = Field(default_factory=list)
    planned: list[Vec3] = Field(default_factory=list)
    trail: list[Vec3] = Field(default_factory=list)
    return_path: list[Vec3] = Field(default_factory=list)
    frontier: list[Vec3] = Field(default_factory=list)
    markers: list[Marker] = Field(default_factory=list)
    cloud: list[float] = Field(default_factory=list)
    explored: float = 0
    occupancy: Occupancy | None = None
class Video(Model):
    rgb_url: str | None = None
    depth_url: str | None = None
    protocol: Literal['MJPEG','VIDEO','WEBRTC_GATEWAY'] = 'MJPEG'
    nearest_obstacle: float | None = None
    target_distance: float | None = None
    timestamp: str = Field(default_factory=now)
class ModeRequest(Model): mode: Literal['DEMO','REAL']
class Command(Model):
    action: Literal['PAUSE','RESUME','STOP','RETURN_TO_BASE','ALL_CLEAR','NAVIGATE_TO','DEPLOY_RELAY','ACKNOWLEDGE_ALERT']
    confirmed: bool = False
    goal: Vec3 | None = None
    alert_id: str | None = None
class DemoRequest(Model):
    action: Literal['NORMAL_MISSION','DETECT_VICTIM','GAS_LEAK','WORKER_SOS','WORKER_FALL','NETWORK_BREAK','START_NETWORK_RECOVERY','DEPLOY_RELAY','RESTORE_NETWORK','COMMUNICATION_LOSS','LORA_FALLBACK','RETURN_TO_BASE','PLAY','PAUSE','RESET','STEP']
class Event(Model):
    type: str
    timestamp: str = Field(default_factory=now)
    source: str
    data_mode: Literal['DEMO','REAL']
    payload: Any
