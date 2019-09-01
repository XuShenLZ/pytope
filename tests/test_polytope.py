
import unittest

import numpy as np

from pytope import Polytope


class TestPolytope(unittest.TestCase):
  def test___init__(self):

    # Create an R^2 Polytope in H-representation from upper and lower bounds.
    # Check that dimension n and the matrices A, b, and H = [A b] are all
    # set correctly.
    lb1 = (1, -4)
    ub1 = (3, -2)

    n1 = len(ub1)
    A1 = np.vstack((-np.eye(n1), np.eye(n1)))
    b1 = np.concatenate((-np.asarray(lb1), np.asarray(ub1)))[:, np.newaxis]

    P1 = Polytope(lb=lb1, ub=ub1)

    self.assertTrue(P1.in_H_rep)
    self.assertFalse(P1.in_V_rep)
    self.assertEqual(P1.n, n1)
    self.assertTrue(np.all(P1.A == A1))
    self.assertTrue(np.all(P1.b == b1))
    self.assertTrue(np.all(P1.H == np.hstack((A1, b1))))
    self.assertTrue(np.issubdtype(P1.A.dtype, np.float))
    self.assertTrue(np.issubdtype(P1.b.dtype, np.float))
    self.assertTrue(np.issubdtype(P1.H.dtype, np.float))

    # Create an R^2 Polytope in V-representation from a list of four vertices
    # Check that dimension n and vertex list V are set correctly
    V2 = np.array([[1, 1], [-1, 1], [-1, -1], [1, -1]])
    n2 = V2.shape[1]

    P2 = Polytope(V2)

    self.assertTrue(P2.in_V_rep)
    self.assertFalse(P2.in_H_rep)
    self.assertEqual(P2.n, n2)
    self.assertTrue(np.issubdtype(P2.V.dtype, np.float))

    # Create an R^2 Polytope in H-representation by specifying A and b in
    # Ax <= b. Check that dimension n and vertex list V are set correctly
    A3 = [[-1, 0], [0, -1], [1, 1]]
    b3 = (0, 0, 2)
    n3 = 2
    H3 = np.hstack((A3, np.asarray(b3, dtype=float)[:, np.newaxis]))

    P3 = Polytope(A3, b3)

    self.assertTrue(P3.in_H_rep)
    self.assertFalse(P3.in_V_rep)
    self.assertEqual(P3.n, n3)
    self.assertTrue(np.all(P3.A == np.asarray(A3, dtype=float)))
    self.assertTrue(np.all(P3.b == np.asarray(b3, dtype=float)[:, np.newaxis]))
    self.assertTrue(np.all(P3.H == H3))
    self.assertTrue(np.issubdtype(P3.A.dtype, np.float))
    self.assertTrue(np.issubdtype(P3.b.dtype, np.float))
    self.assertTrue(np.issubdtype(P3.H.dtype, np.float))

    # Ensure illegal use of the constructor raises an error.
    with self.assertRaises(ValueError):
      Polytope(V2, A=A3, b=b3)
    with self.assertRaises(ValueError):
      Polytope(A3, b3, V=V2)
    with self.assertRaises(ValueError):
      Polytope(A=A3)
    with self.assertRaises(ValueError):
      Polytope(b=b3)
    with self.assertRaises(ValueError):
      Polytope(V2, lb=lb1, ub=ub1)
    with self.assertRaises(ValueError):
      Polytope(A3, b3, lb=lb1, ub=ub1)


if __name__ == '__main__':
  unittest.main()
