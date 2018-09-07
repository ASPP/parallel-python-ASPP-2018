from micro.counting import count_objects
import numpy as np
from numpy.testing import assert_equal

def test_count_no_object():
    a = np.zeros([6, 6], dtype=np.int32)
    assert_equal(count_objects(a), 0)

def test_count_1_object():
    a = np.zeros([6, 6], dtype=np.int32)
    a[1:-1, 1:-1] = 1
    assert_equal(count_objects(a), 1)

def test_count_objects_2_objects():
    a = np.array(
      [[ 0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.],
       [ 0.,  1.,  1.,  1.,  0.,  0.,  0.,  0.,  0.,  0.],
       [ 0.,  1.,  1.,  1.,  0.,  0.,  0.,  0.,  0.,  0.],
       [ 0.,  1.,  1.,  1.,  0.,  0.,  0.,  0.,  0.,  0.],
       [ 0.,  0.,  0.,  0.,  0.,  1.,  1.,  0.,  0.,  0.],
       [ 0.,  0.,  0.,  0.,  0.,  1.,  1.,  0.,  0.,  0.],
       [ 0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.],
       [ 0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.],
       [ 0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.],
       [ 0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.]], dtype=np.int32)
    assert_equal(count_objects(a), 2)

def test_count_1_object_rectangle():
    a = np.array(
      [[ 0.,  0.,  0.,  0.,  0.],
       [ 0.,  1.,  1.,  1.,  0.],
       [ 0.,  1.,  1.,  1.,  0.],
       [ 0.,  1.,  1.,  1.,  0.],
       [ 0.,  0.,  0.,  0.,  0.],
       [ 0.,  0.,  0.,  0.,  0.],
       [ 0.,  0.,  0.,  0.,  0.],
       [ 0.,  0.,  0.,  0.,  0.],
       [ 0.,  0.,  0.,  0.,  0.],
       [ 0.,  0.,  0.,  0.,  0.]], dtype=np.int32)
    assert_equal(count_objects(a), 1)

def test_count_all_ones():
    a = np.ones([6, 6], dtype=np.int32)
    assert_equal(count_objects(a), 1)
