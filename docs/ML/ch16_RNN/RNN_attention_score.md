# Attention Score (or Attention Function, Alignment)

Attention mechanism에서 `query`, `key`, `value` 에서 `query`와 `key`의 ***similarity*** 를 의미.

> 특정 `query`에 대해 모든 `key`들의 Attention score들로 구성된 vector $\textbf{e}$에 `softmax` 함수를 취해서 attention distribution을 구함. 이 attention distribution은 일종의 확률분포이며 `value` vector와 함께 weighted sum, ***attention*** 을 구하는데 사용된다.  
>  
> ![](../img/ch16_RNN/encoder_decoder_w_attention.png)


## Attention score의 등장.

`seq2seq` 에서 2014년 Graves, Wayne, Danihelka에 의해 attention (=content-based attention)이 도입되었음.

Content-based Attention을 위해서 

Decoder의 time-step $j$에서  

* Decoder state $\textbf{s}_{j-1}$ 과
* Encoder state $\textbf{h}_i$ 의
* similarity 를 계산함

해당 계산은 모든 Decoder state들에 대해 이루어짐.

여기서 Decoder state $\textbf{s}$와 Encoder state $\textbf{h}$ 간의 similarity를 구하는 것이 attention score 임.

`query`, `key`로 일반화하여 애기한다면, 

* Decoder state $\textbf{s}_{j-1}$이 `query`.
* Encoder state $\textbf{h}_i$가 `key`.

Grave et al. 의 논문에서 Decoder state와 Encoder state는 같은 dimension 크기를 가짐.

> Grave et al. 에서 `value`는 `key`와 동일.

## 많이 사용되는 Attention score.

Grave et al.이 제안한 것을 포함하여 다음과 같은 여러 attention score가 있음.

| ref. | name | def. | etc.|
|---|---|---|---|
|[Grave et al., 2014](https://arxiv.org/abs/1410.5401)| content-based attention | $f(\textbf{s},\textbf{h})=\frac{\textbf{s}\cdot\textbf{h}}{\|\textbf{s}\|_2 \|\textbf{s}\|_2}$| |
|[Bahdanau et al., 2015](https://arxiv.org/abs/1409.0473)| Bahdanau (or additive) attention | $f(\textbf{s},\textbf{h})=V^T \text{tanh}(W_s \textbf{s}+ W_h \textbf{s})| Luong et al. 에선 `concat` attention score로 칭함. |
|[Luong et al., 2015](https://arxiv.org/abs/1508.04025)| Loung attention | $f(\textbf{s}, \textbf{h})= \textbf{h} \cdot W \textbf{s} | 논문에서 `general` attention score|
|[Luong et al., 2015](https://arxiv.org/abs/1508.04025)| dot attention | $f(\textbf{s},\textbf{h})= \textbf{h} \cdot \textbf{s}$ | 논문에서 `dot` attention score|
|[Vaswani et al., 2017](http://papers.nips.cc/paper/7181-attention-is-all-you-need.pdf)|$f(\textbf{s},\textbf{h})= \frac{\textbf{s}\cdot \textbf{h}}{\sqrt{n}} | $n$ 은 encoder state $\textbf{h}$의 dimension임.| 

## 읽어보면 좋은 자료.

* [Multi-head attention mechanism: “queries”, “keys”, and “values,” over and over again](https://data-science-blog.com/blog/2021/04/07/multi-head-attention-mechanism/)
* [어텐션 메커니즘 (Attention Mechanism) : Seq2Seq 모델에서 Transformer 모델로 가기까지](https://heekangpark.github.io/nlp/attention)
* [cosine similarity](https://dsaint31.tistory.com/entry/ML-Cosine-Similarity)
* [distance function](https://dsaint31.tistory.com/entry/ML-Cosine-Similarity)