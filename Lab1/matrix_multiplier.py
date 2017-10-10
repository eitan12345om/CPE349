from math import floor
import numpy as np


class MatrixMultiplier:
    def __init__(self):
        """
        Initializes a MatrixMultiplier object
        """
        pass

    def iterative_multiplication(self, n, k, m, A, B):
        """
        Multiplies two matrices using an iterative approach

        Arguments:
            n {int} -- Number of rows in matrix A
            k {int} -- Number of columns in A, rows in B
            m {int} -- Number of columns in matrix B
            A {[1...n][1...k]} -- A matrix to be multiplied
            B {[1...k][1...m]} -- A matrix to be multiplied

        Returns:
            C {[1...n][1...m]} -- The product of A and B
        """
        C = [[0 for j in range(k)] for i in range(n)]

        for i in range(n):
            for j in range(m):
                c = 0
                for s in range(k):
                    c += A[i][s] * B[s][j]

                C[i][j] = c

        return C

    def MatrixSum(self, n, A, B):
        C = np.array([[0 for x in range(n)] for y in range(n)])
        for i in range(n):
            for j in range(n):
                C[i][j] = A[i][j] + B[i][j]
        return C

    def MMDC(self, n, A, B):
        C = np.array([[0 for x in range(n)] for y in range(n)])

        if n == 1:
            return (A * B)
        else:
            fl = int(n/2)

            X = A[0:fl, 0:fl]
            Y = A[0:fl, fl:n]
            Z = A[fl:n, 0:fl]
            W = A[fl:n, fl:n]

            P = B[0:fl, 0:fl]
            Q = B[0:fl, fl:n]
            R = B[fl:n, 0:fl]
            S = B[fl:n, fl:n]

            C11 = C[0:fl, 0:fl]
            C12 = C[0:fl, fl:n]
            C21 = C[fl:n, 0:fl]
            C22 = C[fl:n, fl:n]

            XP = np.array([[0 for x in range(fl)] for y in range(fl)])
            XQ = np.array([[0 for x in range(fl)] for y in range(fl)])
            YR = np.array([[0 for x in range(fl)] for y in range(fl)])
            YS = np.array([[0 for x in range(fl)] for y in range(fl)])
            ZP = np.array([[0 for x in range(fl)] for y in range(fl)])
            ZQ = np.array([[0 for x in range(fl)] for y in range(fl)])
            WR = np.array([[0 for x in range(fl)] for y in range(fl)])
            WS = np.array([[0 for x in range(fl)] for y in range(fl)])
            XP = self.MMDC(fl, X, P)
            XQ = self.MMDC(fl, X, Q)
            YR = self.MMDC(fl, Y, R)
            YS = self.MMDC(fl, Y, S)
            ZP = self.MMDC(fl, Z, P)
            ZQ = self.MMDC(fl, Z, Q)
            WR = self.MMDC(fl, W, R)
            WS = self.MMDC(fl, W, S)

            C11 = self.MatrixSum(fl, XP, YR)
            C12 = self.MatrixSum(fl, XQ, YS)
            C21 = self.MatrixSum(fl, ZP, WR)
            C22 = self.MatrixSum(fl, ZQ, WS)

            C[0:fl, 0:fl] = C11
            C[0:fl, fl:n] = C12
            C[fl:n, 0:fl] = C21
            C[fl:n, fl:n] = C22
        return C

    def strassens_algorithm(self, n, k, m, A, B):
        """
        Multiplies two matrices using Volker Strassen's approach

        Arguments:
            n {int} -- Number of rows in matrix A
            k {int} -- Number of columns in A, rows in B
            m {int} -- Number of columns in matrix B
            A {[1...n][1...k]} -- A matrix to be multiplied
            B {[1...k][1...m]} -- A matrix to be multiplied

        Returns:
            C {[1...n][1...m]} -- The product of A and B
        """
        if n == 1:
            return [[A[0][0] * B[0][0]]]

        half_n = floor(n/2)

        X = [[A[i][j] for j in range(half_n)] for i in range(half_n)]
        Y = [[A[i][j + half_n] for j in range(n - half_n)]
             for i in range(half_n)]
        Z = [[A[i + half_n][j] for j in range(half_n)]
             for i in range(n - half_n)]
        W = [[A[i + half_n][j + half_n] for j in range(n - half_n)]
             for i in range(n - half_n)]
        P = [[B[i][j] for j in range(half_n)] for i in range(half_n)]
        Q = [[B[i][j + half_n] for j in range(n - half_n)]
             for i in range(half_n)]
        R = [[B[i + half_n][j] for j in range(half_n)]
             for i in range(n - half_n)]
        S = [[B[i + half_n][j + half_n] for j in range(n - half_n)]
             for i in range(n - half_n)]

        P1 = self.strassens_algorithm(half_n, floor(k/2), floor(m/2), X,
                                      self.matrix_difference(half_n, Q, S))
        P2 = self.strassens_algorithm(half_n, floor(k/2), floor(m/2),
                                      self.matrix_sum(half_n, X, Y), S)
        P3 = self.strassens_algorithm(half_n, floor(k/2), floor(m/2),
                                      self.matrix_sum(half_n, Z, W), P)
        P4 = self.strassens_algorithm(half_n, floor(k/2), floor(m/2), W,
                                      self.matrix_difference(half_n, R, P))
        P5 = self.strassens_algorithm(half_n, floor(k/2), floor(m/2),
                                      self.matrix_sum(half_n, X, W),
                                      self.matrix_sum(half_n, P, S))
        P6 = self.strassens_algorithm(half_n, floor(k/2), floor(m/2),
                                      self.matrix_difference(half_n, Y, W),
                                      self.matrix_sum(half_n, R, S))
        P7 = self.strassens_algorithm(half_n, floor(k/2), floor(m/2),
                                      self.matrix_difference(half_n, X, Z),
                                      self.matrix_sum(half_n, P, Q))

        upper_left = self.matrix_sum(half_n, self.matrix_sum(half_n, P5, P4),
                                     self.matrix_difference(half_n, P6, P2))
        upper_right = self.matrix_sum(half_n, P1, P2)
        lower_left = self.matrix_sum(half_n, P3, P4)
        lower_right = self.matrix_difference(half_n,
                                             self.matrix_sum(half_n, P1, P5),
                                             self.matrix_sum(half_n, P3, P7))

        return self.matrix_combiner(n, upper_left, upper_right, lower_left,
                                    lower_right)

    def matrix_sum(self, n, A, B):
        """
        Helper function for Strassen's Algorithim which sums two matrices

        Arguments:
            n {int} -- Number of rows in the matrices
            A {[1...n][1...n]} -- A matrix to be summed
            B {[1...n][1...n]} -- A matrix to be summed

        Returns:
            C {[1...n][1...m]} -- The sum of A and B
        """
        C = [[0 for j in range(n)] for i in range(n)]

        for i in range(n):
            for j in range(n):
                C[i][j] = A[i][j] + B[i][j]

        return C

    def matrix_difference(self, n, A, B):
        """
        Helper function for Strassen's Algorithm
        which subtracts matrix B from matrix A

        Arguments:
            n {int} -- Number of rows in the matrices
            A {[1...n][1...n]} -- A matrix to be subtracted from
            B {[1...n][1...n]} -- A matrix to be subtracted

        Returns:
            C {[1...n][1...m]} -- The difference of A and B
        """
        C = [[0 for j in range(n)] for i in range(n)]

        for i in range(n):
            for j in range(n):
                C[i][j] = A[i][j] - B[i][j]

        return C

    def matrix_combiner(self, n, upper_left, upper_right, lower_left,
                        lower_right):
        """
        Combines a 4 quarters of a matrix into one whole

        Arguments:
            n {int} -- Number of rows in the final matrix
            upper_left {[1...n/2][1...n/2]}  -- Upper left corner of the matrix
            upper_right {[1...n/2][1...n/2]} -- Upper right corner of the
                                                matrix
            lower_left {[1...n/2][1...n/2]}  -- Lower left corner of the matrix
            lower_right {[1...n/2][1...n/2]} -- Lower right corner of the
                                                matrix

        Returns:
            C {[1...n][1...n]} -- The combination of all four quarters
        """
        C = [[0 for j in range(n)] for i in range(n)]
        k = floor(n/2)

        for i in range(k):
            for j in range(k):
                C[i][j] = upper_left[i][j]
                C[i][j + k] = upper_right[i][j]
                C[i + k][j] = lower_left[i][j]
                C[i + k][j + k] = lower_right[i][j]

        return C
