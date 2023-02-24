# Reinforcement Learning (강화학습)

Agent (학습하는 시스템)가   

* Environment를 관찰하고  
* Action을 취한 후  
* Reward를 받으면서  

어떤 Policy 라는 ^^최상의 전략^^ 을 학습하는 것 을 가르킴.

Reinfrocement Learning 에서 learning system을 `agent`라고 부르며, 이 agent 가 `environment` 와 상호 작용을 하면서 취한 ^^`action`에 따라 reward signal (or penalty signal)를 얻는데^^, ***최종적인 accumulated reward 를 maximize*** 하도록 ^^어떤 일련의 action들을 수행할지를 결정하는 `policy`^^를 학습하는 것을 가르킨다.

> A `policy` determines the action an agent should take in a particular situation to maximize final accumulated reward.

## The three most important distinguishing properties of Reinforcement Learning Proble.

아래와 같은 특징을 가지는 문제를 agent가 효과적으로 해결하도록 하는 방법들을 우리는 Reinforcement Learning method라고 한다.

1. Closed-loop Problem : agent가 취한 action이 이후의 agent의 input (environment의 state 등)에 영향을 준다. 
2. not providing explicitly direct instructions which actions to take : 명시적으로 어떤 action이 취해야 하는지를 직접적으로 알려주지 않음.
3. 연속된 action들과 이들로 인한 reward signal에 의한 결과는 장기간에 걸쳐 누적되어 나타난다. : 특정 action은 즉각적으로는 이득이 될 수 있으나 장기적으로는 오히려 손해가 될 수 있다.

### Agent 와 Reinforcement Learning Process

Agent는 강화학습에서 학습자 에 해당됨.

Reinforcemetn Learning Process는 다음의 요소들을 반드시 가지고 있어야 함.

1. Agent는 environment와 상호작용을 함. (action + sensation)
    - `Action`으로 Environment의 상태를 변화시킴.
    - Environment의 `State` 일부를 sensing할 수 있으며 이를 통해 다음 action을 결정함.
2. Agent는 명시적인 goal을 가짐. (goal)
    - 해당 goal은 Environment의 상태와 연관되어 있음.
    - goal의 달성 여부에 관련된 reward가 정의되며, Agent의 현재 state에 대한 action에 의해 변경된 environment의 state와 goal과의 연관성 등에 의해 계산된 `Reward`가 agent에 주어진다.

![](../img/ch00/reinforcement_learning.png)



## Supervised Learning과 Unsupervised Learning과의 차이점.

Reinforcement Learning은 interaction으로부터 학습이 이루어져야하는데, 이 경우 모든 situation에 대한 correct action이 지정되기 불가능함 (supervised learning과의 차이점). 때문에 reward function등이 label 대신 주어짐. 

> Reward signal은 agent가 취한 action에 대한 environment의 feedback으로 supervised learning의 ground truth에 해당하는 label과는 차이가 있다. 어떤 이상적인 action을 명시적으로 모든 상황에 맞게 주어질 수 없기 때문에 해당 action이 얼마나 goal을 달성하는데 유용한지를 측정하는 reward function으로부터 계산된 값이라고 봐야 한다.

해당 reward function으로부터 주어지는 reward signal을 maximization하는 learning이라는 점에서 unsupervised learning하고도 차이가 있다.

> Reinforcement Learning에서는 exploratory trial-and-error approch나 deliberative planning등을 통해 agent는 final accumulated reward를 최대화하는 것을 목표로 한다.

Unsupervised learning처럼 agent가 얻는 experience의 내부적인 특성 구조를 추출하는 것은 reinforcement learning의 목표가 아니다. (물론 해당 추출하는 과정이 reward signal을 maximization하는 목표에 도움이 될 수는 있다.)  

> Environment의 모든 state에 대해 reward와 panelty가 주어져있다고 생각하고 acton을 통해 agent는 environment의 state를 변경해 나갈 수 있다고 하자. 
> 이때 agent가 acton을 결정하는 기준이 바로 policy이고 이 policy가 final accumulated reward를 최대화하는 방향으로 학습이 되게 하면 된다. 
> 이는 매우 간단한 경우이고, 많은 경우 reward는 즉각적으로 주어지기 어려운 경우도 많다 (체스 등에서 당장은 상대편 말을 잡아서 이득이지만, 장기적으로는 킹을 잃게 되는 수가 있을 수 있고, 당장은 내 퀸을 잃지만 장기적으로는 상대 킹을 잡는 수가 있을 수 있다).
> 더욱이 상대편이 있는 경우엔 상대방의 action에 의해서도 reward가 영향을 받게 된다는 점이 reward function에서 어려운 점이다. 즉, reward는 action에 대해 즉각적일 수도 있으나 delayed feedback으로 주어질 수 있다.

## 결론

요약하면, Reinforcement Learning은 기존의 supervised learning이나 unsupervised learning과 구별되는 종류의 ML이다. interaction이 일어나는 경우에서 사용되므로, 로보틱스등에서 많이 이용된다. 

> ML에서의 hyper-parameter tunning에서도 적용되는 경우도 많다.

