

# Object Tracking

Simple object tracking for computer vision.

### Features

Object tracking based on parameterized identity decision:

  * IoU, Intersection-over-Union thresholding
  * Time between object observation
  * Frames between object observation

## Usage

  * Input: json log of detected objects and their bounding boxes
  * Output: list of json-able objects identified in the log history

```
    import tracking

    data = json.load(json_data)
    object_log = tracking.track_objects(data)
    output_json = [obj.to_json() for obj in object_log]
```

## Roadmap

  1. momentum modelling
  2. use object class information in identity function
