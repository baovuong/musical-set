import copy 
import itertools 

notes = ('C', 'C#', 'D', 'D#', 'E', 'F', 'G', 'G#', 'A', 'A#', 'B')

def get_interval(p1, p2):
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
        output[sorted_pitch_classes[i]][p] = get_interval(sorted_pitch_classes[i], p)
        output[sorted_pitch_classes[i]][n] = get_interval(sorted_pitch_classes[i], n)
    
    return output 

def rotate(pitch_classes, steps):
    return pitch_classes[steps:] + pitch_classes[:steps]

class PitchClassSet:

    def __init__(self, pitch_classes):
        
        # make pitch_classes valid
        self.pitch_classes = to_valid(pitch_classes)

    # public methods 
    def interval_vector(self): 
        vector = {}
        pairs = itertools.combinations(self.pitch_classes, 2)
        for p in pairs:
            interval = get_interval(p[0], p[1])
            if not interval in vector:
                vector[interval] = 1
            else:
                vector[interval] += 1
        return vector 
    
    def interval_sum(self):
        iv = self.interval_vector()
        return sum([k*v for k,v in iv.items()])
    
    def transpose(self, steps):
        return PitchClassSet([(p + steps) % 12 for p in self.pitch_classes])
    
    def invert(self):
        return PitchClassSet([(4 - p) % 12 for p in self.pitch_classes])
    
    def rotate(self, steps):
        return PitchClassSet(rotate(self.pitch_classes, steps))
    
    def normal_order(self):
        
        if self.pitch_classes == None or len(self.pitch_classes) == 0:
            return copy.deepcopy(self) 
        
        # get rid of duplicates
        pitch_classes = list(dict.fromkeys(self.pitch_classes))

        # find largest interval
        pitches = set()
        ai = adjacency_list(self.pitch_classes)
        for key, value in ai.items():
            for k in value.keys():
                pitches.add(tuple(sorted((key, k))))
        
        intervals = [(sorted(p), get_interval(p[0], p[1])) for p in pitches]
        intervals = sorted(intervals, key=lambda x: x[1], reverse=True)
        largest_intervals = set([tuple(i[0]) for i in intervals if i[1] == intervals[0][1]])
        largest_intervals = [set(i) for i in largest_intervals]


        possible_normal_orders = []
        current_possibility = PitchClassSet(sorted(pitch_classes))
        for i in range(len(pitch_classes)):
            checked = [li for li in largest_intervals if len(set([current_possibility[0], current_possibility[-1]]).intersection(li)) == 2]
            if len(checked) > 0:
                possible_normal_orders.append(current_possibility)
            current_possibility = current_possibility.rotate(1)

        
        def normal_order_sorting(x):
            # first transpose them down to 0
            t = x.transpose(0 - x[0])
            return t[-2]
        
        sorted(possible_normal_orders, key=normal_order_sorting)
        return possible_normal_orders[0]

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
        return prime if prime.__root_steps() <= inversion.__root_steps() else inversion  
    
    # private methods 
    def __root_steps(self):
        return sum([self.pitch_classes[i] - self.pitch_classes[0] for i in range(1, len(self.pitch_classes))])

    # magic methods 
    def __list__(self):
        return list(self.pitch_classes)
    
    def __tuple__(self):
        return tuple(self.pitch_classes)
    
    def __getitem__(self, key):
        return self.pitch_classes[key]
    
    def __len__(self):
        return len(self.pitch_classes)
