import unittest 

from musical_set.pitch_set import (interval_distance, 
                                   is_valid_pitch_set, 
                                   to_valid_pitch_set, 
                                   transpose, 
                                   rotate, 
                                   normal)

from ddt import ddt, data, unpack

@ddt 
class TestPitchSetFunctions(unittest.TestCase):


    @data(
        (5, 0, 5), 
        (5, 5, 0), 
        (5, 0, 7)
    )
    @unpack 
    def test_interval_distance_success_equal(self, expected, interval1, interval2):
        actual = interval_distance(interval1, interval2)
        self.assertEqual(expected, actual)
    
    @data(
        (7, 0, 7)
    )
    @unpack
    def test_interval_distance_notequal(self, expected, interval1, interval2):
        actual = interval_distance(interval1, interval2)
        self.assertNotEqual(expected, actual)

    @data(
        [0, 1, 4],
        [1, 2, 3]
    )
    def test_is_valid_pitch_set_true(self, p):
        self.assertTrue(is_valid_pitch_set(p))
        
    @data(
        [-1, 0, 3]
    )
    def test_is_valid_pitch_set_false(self, p):
        self.assertFalse(is_valid_pitch_set(p))
    
    @data(
        ([-1, 0, 3], [11, 0, 3]),
        ([12], [0])
    )
    @unpack
    def test_to_valid_pitch_set(self, input_set, expected):
        actual = to_valid_pitch_set(input_set)
        self.assertEqual(expected, actual)
        
    @data(
        ([0, 1, 2], 1, [1, 2, 3]),
        ([10, 11, 0], 1, [11, 0, 1]),
        ([1, 3, 6, 7], 12, [1, 3, 6, 7]),
        ([3, 2, 3], -1, [2, 1, 2]),
        ([0, 3, 10], -3, [9, 0, 7])
    )
    @unpack
    def test_transpose(self, input_set, steps, expected):
        actual = transpose(input_set, steps)
        self.assertEqual(expected, actual)
    
    @data(
        ([0, 1, 2], 1, [1, 2, 0]),
        ([0, 1, 2], 2, [2, 0, 1])
    )
    @unpack
    def test_rotate(self, p, s, expected):
        actual = rotate(p, s)
        self.assertEqual(expected, actual)
        
        
    @data(
        ([7, 4, 0], [0, 4, 7]),
        ([4, 7, 2, 4], [2, 4, 7]),
        ([5, 7, 2, 5], [2, 5, 7])
    )
    @unpack 
    def test_normal(self, input_set, expected):
        actual = normal(input_set)
        self.assertEqual(expected, actual)
        