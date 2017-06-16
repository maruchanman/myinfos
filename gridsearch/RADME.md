# GridSearchとRandomizedSearch

## 目的

GridSearchとRandomizedSearchを比較する

RandomizedSearchには、
確率分布を与える方法とパラメータ候補をリストで与える方法があるが、
今回は確率分布を与える方法を取り上げる。

## アウトライン

- 概念の違い
- 実装の違い
- 使い分け案

## 概念の違い

### GridSearch

- 有限数のグリッドを全て調べる
  - 精度は高いが時間がかかりがち
- 取り得るパラメータを予め決めて渡す
  - パラメータの値域が検討つかない時どうしよう問題
- 離散変数のみ
  - 連続変数には対応していない

### RandomizedSearch

- 無限数のグリッドをランダムに調べまくる
- 各パラメータに対して確率分布を与える
- 連続変数に対応できる

## 実装の違い

XGBoostのパラメータ推定をそれぞれの方法でやってみる。

### GridSearch

```python

from xgboost import XGBClassifier
from sklearn.grid_search import GridSearchCV

param_grid = {
    "max_depth": list(range(1, 11)),
    "subsample": [x * 0.1 for x in range(5, 16)],
    "colsample_bytree": [x * 0.1 for x in range(5, 16)]
}
gs = GridSearchCV(XGBClassifier(), param_grid)

```

GridSearchはパラメータをリストで渡す。

### RandomizedSearch

```python

from scipy import stats
from xgboost import XGBClassifier
from sklearn.grid_search import RandomizedSearchCV

param_dist = {
    "max_depth": stats.randint(1,10),
    "subsample": stats.uniform(0.5, 1),
    "colsample_bytree": stats.uniform(0.5, 1)
}
rs = RandomizedSearchCV(XGBClassifier(), param_dist)

```

RandomizedSearchはパラメータを確率分布で渡す。
確率分布はscipy.statsから選ぶ。
今回は、subsampleやcolsample_bytreeに0.5~1.5の値域の一様分布を採用してみた。

他にも色々と確率分布は選択できる。

例えば、

```
正規分布：stats.norm()
指数分布：stats.expon()
```
などなど、
パラメータに合わせて最適な確率分布を選ぶと良い。
【使える確率分布一覧】
https://docs.scipy.org/doc/scipy/reference/stats.html



## 使い分け案

連続変数のパラメータを推定したいときや、
パラメータがどんな値を取るのか全く検討がつかないときは、
RandomizedSearchを使ってみるとよいかも。


