
import tracking

#import simplejson as _json
#with open('signage.json') as _json_data:
#    _d = _json.load(_json_data)
#
#def _get_data():
#    return _d

#test_data_dicts = [
#            {'no_faces': 3,
#             'windows': "100,100,200,200,562,99,883,420,1,11,271,219",
#             'image_id': 'epoch_time',
#             'camera_id': 'camera-1',
#             'id': 176,
#             'date_created': 1532538996.0 }
#        ,   {'no_faces': 2,
#             'windows': "100,100,200,200,1,11,271,219",
#             'image_id': 'epoch_time',
#             'camera_id': 'camera-1',
#             'id': 176,
#             'date_created': 1532538999.0 }
#        ,   {  "windows": ""
#             , "image_id": "image_id"
#             , "location": "mac"
#             , "camera_id": "camera-1\r"
#             , "date_created": 1533227762.0
#             , "id": 1310
#             , "no_faces": 0}
#             ]

test_data = [
            {"windows": "", "image_id": "image_id", "location": "mac", "camera_id": "camera-1\r", "date_created": 1533227583.0, "id": 1140, "no_faces": 0}
        ,   {"windows": "", "image_id": "image_id", "location": "mac", "camera_id": "camera-1\r", "date_created": 1533227584.0, "id": 1141, "no_faces": 0}
        ,   {"windows": "", "image_id": "image_id", "location": "mac", "camera_id": "camera-1\r", "date_created": 1533227585.0, "id": 1142, "no_faces": 0}
        ,   {"windows": "", "image_id": "image_id", "location": "mac", "camera_id": "camera-1\r", "date_created": 1533227587.0, "id": 1143, "no_faces": 0}
        ,   {"windows": "", "image_id": "image_id", "location": "mac", "camera_id": "camera-1\r", "date_created": 1533227588.0, "id": 1144, "no_faces": 0}
        ,   {"windows": "", "image_id": "image_id", "location": "mac", "camera_id": "camera-1\r", "date_created": 1533227590.0, "id": 1145, "no_faces": 0}
        ,   {"windows": "", "image_id": "image_id", "location": "mac", "camera_id": "camera-1\r", "date_created": 1533227591.0, "id": 1146, "no_faces": 0}
        ,   {"windows": "348,241,669,562", "image_id": "image_id", "location": "mac", "camera_id": "camera-1\r", "date_created": 1533227749.0, "id": 1298, "no_faces": 1}
        ,   {"windows": "348,241,669,562", "image_id": "image_id", "location": "mac", "camera_id": "camera-1\r", "date_created": 1533227750.0, "id": 1299, "no_faces": 1}
        ,   {"windows": "348,241,669,562", "image_id": "image_id", "location": "mac", "camera_id": "camera-1\r", "date_created": 1533227753.0, "id": 1300, "no_faces": 1}
        ,   {"windows": "312,241,633,562", "image_id": "image_id", "location": "mac", "camera_id": "camera-1\r", "date_created": 1533227755.0, "id": 1301, "no_faces": 1}
        ,   {"windows": "974,290,1359,675", "image_id": "image_id", "location": "mac", "camera_id": "camera-1\r", "date_created": 1533227757.0, "id": 1302, "no_faces": 1}
        
            ]

object_log = tracking.track_objects(test_data)

from pprint import pprint
pprint(object_log)



