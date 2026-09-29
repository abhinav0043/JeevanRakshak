import uuid, copy
from ..models import now, Event
from ..providers.mock import *
class State:
    def __init__(self,db):
        self.db=db; self.clients=set(); self.pending=[]; self.reset('DEMO')
    def reset(self,mode):
        if hasattr(self,'data'):
            self.db.save(self.data['mission_id'],self.data); self.db.end(self.data['mission_id'])
        self.pending.clear();self.cloud_revision=0
        id=str(uuid.uuid4())
        self.data={'mission_id':id,'mission_active':True,'started':now(),'timestamp':now(),'data_mode':mode,'rover':None,'workers':[],'environment':{},'thermal':None,'ai':None,'detections':[],'network':None,'map':MapData().model_dump(),'video':None,'alerts':[],'timeline':[],'scenario':{'step':0,'playing':False,'label':'Ready to demonstrate'},'stop_latched':False}
        self.db.start(id,mode)
        if mode=='DEMO':
            for key,provider in [('rover',MockRoverTelemetryProvider),('workers',MockWorkerTelemetryProvider),('environment',MockEnvironmentProvider),('thermal',MockThermalProvider),('ai',MockAIProvider),('network',MockNetworkTopologyProvider),('map',MockMapProvider),('video',MockVideoProvider)]: self.data[key]=provider.initial()
        self.log('SYSTEM','Mission started • '+mode)
    def emit(self,type,payload,source='R01'):
        e=Event(type=type,payload=copy.deepcopy(payload),source=source,data_mode=self.data['data_mode']).model_dump()
        self.db.add(self.data['mission_id'],e);self.pending.append(e)
        return e
    def log(self,source,description,severity='INFORMATION'):
        item={'id':str(uuid.uuid4()),'timestamp':now(),'source':source,'description':description,'severity':severity}
        self.data['timeline']=[item]+self.data['timeline'][:199];self.emit('mission.event',item,source)
    def alert(self,source,description,severity='WARNING',zone='R01 current pose',marker_id=None):
        item={'id':str(uuid.uuid4()),'timestamp':now(),'source':source,'description':description,'severity':severity,'zone':zone,'acknowledged':False,'marker_id':marker_id}
        self.data['alerts']=[item]+self.data['alerts'][:199];self.emit('alert.created',item,source); self.log(source,description,severity)
    def marker(self,type,description,severity='WARNING',position=None,zone=None):
        pos=None if zone else position or (self.data['rover']['position'] if self.data['rover'] else None)
        m=Marker(id=str(uuid.uuid4()),type=type,position=pos,zone=zone,description=description,source='R01 / DEMO' if self.data['data_mode']=='DEMO' else 'R01',severity=severity).model_dump()
        self.data['map']['markers'].append(m);self.emit('map.marker',m);return m['id']
    def snapshot(self):
        self.data['timestamp']=now();return copy.deepcopy(self.data)
