"""
    Object Tracking Algorithm

    Input: JSON containing a timestamp and list of bounding boxes for objects.

    Object tracking is performed with only a short active history. 
    No momentum or long-term modelling is performed.
    Tracking Parameters:
      * iou_threshold   - scaler on matching sensitivity to location
      * momentum_scale  - scaler on matching sensitivity to speed
      * max_frames      - maximum number of frames to track an entity
      * min_seconds     - minimum time in seconds to track a new entity

    Output: log of objects tracked with a lifetime over min_seconds threshold.
"""

import time as _time
from datetime import datetime as _datetime
import math as _math

class ObjectTracker:
    """ Manages identification and tracking of objects
        from a single view across multiple frames over time. """
    
    def __init__(self):
        self.active = []
        self.object_log = []

        ### Object matching parameters
        self.iou_threshold = 0.8
        self.momentum_scale = 1.0

        ### Environment Model # alternate matching at obstruction and view boundaries
        self.activity_boundaries = []
        self.obstructions = []

        ### Define recent active history
        self.max_frames = 150

        ### Minimum lifetime required for output logging
        self.min_seconds = 1

    def get_id(self):
        taken = set([obj.id for frame in self.active for obj in frame.objects if obj.id is not None])
        #print("taken ids: {}".format(','.join([str(name) for name in taken])))   
        for i in range(100,1000,100):
            #print("checking ids from {} to {}".format(i-100,i))
            new = set(range(i-100,i))
            free = list(new-taken)
            if len(free) > 0:
                return free[0]
            
    def momentum_match(self,objA,objB):
        """ Given two TrackedObjects, return Boolean match based on movement.
            Default of lack of data is no match. """
        if not (objA.speed and objB.speed):
            return False
        return abs( objA.speed - objB.speed ) < self.momentum_scale            

    def location_match(self,objA,objB):
        """ Given two TrackedObjects, return Boolean match based on location.
            Default of lack of data is no match. """
        boxA = objA.coords
        boxB = objB.coords
        try:
            xA = max(boxA[0], boxB[0])
            yA = max(boxA[1], boxB[1])
            xB = min(boxA[2], boxB[2])
            yB = min(boxA[3], boxB[3])
            
            interArea = max(0,xB-xA+1) * max(0,yB-yA+1)
            boxAArea = (boxA[2] - boxA[0] + 1) * (boxA[3] - boxA[1] + 1)
            boxBArea = (boxB[2] - boxB[0] + 1) * (boxB[3] - boxB[1] + 1)
            iou = interArea / float(boxAArea + boxBArea - interArea)
            if iou>self.iou_threshold:
                return True
        except:
            pass
        return 0


    def frame_update(self,frameA,frameB):
        """ frameB is updated to match objects from frameA. """
        #print("comparing {} new objects with {} old objects".format(len(frameB.new_objects),len(frameA.objects)))
        no_matches = []
        
        # First pass using momentum factors
        for obja in frameA.objects:
            for objb in frameB.new_objects:
                if self.momentum_match(obja,objb):
                    objb.observe(obja)
        
        # Second pass using location
        for obja in frameA.objects:
            for objb in frameB.new_objects:
                if self.location_match(obja,objb):
                    objb.observe(obja)
        
        return frameB


    def process_new_frame(self,new_frame):
        """ new_frame must have 0 or more boxes in it.
            Update active frames and list of objects present in new frame. """
        if new_frame.get("no_faces") == 0:
            return []

        new_frame = _Frame(new_frame,self)

        for active_frame in self.active:
            new_frame = self.frame_update(active_frame,new_frame)
            if len(new_frame.new_objects) == 0:
                break

        self.active.append(new_frame)

        if len(self.active) > self.max_frames:
            retiring = self.active[:-(self.max_frames+1)]
            self.active = self.active[-(self.max_frames+1):]
            for frame in retiring:
                self.log_objects(frame)

    def close(self):
        """ close out active frames and log their objects """
        self.active.reverse()
        while self.active:
            _frame = self.active.pop()
            self.log_objects(_frame)

    def log_objects(self,frame):
        """ log objects which are not present in active frames """
        obj_ids = [obj.id for obj in frame.objects]
        exc_ids = [obj.id for _frame in self.active for obj in _frame.objects]
        new_object_ids = list(set(obj_ids) - set(exc_ids))

        for obj in frame.objects:
            if obj.id in new_object_ids and obj.time_alive >= self.min_seconds:
                self.object_log.append(obj)

                
