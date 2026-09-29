"""Deterministic simulated data. Never loaded by real-mode producers."""
import math
from ..models import *
def p(x,z,y=0): return {'x':x,'y':y,'z':z}
ROUTE=[p(x,0) for x in range(0,25,2)]+[p(24,z) for z in range(2,19,2)]+[p(x,18) for x in range(26,49,2)]
class MockRoverTelemetryProvider:
    @staticmethod
    def initial():
        sensors={x:'ONLINE' for x in ['lidar','depth_camera','night_camera','thermal','gas','imu','esp32','motor_controller','watchdog','lora','relay_mechanism']};sensors['water']='WAITING'
        return Rover(mode='AUTONOMOUS',orientation=0,velocity_linear=.18,velocity_angular=0,battery=78,connectivity='CONNECTED',primary_link='CONNECTED',lora_link='STANDBY',slam_status='ACTIVE',localization_status='TRACKING',nav2_status='ACTIVE',distance_to_goal=8.4,relay_nodes_remaining=3,position=Vec3(x=8),current_goal=Vec3(x=48,z=18),sensors=sensors,mission_state='AUTONOMOUS EXPLORE',health={'CPU %':43,'RAM %':58,'Temperature °C':54,'Storage %':21,'AI load %':37,'Throughput Mbps':8.2,'ROS':'ONLINE'}).model_dump()
class MockWorkerTelemetryProvider:
    @staticmethod
    def initial():
        return [Worker(worker_id=f'W{i:02}',heart_rate=76+i,spo2=98,temperature=28+i/10,humidity=65,mq4=210+i,mq135=145+i,last_checkpoint=f'CP-{i:02}',zone_start_relay=f'R{min(i,3)}',zone_end_relay=f'R{min(i+1,4)}',rssi=-65-i*3).model_dump() for i in range(1,7)]
class MockMapProvider:
    @staticmethod
    def initial():
        cloud=[]
        for x in range(49):
            z0=0 if x<=24 else 18
            for a in range(0,360,12):
                t=math.radians(a);cloud += [float(x),1.5+1.6*math.sin(t),z0+2*math.cos(t)]
        for z in range(19):
            for a in range(0,360,12):
                t=math.radians(a);cloud += [24+2*math.cos(t),1.5+1.6*math.sin(t),float(z)]
        return MapData(tunnels=[[Vec3(x=0),Vec3(x=24),Vec3(x=24,z=18),Vec3(x=48,z=18)],[Vec3(x=12),Vec3(x=12,z=-12)]],planned=ROUTE,frontier=[p(48,18)],cloud=cloud,explored=.35,markers=[Marker(id='OBS-01',type='BLOCKED_PASSAGE',position=Vec3(x=12,z=-10),description='Rockfall / branch blocked',source='DEMO',severity='WARNING')]).model_dump()
class MockAIProvider:
    @staticmethod
    def initial(): return Assessment(state='AUTONOMOUS EXPLORE',trigger='Frontier F-07 selected',observations=['Path traversable','No flooding detected','Low-light mode active'],decision='Inspect eastern passage',action='Follow planned route',next_check='Continuous obstacle monitoring',model='YOLO • simulated inference',fps=6.8,latency_ms=147,trained_classes=['person','obstruction']).model_dump()
class MockEnvironmentProvider:
    @staticmethod
    def initial():
        return {k:Reading(value=v,unit=u,sensor=s,severity='SAFE' if v is not None else 'UNAVAILABLE').model_dump() for k,v,u,s in [('Methane',238,'ADC','MQ-4 • uncalibrated'),('Carbon monoxide',120,'ADC','MQ-7 • uncalibrated'),('Oxygen',None,'%','Not installed'),('Temperature',28.4,'°C','Demo sensor'),('Humidity',67,'%','Demo sensor'),('Pressure',1008,'hPa','Demo sensor'),('Water',None,'','Not installed'),('Air quality',156,'ADC','MQ135 • uncalibrated')]}
class MockThermalProvider:
    @staticmethod
    def initial():return Thermal(values=[27.4+.6*math.sin(i) for i in range(64)],ambient=27.4,interpretation='No correlated anomaly').model_dump()
class MockNetworkTopologyProvider:
    @staticmethod
    def initial():
        ids=['BASE','R1','R2','R3','R4','R01']; positions=[p(0,0),p(8,0),p(20,0),p(24,8),p(32,18),p(40,18)]
        return Network(nodes=[Node(id=id,role='Base station' if id=='BASE' else 'Rover' if id=='R01' else 'Relay',position=positions[i],signal=-45-i*6,latency=2+i*4) for i,id in enumerate(ids)],links=[Link(source=ids[i],target=ids[i+1]) for i in range(5)]).model_dump()
class MockVideoProvider:
    @staticmethod
    def initial():return Video(nearest_obstacle=1.82,target_distance=4.63).model_dump()
class MockPointCloudProvider(MockMapProvider): pass
