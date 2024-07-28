import numpy as np

# 输入数据的数量
n_Y = input('请输入评价对象的数量: ')
m_Y = input('请输入评价指标的数量: ')
n_Y = int(n_Y)
m_Y = int(m_Y)

# 读取和处理输入的判断
Judgement = int(input('这些指标是否需要经过正向化处理，需要请输入1，不需要输入0: '))

# 正向化处理
if Judgement == 1:
    Pos_Y = list(map(int, input('输入需要正向化处理的指标所在列（例如：2,3,6）: ').split(',')))
    Type_Y = list(map(int, input('输入需要处理的这些列的指标类型（1:极小型, 2:中间型, 3:区间型）: ').split(',')))
    Y = np.array(input('输入原始矩阵 Y: '))
    for i, pos in enumerate(Pos_Y):
        Y[:, pos - 1] = Posit_Y(Y[:, pos - 1], Type_Y[i])  # 注意：Python索引从0开始

    print('正向化后的矩阵 Y:')
    print(Y)

# 标准化过程
Z = Y / np.sqrt(np.sum(Y**2, axis=0))
print('标准化矩阵 Z:')
print(Z)

# 权重处理
Judgement = int(input('是否需要增加权重，需要输入1，不需要输入0: '))
if Judgement == 1:
    Judgement = int(input('使用熵权法确定权重请输入1，否则输入0: '))
    if Judgement == 1:
        # 重新标准化检查
        if np.any(Z < 0):
            print('原来标准化得到的Z矩阵中存在负数，所以需要对X重新标准化')
            for i in range(n_Y):
                for j in range(m_Y):
                    Z[i, j] = (Y[i, j] - np.min(Y[:, j])) / (np.max(Y[:, j]) - np.min(Y[:, j]))

        W = weight_shang(Z)
        print('熵权法确定的权重为:')
        print(W)
    else:
        # 自定义权重
        w = np.array(list(map(float, input('输入权重（以空格分隔）: ').split())))
        if w.shape[0] != m_Y:
            raise ValueError('权重的数量应该等于评价指标的数量')

else:
    w = np.ones(m_Y) / m_Y

# 计算得分
D_P = np.sqrt(np.sum((Z - np.max(Z))**2 * np.repeat(w, n_Y, axis=0), axis=1))
D_N = np.sqrt(np.sum((Z - np.min(Z))**2 * np.repeat(w, n_Y, axis=0), axis=1))
S = D_N / (D_P + D_N)
stand_S = S / np.sum(S)
sorted_S, index = np.sort(stand_S, descending=True)

print('最后的得分为:')
print(stand_S)

# 计算熵权函数
def weight_shang(Z):
    n, m = Z.shape
    D = np.zeros(m)
    for i in range(m):
        P = Z[:, i] / np.sum(Z[:, i])
        e = np.where(P == 0, 0, -P * np.log(P) / np.log(n))
        D[i] = 1 - np.sum(e)

    W = D / np.sum(D)
    print('熵值为:')
    for i in range(m):
        print(e[i])

    return W

# 正向化处理函数
def Posit_Y(column, type_y):
    # 此函数需要根据正向化的具体规则进行定义
    # 由于没有具体的正向化规则，以下代码仅为示例
    if type_y == 1:
        # 极小型
        return 1 / (1 + column)
    elif type_y == 2:
        # 中间型
        return (1 + column) / 2
    elif type_y == 3:
        # 区间型
        return (column - np.min(column)) / (np.max(column) - np.min(column))
    else:
        raise ValueError('未知的指标类型')

# 注意：实际应用中，你需要根据实际情况实现 Posit_Y 函数。
