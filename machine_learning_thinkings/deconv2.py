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
        # output stride should be 2n
        if s & 1:
            return
        s = s >> 1
        # apply padding
        cur_idx = 0
        for i in range(size_m):
            for _ in range(p):
                matrix[i] = [0] + matrix[i] + [0]
        size_m = size_m + p * 2
        for _ in range(p):
            matrix = [[0] * size_m] + matrix + [[0] * size_m]
        # add zeros between ranges
        for i in range(size_m):
            curpos = 0
            while curpos < size_m * (1 + s) - 2:
                matrix[i] = matrix[i][:curpos + 1] + [0] * s + matrix[i][curpos + 1:]
                curpos += 2
        size_m = size_m * (1 + s) - 1
        curpos = 0
        while curpos < size_m - 1:
            matrix = matrix[:curpos + 1] + [[0] * size_m] * s + matrix[curpos + 1:]
            curpos += 2
        # add zeros around
        for i in range(size_m):
            matrix[i] = [0] * (size_f - 1) + matrix[i] + [0] * (size_f - 1)
        size_m = size_m + (size_f - 1) * 2
        for _ in range(size_f - 1):
            matrix = [[0] * size_m] + matrix + [[0] * size_m]

        new_size = size_m - size_f + 1
        answer = [[0] * new_size for _ in range(new_size)]
        f = self.rearrange_matrix(f)
        for i in range(new_size):
            for j in range(new_size):
                m = self.cut_matrix(matrix, (i, j), size_f, size_f)
                answer[i][j] = self.convolution_cell(m, f)
        return answer
            
    def convolution_cell(self, m1, m2):
        if len(m1)!= len(m2) or len(m1[0]) != len(m2[0]):
            return
        s = 0
        for i in range(len(m1)):
            for j in range(len(m1[0])):
                s += m1[i][j] * m2[i][j]
        return s
    
    def cut_matrix(self, original_matrix, start_pos, cut_x, cut_y):
        start_y, start_x = start_pos[0], start_pos[1]
        end_y, end_x = start_y + cut_y, start_x + cut_x
        cutted_y = original_matrix[start_y:end_y]
        res = []
        for line in cutted_y:
            res.append(line[start_x:end_x])
        return res

    def rearrange_matrix(self, matrix):
        size = len(matrix)
        m = [[0] * size for _ in range(size)]
        for i in range(size):
            for j in range(size):
                m[i][j] = matrix[size - i - 1][size - j - 1]
        return m

a = Solution()
b = a.deconvolution([[3, 3],[1, 1]], [[1, 2, 3], [0, 1, 0], [2, 1, 2]], 0, 2)
print(b)