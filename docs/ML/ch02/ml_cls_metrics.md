# Performance Measures for Classifiers

## Confusion matrix

Confusion matrix(오차행렬)은 

* row는 label의 class를 나타내며, 
* column은 prediction 결과 class를 나타낸다.

Classifier의 성능을 확실하게 파악할 수 있다는 장점이 있으나 하나의 값으로 표현되지 않는다는 단점을 가짐.

`sklearn.metrics.confusion_matrix` 를 사용하여 쉽게 구할 수 있음.

binary classifier의 경우,

|  | Negative | Positive |
| :---: | :---: | :---: |
| $H_1$: False ($H_0$: True) | $TN$, True Negative | $FP$, False Positive (Type-I error)|
| $H_1$: True ($H_0$: False)| $FN$, False Negative (Type-II error) | $TP$, True Positive |

* $H_1$ : alternative hypothesis
* $H_0$ : null hypothesis
* False Positive 는 Type-I error(1종오류) 또는 $\alpha$ error라고도 불림.
* False Negative 는 Type-II error(2종오류) 또는 $\beta$ error라고도 불림.
* 가설검증 등에서 사용하는 $\alpha$ value (Critical value, significance level)가 작아질수록 Type-I error가 일어날 확률은 감소하지만 Type-II error가 일어날 확률은 커짐.

<figure markdown>
![](./img/type1_type2_error.png)
</figure>

* 가설검증은 type-1 error를 줄이는데 초점을 둠. ($\alpha=0.05$에서 $\alpha=0.01$을 쓰는 추세)

## Accuracy (정확도)

Prediction에서 Ground True값인 label을 정확하게 맞춘 확률을 의미함.

$$\text{Accuracy} = \dfrac{\text{Correct_Predictions}}{\text{All_Predictions}}$$

Binary classification으로 말한다면

$$\text{Accuracy} = \dfrac{TP+TN}{TP+FP+TN+FN}$$

* $TP$ : True Positive (실제로 Label이 Positive인데 Positive라고 predict한 갯수)
* $TN$ : True Negative (실제로 Label이 Negative인데 Negative라고 predict한 갯수)
* $FP$ : False Positive (실제로 Label이 Positive인데 Negative라고 predict한 갯수)
* $FN$ : False Negative (실제로 Label이 Negative인데 Positive라고 predict한 갯수)

가장 일반적으로 사용되는 Performance measure이지만, unbalanced classification의 경우엔 성능을 제대로 나타내지 못한다는 단점이 있음.


예를 들어 유병률이 0.1% 희귀병을 판정하는 classifier의 경우, 아무 로직 없이 무조건 희귀병이 아니라고 판정해도 99.9%의 accuracy를 얻게된다.

* 이같은 단점 때문에 precision과 recall 등과 함께 사용됨.

---

## Precision (정밀도)

특정 class의 precision이란, 해당 class라고 predict한 sample들의 수가 분모이고 해당 prediction에서 Label도 해당 class인 경우들의 수가 분자임.

* 즉, 특정 class라고 예측한 경우에서 몇 퍼센트가 정답을 맞추었는지를 나타냄.
* 특정 class라고 예측한 경우에서의 정답률에 해당함.

$$\text{Precision}_\text{cls_A} = \dfrac{TP_\text{cls_A}}{TP_\text{cls_A}+FP_\text{cls_A}}$$

* $TP_\text{cls_A}$ : Label과 Predict 모두 class A인 sample들의 수.
* $FP_\text{cls_A}$ : Predict는 class A였으나 Label이 class A가 아닌 sample들의 수.

Precision을 올리는 쉬운 방법은 정말 확실하게 해당 class A인 경우에만 class A로 판정하는 것임. 즉, 판정시 사용하는 threshold를 매우 높게 잡으면 precision은 올라간다.

> imbalanced classes의 경우에도, precision은 다음에 다룰 recall과 함께 성능을 잘 반영해준다.  
> 각 class별로 precision이 나오며 특정 관심이 있는 class에서의 model의 성능을 따로 확인할 수 있다.

문제는 threshold를 올려서 precision을 올리는 경우, Label이 class A이지만 prediction에서 낮은 score를 기록할 경우, class A라고 판정하지 않을 확률이 올라간다. (이는 recall or sensitivity가 낮아지는 문제로 이어짐)

---

## Recall (재현율)

