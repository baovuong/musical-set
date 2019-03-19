import unittest 

from musical_set import pitch_set

from ddt import ddt, data, unpack

@ddt 
class TestPitchSetFunctions(unittest.TestCase):


    @data((5, 0, 5), (5, 5, 0), (5, 0, 7))
    @unpack 
    def test_interval_distance(self, expected, interval1, interval2):
        actual = pitch_set.interval_distance(interval1, interval2)
        self.assertEqual(expected, actual)
    

    def test_is_valid_pitch_set(self):
        self.assertTrue(pitch_set.is_valid_pitch_set([0, 1, 4]))