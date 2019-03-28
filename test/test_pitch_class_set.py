import pytest 
from musical_set.pitch_class_set import (get_interval, 
                                         to_valid,
                                         adjacency_list,
                                         PitchClassSet)

@pytest.mark.parametrize('expected, p1, p2', [
    (5, 0, 5),
    (5, 5, 0),
    (5, 0, 7)
])
def test_get_interval_equal(expected, p1, p2):
    actual = get_interval(p1, p2)
    assert expected == actual

@pytest.mark.parametrize('expected, p1, p2', [
    (7, 0, 7)
])
def test_get_interval_distance_notequal(expected, p1, p2):
    actual = get_interval(p1, p2)
    assert expected != actual

@pytest.mark.parametrize('input_set, expected', [
    ([-1, 0, 3], [11, 0, 3]),
    ([12], [0])
])
def test_to_valid(input_set, expected):
    actual = to_valid(input_set)
    assert expected == actual

    
@pytest.mark.parametrize('input_set, expected', [
    (
        [0, 4, 7], 
        {
            0: {4: 4, 7: 5},
            4: {0: 4, 7: 3},
            7: {0: 5, 4: 3}
        }
    )
])
def test_adjacency_list(input_set, expected):
    actual = adjacency_list(input_set)
    assert expected == actual 

class TestPitchClassSet(object):
    
    
    @pytest.mark.parametrize('input_set, expected_vector, expected_sum', [
        ([0, 4, 7], {3: 1, 4: 1, 5: 1}, 12)
    ])
    def test_interval_vector(self, input_set, expected_vector, expected_sum):
        actual = PitchClassSet(input_set)
        assert expected_vector == actual.interval_vector() 
        assert expected_sum == actual.interval_sum()
    
    @pytest.mark.parametrize('input_set, steps, expected', [
        ([0, 1, 2], 1, [1, 2, 3]),
        ([10, 11, 0], 1, [11, 0, 1]),
        ([1, 3, 6, 7], 12, [1, 3, 6, 7]),
        ([3, 2, 3], -1, [2, 1, 2]),
        ([0, 3, 10], -3, [9, 0, 7])
    ])
    def test_transpose(self, input_set, steps, expected):
        actual = PitchClassSet(input_set).transpose(steps)
        assert expected == list(actual)

    @pytest.mark.parametrize('p, s, expected', [
        ([0, 1, 2], 1, [1, 2, 0]),
        ([0, 1, 2], 2, [2, 0, 1])
    ])
    def test_rotate(self, p, s, expected):
        actual = PitchClassSet(p).rotate(s)
        assert expected == list(actual)


    @pytest.mark.parametrize('input_set, expected', [
        ([0, 2, 7], [4, 2, 9])
    ])
    def test_invert(self, input_set, expected):
        actual = PitchClassSet(input_set).invert()
        assert expected == list(actual)
    
    @pytest.mark.parametrize('input_set, expected', [
        ([7, 4, 0], [0, 4, 7]),
        ([4, 7, 2, 4], [2, 4, 7]),
        ([5, 7, 2, 5], [2, 5, 7]),
        ([0, 2, 3, 5, 10], [10, 0, 2, 3, 5]),
        ([8, 9, 3], [3, 8, 9])
    ])
    def test_normal_order(self, input_set, expected):
        actual = PitchClassSet(input_set).normal_order()
        assert expected == list(actual)
    

    @pytest.mark.parametrize('input_set, expected', [
        ([0, 2, 3, 5, 10], [0, 2, 3, 5, 7]),
        ([8, 2, 5, 1], [0, 1, 4, 7]),
        ([5, 9, 0, 4], [0, 1, 5, 8])
    ])
    def test_prime_form(self, input_set, expected):
        actual = PitchClassSet(input_set).prime_form()
        assert expected == list(actual)