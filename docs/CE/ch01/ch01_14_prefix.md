# Prefixs for SI Units and for bits (IEC) 

## Prefixs for SI Units

우리가 일반적으로 사용하는 Prefix들은 SI unit (국제단위, gram, meter등등)을 위한 것들이다.

| Prefix | Symbol | Factor |   | Prefix | Symbol | Factor |
|:------:|:------:|:------:|---|:------:|:------:|:------:|
| deka-  | da     | $10^1$ |   | deci-  | d      | $10^{-1}$ |
| hecto- | h      | $10^2$ |   | centi- | c      | $10^{-2}$ |
| kilo-  | k or K | $10^3$ |   | milli- | m      | $10^{-3}$ |
| mega-  | M      | $10^6$ |   | micro- | $\mu$  | $10^{-6}$ |
| giga-  | G      | $10^9$ |   | nano-  | n      | $10^{-9}$ |
| tera-  | T      | $10^{12}$ || pico-  | p      | $10^{-12}$ |
| peta-  | P      | $10^{15}$ || pemto- | f      | $10^{-15}$ |
| exa-   | E      | $10^{18}$ || atto-  | a      | $10^{-18}$ |

이들의 단위들은 ^^인간을 위한 것^^ 이므로 `base`를 10으로 사용하고 있다.

`bit`의 경우 `base-2 system`이기 때문에 실제로는 ***2의 제곱*** 으로 표현이 되어야 한다.

하지만, 1995년 이전에는 ^^bit에 대한 prefix도 SI unit의 것을 차용해서 사용^^ 했다.  
사실, 차용을 할 때, SI Unit의 prefix에 ^^가장 가까운 2의 제곱으로 할당^^ 을 했다. 즉, 컴퓨터 초기에는 kilobits 또는 kilobytes 를 많이 사용했고, `kilo-`의 1,000에 가까운 2의 제곱값이 바로 $2^{10}=1024$ (2의 10승, 2 to the power 10)인지라, 원래는 $2^{10}$ bit인 것을 그냥 1 kilobit라고 차용하여 사용한 것이다.

문제는 이런 암묵적인 차용으로 인해 base(밑수)를 10으로 쓰는 사람과 2로 쓰는 사람들 간에 오차가 발생한다는 점이다.  

storage기술이 발전하면서 더 큰 prefix가 사용되었고 결국 오차는 점점 더 커지게 되었다.  실제로 storage를 파는 사람들의 경우 ^^SI unit에서의 prefix로 계산 (밑수를 10으로 사용)^^하여 본인들의 제품의 저장용량을 표시했고, 이를 사용하는 기술자들은 프로그래밍에 익숙하기 때문에 2를 밑수로 하여 해당 용량을 이해하는 경우가 많았다.  

결국 1995년에 관련하여 미국에서 소송이 발생했고 해당 이슈들로 인해 IEC가 새로운 prefix를 1998년에 발표를 하게 되었다. 하지만, 아직도 많은 사람들이 SI unit으로 이해하고 있고 사용하고 있는 게 현실임.

> IEC : International Electrotechnical Commission.   

## Prefix for bit (IEC standard prefix)


| Prefix | Symbol | Factor |   |
|:------:|:------:|:------:|:------:
| kibi-  | Ki     | $2^{10}$ |kilobinary |
| mebi-  | Mi     | $2^{20}$ |megabinary |
| gibi-  | Gi     | $2^{30}$ |gigabinary |
| tebi-  | Ti     | $2^{40}$ |terabinary |
| pebi-  | Pi     | $2^{50}$ |petabinary |
| exbi-  | Ei     | $2^{60}$ |exabinary |

`KiB` 는 `kibi-bytes`를 의미하고, `Mib`는 `Mebi-bits`를 의미한다.


## 참고자료

* techtarget's [kibi, mebi, gibi, tebi, pebi and exbi](https://www.techtarget.com/searchstorage/definition/Kibi-mebi-gibi-tebi-pebi-and-all-that)







