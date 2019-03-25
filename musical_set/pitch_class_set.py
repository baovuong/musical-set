import copy 
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

def to_valid(pitch_classes):
    return [p % 12 for p in pitch_classes]

def adjacency_list(pitch_classes):
    output = {}
    sorted_pitch_classes = sorted(pitch_classes)
    for i in range(len(sorted_pitch_classes)):
        output[sorted_pitch_classes[i]] = {}
        
        # get neighbors
        p = sorted_pitch_classes[(i-1) % len(sorted_pitch_classes)]
        n = sorted_pitch_classes[(i+1) % len(sorted_pitch_classes)]
        output[sorted_pitch_classes[i]][p] = interval_distance(sorted_pitch_classes[i], p)
        output[sorted_pitch_classes[i]][n] = interval_distance(sorted_pitch_classes[i], n)
    
    return output 

class PitchClassSet:

    def __init__(self, pitch_classes):
        
        # make pitch_classes valid
        self.pitch_classes = to_valid(pitch_classes)
    


    # public methods 
    def steps(self):
        total = 0
        for i in range(1, len(self.pitch_classes)):
            total += interval_distance(0, self.pitch_classes[i])
        return total 

    def interval_vector(self):
        # TODO work on this 
        pass

    def transpose(self, steps):
        return PitchClassSet([(p + steps) % 12 for p in self.pitch_classes])
    
    def invert(self):
        return PitchClassSet([(4 - p) % 12 for p in self.pitch_classes])
    
    def rotate(self, steps):
        return PitchClassSet(self.pitch_classes[steps:] + self.pitch_classes[:steps])
    
    def normal_order(self):
        
        if self.pitch_classes == None or len(self.pitch_classes) == 0:
            return copy.deepcopy(self) 
        
        # get rid of duplicates
        pitch_classes = list(dict.fromkeys(self.pitch_classes))

        # find largest interval
        intervals = set()
        ai = adjacency_list(self.pitch_classes)
        for key, value in ai.items():
            for k in value.keys():
                intervals.add(tuple(sorted((key, k))))
        
        interval_distances = [(sorted(i), interval_distance(i[0], i[1])) for i in intervals]
        interval_distances = sorted(interval_distances, key=lambda x: x[1], reverse=True)
        largest_interval = set(interval_distances[0][0])

        # rotate until the intervals are on each side
        normal_order = PitchClassSet(sorted(pitch_classes))

        while set([normal_order[0], normal_order[-1]]) != largest_interval:
            normal_order = normal_order.rotate(1)

        return normal_order 

    # TODO implement this
    def prime_form(self):
        # normal order
        prime = self.normal_order()
        
        # transpose to zero
        prime = prime.transpose(0 - prime[0])

        # invert
        inversion = prime.invert().normal_order()

        # transpose inversion to zero
        inversion = inversion.transpose(0 - inversion[0])

        # compare the two
        return prime if prime.steps() <= inversion.steps() else inversion  
    
    # magic methods 
    def __list__(self):
        return list(self.pitch_classes)
    
    def __tuple__(self):
        return tuple(self.pitch_classes)
    
    def __getitem__(self, key):
        return self.pitch_classes[key]
    
    def __len__(self):
        return len(self.pitch_classes)
