import copy

class Solution:
    def deconvolution(self, matrix, f, p, s):
        """
        :type matrix, f: List[List[int]]; matrix and filter
        :type p, s: int; p : padding, s : stride
        :rtype: List[List[int]]
        """
        if not matrix or not matrix[0] or not f or not f[0]:
            return
        size_m = len(matrix)
        size_f = len(f)
        if size_m != len(matrix[0]) or size_f != len(f[0]):
            return
        if s > size_f:
            return
        # enlarger the original matrix
        for _ in range(p):
            for i in range(len(size_m)):
                matrix[i] = [0] + matrix[i] + [0]
                size_m += 2
            matrix = [0] * size_m + matrix + [0] * size_m
        y_matrix = []
        for i in range(size_m):
            x_matrix = []
            for j in range(size_m):
                # need to do deep copy otherwise it will edit filter based on the existed pointer
                new_f = copy.deepcopy(f)
                m = self.matrix_multiply(new_f, matrix[i][j])
                x_matrix.append(m)
            base_matrix = x_matrix[0]
            for i in range(1, len(x_matrix)):
                base_matrix  = self.matrix_shiftadd(base_matrix, x_matrix[i], shift = s)
            y_matrix.append(base_matrix)
        base_matrix = y_matrix[0]
        for i in range(1, len(y_matrix)):
            base_matrix = self.matrix_shiftadd(base_matrix, y_matrix[i], shift = s, is_x= False)
        return base_matrix
            

    def matrix_shiftadd(self, m1, m2, shift = 1, is_x = True):
        h = len(m1)
        w = len(m1[0])
        if is_x:
            for i in range(h):
                m1_start = w - len(m2[0]) + shift
                for j in range(m1_start, w):
                    m1[i][j] += m2[i][j - m1_start]
                for b in range(shift - 1, -1, -1):
                    m1[i].append(m2[i][len(m2[0]) - 1 - b])
        else:
            m1_start = h - len(m2) + shift
            for i in range(m1_start, h):
                for j in range(w):
                    m1[i][j] += m2[i - m1_start][j]
            for b in range(shift - 1, -1, -1):
                m1.append(m2[len(m2) - 1 - b])
        return m1

    def matrix_multiply(self, matrix, multipilar):
        for i in range(len(matrix)):
            for j in range(len(matrix)):
                matrix[i][j] *= multipilar
        return matrix

a = Solution()
b = a.deconvolution([[1,2],[4,5]], [[0, 1, 2], [1, 1, 2], [0, 1, 2]], 0, 2)
print(b)