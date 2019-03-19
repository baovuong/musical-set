import itertools 

notes = ('C', 'C#', 'D', 'D#', 'E', 'F', 'G', 'G#', 'A', 'A#', 'B')

def interval_distance(p1, p2):
    distance = abs(p1 - p2)

    if distance > 6:
        if distance <= 12:
            return 12 % distance 
        else: 
            return distance % 12

    return distance 

def is_valid_pitch_set(pitch_set):
    # make sure all values are between 0 (inclusive) and 12 (exclusive)
    return len([p for p in pitch_set if p >= 0 and p < 12]) == len(pitch_set)

def to_valid_pitch_set(pitch_set):
    return tuple(p % 12 for p in pitch_set)

def transpose(pitch_set, steps):
    return tuple((p + steps) % 12 for p in pitch_set)

def rotate(pitch_set, steps):
    return pitch_set[steps:] + pitch_set[:steps]

def normal(pitch_set):

    if pitch_set == None or len(pitch_set) == 0:
        return pitch_set
    
    # make sure it valid
    valid_pitch_set = to_valid_pitch_set(pitch_set)

    # find largest interval
    intervals = itertools.combinations(valid_pitch_set, 2)
    interval_distances = [(i, interval_distance(i[0], i[1])) for i in intervals]
    interval_distances = sorted(interval_distances, key=lambda x: x[1], reverse=True)
    largest_interval = interval_distances[0]

    # rotate until the intervals are on each side
    normal_form = sorted(valid_pitch_set)
    while normal_form[0] == largest_interval[0] and normal_form[len(normal_form) - 1] == largest_interval[1]:
        normal_form = rotate(normal_form, 1)

    return normal_form 


    

def prime(pitch_set):
    pass 
