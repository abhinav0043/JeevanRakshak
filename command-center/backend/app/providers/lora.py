from ..models import Worker
class LoRaWorkerProvider:
    """Parses wearable packets; does not infer a location from RSSI."""
    @staticmethod
    def parse(packet: str, **metadata) -> Worker:
        parts=packet.strip().split(','); data=dict(p.split('=',1) for p in parts[1:])
        out={'worker_id':parts[0],**metadata}
        for key,name in {'HR':'heart_rate','SPO2':'spo2','TEMP':'temperature','HUM':'humidity','MQ4':'mq4','MQ135':'mq135'}.items():
            if key in data: out[name]=float(data[key])
        for key in ['FALL','SOS']:
            if data.get(key,'0') not in ['0','1']: raise ValueError('Invalid boolean')
            out[key.lower()]=data.get(key)=='1'
        out['state']='EMERGENCY' if out['fall'] or out['sos'] else data.get('STATE','NORMAL')
        return Worker(**out)