class _Frame:
    objects = None

    @property
    def new_objects(self):
        return [obj for obj in self.objects if obj.new_observation]    

    def __init__(self,frame_dict,tracker):
        self.timestamp = float(frame_dict['date_created'])
        self.face_count = int(frame_dict['no_faces'])
        self.objects = [TrackedObject(bbox,self.timestamp,tracker.get_id()) for bbox in self._convert_to_frame_of_boxes(frame_dict['windows']) ]

    def _convert_to_frame_of_boxes(self,array):
        """ for any-lenth array or list, give a list of tuples where each tuple is length 4"""
        #print("   input array {}".format(array))
        if type(array) == str:
            array = array.split(',')
        if len(array) <4:
            return []
        output = []
        unfinished = []
        for item in array:
            unfinished.append(int(item))
            if len(unfinished) == 4:
                output.append(unfinished)
                unfinished = []
        return output

    def __repr__(self):
        report = "frame with {} objects".format(len(self.objects))
        for obj in self.objects:
            report += "\n    "+str(obj)
        return report

class _Footprint:
    @property
    def isotimestamp(self):
        return _datetime.utcfromtimestamp(self.timestamp).isoformat()
    
    def __init__(self,coords,timestamp):
        self.coords=coords
        self.timestamp=timestamp
        
    def __lt__(self,other):
        return self.timestamp < other.timestamp
    
    def __gt__(self,other):
        return self.timestamp > other.timestamp
    
    def __eq__(self,other):
        return self.timestamp == other.timestamp and self.coords == other.coords
    
    def __ne__(self,other):
        return self.timestamp != other.timestamp or self.coords != other.coords
        
    def __le__(self,other):
        return self.timestamp <= other.timestamp
    
    def __ge__(self,other):
        return self.timestamp >= other.timestamp
        
    def __cmp__(self,other):
        return self.timestamp.__cmp__(other)
    
    def __repr__(self):
        return f"{self.isotimestamp}" + " (" + ','.join([str(x) for x in self.coords]) + ")"

class TrackedObject:
    """ Class represents an object/face located in a Frame """
    
    @property
    def date_created(self):
        return self.tracks[0].timestamp
    
    @property
    def end_time(self):
        return self.tracks[-1].timestamp
    
    @property
    def time_alive(self):
        return int(self.end_time - self.date_created)

    @property
    def speed(self):
        def centroid(coords):
            y1,x1,y2,x2 = coords
            return (y1+(y2-y1)/2 , x1+(x2-x1)/2)
        
        if self.end_time == self.date_created:
            return None
        if not self.coords:
            return None
        else:
            start = self.tracks[0].coords
            end = self.tracks[-1].coords
            
            t0 = self.tracks[0].timestamp
            t1 = self.tracks[-1].timestamp
            
            return _math.sqrt( (end[0]-start[0])**2 + (end[1]-start[1])**2 ) / (t1-t0)

    def __init__(self,coords,date_created,oid):
        self.coords = coords
        self.id = oid
        self.new_observation = True
        self.tracks = [_Footprint(coords,date_created)]
        

    def observe(self,other_obj):
        """update this object with a previous observation.
           equivalent to merge of the two objects.
           do nothing if both have been merged already."""
        if not self.new_observation and not other_obj.new_observation:
            return
        
        if other_obj.date_created < self.date_created:
            self.new_observation = False
            self.id = other_obj.id
        else:
            other_obj.new_observation = False
            other_obj.id = self.id
            
        tracks = other_obj.tracks + self.tracks
        tracks.sort()
        self.tracks = other_obj.tracks = tracks

            
    def __repr__(self):
        report = "id: {} - coords: {}".format(self.id,','.join([str(x) for x in self.coords]))
        report += "\n  lived {} secs ({} to {})".format(self.time_alive,self.date_created,self.end_time)
        report += "\n  tracks: {}".format(self.tracks)
        report += "\n"
        return report


    def __iter__(self):
        yield ('latest_coords' , self.latest_coords)
        yield ('date_created'  , self.date_created)
        yield ('end_time'      , self.end_time)
        yield ('time_alive'    , self.time_alive)

    
def track_objects(json_data):
    tracker = ObjectTracker()

    for frame in json_data:
        tracker.process_new_frame(frame)

    tracker.close()

    return tracker.object_log


