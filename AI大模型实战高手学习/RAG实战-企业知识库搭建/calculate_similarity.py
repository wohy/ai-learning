import numpy as np
from gensim.models import KeyedVectors
# 定义计算余弦相似度的函数
def calculate_similarity(vector1, vector2):
    # 使用numpy库来计算余弦相似度
    dot_product = np.dot(vector1, vector2)
    norm_vector1 = np.linalg.norm(vector1)
    norm_vector2 = np.linalg.norm(vector2)
    similarity = dot_product / (norm_vector1 * norm_vector2)
    return similarity
# 假设我们有一个向量代表用户偏好
user_preference = np.array([10, 5, 10, 4])
# 我们有一系列电影向量
movie_vectors = np.array([
    [8, 7, 9, 6],   # 电影A
    [9, 6, 8, 7],   # 电影B
    [10, 5, 7, 8]   # 电影C
])
# 计算并打印每部电影与用户偏好之间的相似度
for i, movie_vector in enumerate(movie_vectors):
    similarity = calculate_similarity(user_preference, movie_vector)
    #电影A与用户偏好的相似度为: 0.97
    # 电影B与用户偏好的相似度为: 0.97
    # 电影C与用户偏好的相似度为: 0.95
    print(f"电影{chr(65+i)}与用户偏好的相似度为: {similarity:.2f}")