Sensitivity 또는 True Positive Rate라고도 불린다. Precision과 분자는 같지만 분모가 달라진다. 분모가 Label이 특정 class인 샘플의 수가 된다. 

* 즉, 특정 class를 label로 가지는 sample들에 대해 몇 퍼센트를 해당 class로 맞추었는지를 의미함.
* precision과 마찬가지로 class별로 구해진다.

$$\text{Recall}_\text{cls_A} = \dfrac{TP_\text{cls_A}}{TP_\text{cls_A}+FN_\text{cls_A}}$$

Recall과 Precision은 trade-off 관계이다. threshold를 올리면 precision은 향상되지만, recall은 떨어지게 된다.

극단적으로 항상 class A라고 판정할 경우, class A에 대한 recall은 1.0 (=100%)를 달성할 수 있다. 당연하지만 이 경우 class A의 precision은 매우 나뻐지게 된다.

--- 

## Precision and Recall for Multi-class classification

Macro Average
: 각 class별로 precision과 recall을 구하고 이들의 평균을 낸 경우. 각 클래스별로 동일한 weight를 주어 평균을 구함.

$$\text{Precision}_\text{macro} = \dfrac{\text{Precision}_\text{cls_A}+\text{Precision}_\text{cls_B}+ \dots +\text{Precision}_\text{cls_N}}{N}$$

$$\text{Recall}_\text{macro} = \dfrac{\text{Recall}_\text{cls_A}+\text{Recall}_\text{cls_B}+ \dots +\text{Recall}_\text{cls_N}}{N}$$

* $N$ : number of classes

Micro Average
: 각 class별로 TP, FP, TN, FP를 구하고, 각 class의 TP, FP, TN, FP를 더해서 최종 TP와 FP, TN, FP를 구하고 이로부터 Precision과 Recall을 구한다.

$$\text{Precision}_\text{micro} = \dfrac{TP_\text{cls_A}+TP_\text{cls_B}+ \dots +TP_\text{cls_N}}{TP_\text{cls_A}+TP_\text{cls_B}+ \dots +TP_\text{cls_N}+ FP_\text{cls_A}+FP_\text{cls_B}+ \dots +FP_\text{cls_N}}$$


$$\text{Recall}_\text{micro} = \dfrac{TP_\text{cls_A}+TP_\text{cls_B}+ \dots +TP_\text{cls_N}}{TP_\text{cls_A}+TP_\text{cls_B}+ \dots +TP_\text{cls_N}+ FN_\text{cls_A}+FN_\text{cls_B}+ \dots +FN_\text{cls_N}}$$

Weighed Average
: 각 class별로 precision과 recall을 구하고 label에서 각 class의 샘플수를 weight로 삼아 average를 계산함.

$$\text{Precision}_\text{weighted} = \dfrac{N_\text{cls_A}\text{Precision}_\text{cls_B}+N_\text{cls_B}\text{Precision}_\text{cls_B}+ \dots +N_\text{cls_N}\text{Precision}_\text{cls_N}}{M}$$


$$\text{Recall}_\text{weighted} = \dfrac{M_\text{cls_A}\text{Recall}_\text{cls_A}+M_\text{cls_B}\text{Recall}_\text{cls_B}+ \dots +M_\text{cls_N}\text{Recall}_\text{cls_N}}{M_\text{total}}$$

* $M_\text{total}$ : number of total samples
* $M_\text{cls_A}$ : number of samples of class A

---

## Precision-Recall Curve and Precision-Recall Trade-off

Binary classification에서 주로 얻어지는 curve. 

