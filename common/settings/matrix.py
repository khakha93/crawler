def transpose_matrix(mat):
    t_mat = list(map(list, zip(*mat)))
    return t_mat


def print_matrix(mat):
    for r in mat:
        for c in r:
            print(c, end=' ')
        print('')


def confirm_matrix(mat):
    is_ok = True
    # row 가 잘 들어갔는지 한번 더 확인
    column_num = len(mat[0])
    for i in range(1, len(mat)):
        if len(mat[i]) != column_num:
            mat[i] = mat[i][:column_num]
            is_ok = False
    return is_ok
