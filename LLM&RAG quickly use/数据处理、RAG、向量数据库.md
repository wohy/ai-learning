# 数据处理：把企业知识组织起来
## RAG 
### 解决以下问题
1. 交互过程中的长文本处理
2. 信息内容的实时更新
### 数据保留了程序的全部记忆
AI 时代的程序记忆：**向量数据库**
数据信息被转换为高维向量，使得**语言模型能够进行高效的语义相似度计算和检索**
向量数据库中，**查找变成了计算每条记录的向量近似度**，然后按照分值倒序返回结果
**RAG** 就是如何存取向量的方法论
- 衍生出的多种 RAG 技术
    - 利用**图结构**表示和检索知识的 GraphRAG
    - 结合**知识图谱**增强生成能力的 KGA2G（Knowledge Graph Augmented Generation）

### Embedding 的概念
Embedding 指的是将文本、图像等数据转化为固定维度的向量表示的过程。
这个向量捕捉了数据的语义特征，便于进行相似性比较和检索

### 向量对文本数据的表示
方式：
1. 词嵌入 (**Word Embeddings**)
    - **Word2Vec**（一种 NLP 技术）, **GloVe**（Global Vectors, is a model for distributed word representation 分布式词表示模型）：
        通过这些模型，将 words mapping 到低维度的空间，使语义相近的词在向量空间中相距更近。并通过训练，模型可以知道词与词之间的关系

    - **Contextual Embeddings**（上下文嵌入）：
        如 BERT 和 GPT ，这些模型通过上下文生成词的嵌入，能够捕捉到不同词在不同句子语境中的不同含义

2. 句子和段落嵌入（**Sentence and Paragraph Embeddings**）
    可以通过聚合单词的嵌入（例如取平均）或使用特定模型（如 Sentence-BERT）来生成句子或段落的嵌入，从而捕捉更复杂的语义。


### 向量对图像数据的表示
方式：
1. 卷积神经网络（**Convolutional Neural Networks (CNNs)**）
    CNNs 被广泛的运用于图像处理，它通过多个卷积层来提取图像的特征，这些特征经过几层处理后，转化为向量表示，通过该向量可以捕捉到图像的形状、颜色、纹理等信息

2. 图像嵌入（**Image Embeddings**）
    通过 CNNs 处理后的向量可以作为图像嵌入，使其更易于进行相似度比较和检索，例如，相似度更高的图片在向量空间中靠的更近

### 向量对数据的语义特征的捕捉
方式：
1. 相似性学习 （**Similarity Learning**）
嵌入学习的目标就是，使相相似的 image 、 words or text 在向量空间中跟距离更近，这通过 **损失函数（loss function）**（like contrastive loss） 来实现

2. 高维度特征映射 （**High-Dimensional Feature Mapping**）
向量可以在高维度空间中进行运算，从而捕捉到数据中更复杂的关系和特征

3. 语义关系 （**Semantic Relationships**）
通过训练，模型可以识别出不同数据之间潜在的语义关系，从而在向量表示中反映出来