Multiclass 의 경우는 다음 URL을 참고할 것 (micro 를 이용.).
[scikit-learn's plot_precision_recall](https://scikit-learn.org/0.15/auto_examples/plot_precision_recall.html)

해당 class로 판정하는 threshold를 조절하여 각각의 경우의 precision과 recall에 점을 찍는 방식으로 그려진다.

* recall이 x축, precision이 y축에 그려지는게 일반적임.
* 오른쪽 상단은 recall과 precision이 둘다 높은 경우이기 때문에 curve가 오른쪽 상단에 가깝게 그려질수록 우수한 performance의 모델임.

<figure markdown>
![](./img/PR_curve.png){width="600" align="center"}
</figure>

위의 PR Curve에서 보이듯이 precision이 높아지면 recall이 낮아지고, recall이 높아지면 precision이 떨어진다.

이를 threshold를 x축으로 하여 precision과 recall을 각각 그리면 다음과 같음.

<figure markdown>
![](./img/PR_threshold.png){width="600" align="center"}
</figure>

* 위의 graph에서 threshold가 극도로 높아지면 precision이 출렁거리는 것을 확인할 수 있음.
* 이는 해당 threshold를 넘는 sample의 수가 매우 적어지다보니 적은 수의 FP의 영향력이 커져서 발생하는 현상임. 

MNIST 데이터 (0-9까지의 숫자 데이터)에서 class 5에 대한 분류기에 대해 12개 샘플로 테스트한 결과가 다음과 같다고 가정하자.

<figure markdown>
![](./img/PR_tradeoff.png)
</figure>

* Threshold에 따라 precision과 recall이 어떻게 변하는지를 간략하게 보여줌.
* recall의 경우 threshold가 낮아짐에 따라 항상 증가하지만,
* precision은 경우 오답인 sample이 추가됨에 따라 출렁거림이 있을 수 있다. 

---

## Receiver operating characteristics (ROC) and AUC

ROC는 False Positive Rate (FPR, fall-out) 에 대해 Recall (=True Positive Rate)를 그린 graph임.

* x축 : FPR (=1-NTR = 1-specificity)
* y축 : TPR (=recall, sensitivity)

OvR 또는 OvO 를 이용하여 Multi-class classification에서도 그릴 수는 있으나 주로 binary classification에서 사용됨.

Multi-class의 경우의 ROC는 다음 URL을 참고할 것.
[Multiclass Receiver Operating Characteristic (ROC)](https://scikit-learn.org/stable/auto_examples/model_selection/plot_roc.html)

PR-Curve와 유사한 형태이나 Left-top이 ideal model의 performance에 해당하기 때문에 chart가 Left-top (High recall and Low FPR)에 가까울수록 높은 성능의 모델임.

### False Positive Rate (=FPR)

$$\text{FPR}=\dfrac{FP}{FP+TN}= 1-\dfrac{TN}{FP+TN} = 1-\text{specificity}$$

* Label이 Negative인 sample의 수가 분모이며 분자는 Label이 negative인데 positive로 predict한 sample의 수임.
* 작을수록 좋은 모델임.

FPR은 1-TNR (=1-specificity)에 해당한다. specificity는 negative인 sample을 negative로 predict할 확률로 True Negative Rate라고도 불림.

### Area under the Curve (AUC)

ROC 에서 curve 아래의 area(면적)을 가르키며, 1에 가까울수록 ideal한 model임.

---

## PR-Curve vs. ROC-Curve

Label이 Positive인 sample이 적은 경우 또는 false positive 를 false negative 보다 중요하게 생각할 때, PR-Curve가 보다 선호된다.

* 위의 경우, ROC-Curve의 경우보다 PR-Curve는 보다 AUC가 낮게 나와서 성능의 차이를 보다 잘 보여준다.

다음 그림은 MNIST에서 5와 5가 아닌 경우를 분류하는 binary classification을 수행하는 동일 모델에 대해 ROC-Curve와 PR-Curve를 그린 것임.

<figure markdown>
![](./img/PR_vs_ROC.png)
</figure>

---

## F Score ( f measure or f-beta score)

Precision과 Recall을 동시에 반영하는 measure로 많이 사용됨.

Precision과 Recall의 Harmonic mean으로 수식은 다음과 같음.

$$\begin{aligned}F_{\beta}=F&=\dfrac{1}{\alpha\dfrac{1}{\text{precision}}+(1-\alpha)\dfrac{1}{\text{recall}}}\\ &=\dfrac{(\beta^2+1)\text{precision}\times\text{recall}}{\beta^2\text{precision}+\text{recall}}\end{aligned}$$

* Precision과 Recall이 모두 중요할 경우 $\beta=1$
* Recall이 보다 중요할 경우 보통  $\beta=2$ : 의료분야등에서 많이 이용됨.
* Precision이 보다 중요할 경우 $\beta=0.5$


---

## 참고자료

* [Accuracy, precision, and recall in multi-class classification](https://www.evidentlyai.com/classification-metrics/multi-class-metrics)
* [[Math] Mean : Measures of Central Tendency](https://dsaint31.tistory.com/483)