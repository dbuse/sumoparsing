"""
configurations to use with iterparse_plain_xml and iterparse_nested_xml

>>> iterparse_xml("some-tripinfo file.xml", 'tripinfo')
"""

import numpy as np

# add legacy aliases
xml_type_configs = {
    'detector_instant': {
        'tag': 'instantOut',
        'fields': {
            'id': str,
            'time': np.float64,
            'state': str,
            'vehID': str,
            'speed': np.float64,
            'length': np.float64,
            'type': str,
            'occupancy': np.float64,
            'gap': np.float64,
        },
        'timestep_fields': [],
        'categoricals': [
            'id',
            'state',
            'vehID',
            'type',
        ],
    },
    'detector_e1': {
        'tag': 'interval',
        'fields': {
            'id': str,
            'begin': np.float64,
            'end': np.float64,
            'nVehContrib': np.int32,
            'flow': np.float64,
            'occupancy': np.float64,
            'speed': np.float64,
            'length': np.float64,
            'nVehEntered': np.int32,
        },
        'timestepFields': [
            'begin',
            'end',
        ],
        'categoricals': [
            'id',
            'length',
        ],
    },
    'detector_e2': {
        'tag': 'interval',
        'fields': {
            'id': str,
            'begin': np.float64,
            'end': np.float64,
            'sampledSeconds': np.float64,
            'nVehEntered': np.int32,
            'nVehLeft': np.int32,
            'nVehSeen': np.int32,
            'meanSpeed': np.float64,
            'meanTimeLoss': np.float64,
            'meanOccupancy': np.float64,
            'meanMaxJamLengthInVehicles': np.float64,
            'meanMaxJamLengthInMeters': np.float64,
            'maxJamLengthInVehicles': np.float64,
            'maxJamLengthInMeters': np.float64,
            'jamLengthInVehiclesSum': np.float64,
            'jamLengthInMetersSum': np.float64,
            'meanHaltingDuration': np.float64,
            'maxHaltingDuration': np.float64,
            'haltingDurationSum': np.float64,
            'meanIntervalHaltingDuration': np.float64,
            'maxIntervalHaltingDuration': np.float64,
            'intervalHaltingDurationSum': np.float64,
            'startedHalts': np.float64,
            'meanVehicleNumber': np.float64,
            'maxVehicleNumber': np.int16,
        },
        'timestepFields': [
            'begin',
            'end',
        ],
        'categoricals': {
            'id': 'detector_e2_ids',
        },
    },
    'tlsstate': {
        'tag': 'tlsState',  # NOTE: might be tlsstate in older files
        'fields': {
            'time': np.float64,
            'id': str,
            'programID': str,
            'phase': np.int16,
            'state': str,
        },
        'timestep_fields': ['time'],
        'categoricals': {
            'id': 'tls_ids',
            'programID': 'tls_program_ids',
            'state': None,
        },
    },
    'tripinfo': {
        'tag': 'tripinfo',
        'fields': {
            'id': str,
            'depart': np.float64,
            'departLane': str,
            'departPos': np.float64,
            'departSpeed': np.float64,
            'departDelay': np.float64,
            'arrival': np.float64,
            'arrivalLane': str,
            'arrivalPos': np.float64,
            'arrivalSpeed': np.float64,
            'duration': np.float64,
            'routeLength': np.float64,
            'timeLoss': np.float64,
            'rerouteNo': np.int16,
            'vType': str,
            'speedFactor': np.float64,
            'vaporized': bool,
            'waitingTime': np.float64,
            'waitingCount': np.int16,
            'waitSteps': np.int32,
            # removed: device
        },
        'timestep_fields': [
            'depart',
            'arrival',
        ],
        'categoricals': {
            'id': 'vehicle_ids',
            'departLane': 'lane_ids',
            'arrivalLane': 'lane_ids',
            'vType': 'vTypes',
        },
    },
    'summary': {
        'tag': 'step',
        'fields': {
            'time': np.float64,
            'loaded': np.int32,
            'inserted': np.int32,
            'running': np.int16,
            'waiting': np.int16,
            'ended': np.int32,
            'meanWaitingTime': np.float64,
            'meanTravelTime': np.float64,
        },
        'timestep_fields': ['time'],
        'categoricals': {},
    },
    'floatingcar': {
        'tags': [
            'timestep',
            'vehicle',
        ],
        'fields': {
            'timestep': {
                'time': np.float64,
            },
            'vehicle': {
                'id': str,
                'type': str,
                'speed': np.float64,
                'angle': np.float64,
                'x': np.float64,
                'y': np.float64,
                'pos': np.float64,
                'lane': str,
                'slope': np.float64,
            }
        },
        'timestep_fields': ['time'],
        'categoricals': {
            'id': 'vehicle_ids',
            'type': 'vTypes',
            'lane': 'lane_ids',
        },
    },
    'routes': {
        'tags': [
            'vehicle',
            'route'
        ],
        'fields': {
            'vehicle': {
                'id': str,
                'type': str,
                'depart': np.float64,
                'departLane': str,
                'departPos': str,
                'departSpeed': np.float64,
                'arrivalLane': np.int8,
                'arrivalPos': str,
                'arrivalSpeed': np.float64,
            },
            'route': {
                'edges': lambda x: x.split(' '),
            },
        },
        'timestep_fields': ['depart'],
        'categoricals': {
            'id': 'vehicle_ids',
            'type': 'vTypes',
        },
    },
    'trips': {
        'tag': 'trip',
        'fields': {
            'id': str,
            'depart': np.float64,
            'from': str,
            'to': str,
            'via': str,
            'fromTaz': str,
            'toTaz': str,
            'color': str,
            'type': str,
            'departLane': str,
            'departPos': str,
            'departSpeed': str,
            'arrivalLane': str,
            'arrivalPos': str,
            'arrivalSpeed': str,
        },
        'timestep_fields': [],
        'categoricals': {
            'id': 'vehicle_ids',
            'type': 'vTypes',
            'color': 'color',
            'from': None,
            'to': None,
            'via': None,
            'fromTaz': None,
            'toTaz': None,
            'departLane': None,
            'arrivalLane': None,
        },
    },
    'emitter_vehicles': {
        'tag': 'vehicle',
        'fields': {
            'id': str,
            'type': str,
            'depart': np.float64,
            'departLane': str,
            'departPos': str,
            'departSpeed': np.float64,
            'route': str,
        },
        'timestep_fields': ['depart'],
        'categoricals': [
            'id',
            'type',
            'route',
            'departLane',
        ],
    },
    'vType': {
        'tag': 'vType',
        'fields': {
            'id': str,
            'vClass': str,
            'color': str,
        },
        'timestep_fields': [],
        'categoricals': [
            'id',
            'vClass',
            'color',
        ],

    },
    'conflict_graph_lanes': {
        'tags': [
            'junction',
            'approach',
            'lane',
        ],
        'fields': {
            'junction': {'id': {'newname': 'junction_id', 'func': str}},
            'approach': {'id': {'newname': 'approach_id', 'func': np.int8}},
            'lane': {'id': {'newname': 'lane_id', 'func': str}},
        },
        'timestep_fields': [],
        'categoricals': ['junction'],
    },
    # custom format -- not part of SUMO
    'conflict_graph_inferior': {
        'tags': [
            'junction',
            'approach',
            'inferior',
        ],
        'fields': {
            'junction': {'id': {'newname': 'junction_id', 'func': str}},
            'approach': {'id': {'newname': 'approach_id', 'func': np.int8}},
            'inferior': {'other': {'newname': 'inferior_id', 'func': np.int8}},
        },
        'timestep_fields': [],
        'categoricals': ['junction'],
    },
    'tls_mapping': {
        'tags': [
            'junction',
            'detector',
        ],
        'fields': {
            'junction': {
                'city_nr': {'newname': 'junction_id_city', 'func': str},
                'sumo_id': {'newname': 'junction_id_sumo', 'func': str},
                'name': str,
            },
            'detector': {
                'city_id': {'newname': 'detector_id_city', 'func': str},
                'sumo_id': {'newname': 'detector_id_sumo', 'func': str},
                'city_name': {'newname': 'detector_name_city', 'func': str},
            },
        },
        'timestep_fields': [],
        'categoricals': [
            'junction_id_city',
            'junction_id_sumo',
            'name',
            'detector_id_city',
            'detector_id_sumo',
        ],
    },
}
xml_type_configs['phased-e2-output'] = xml_type_configs['detector_e2']
xml_type_configs['phased-switches'] = xml_type_configs['tlsstate']
