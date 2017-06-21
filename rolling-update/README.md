# 【GCP】rolling-updateを用いて新しいバージョンをGKE上に安全にデプロイする

## 目的

GKEで動かしているデプロイメントのdockerイメージを更新して新しいバージョンをデプロイしたいと想定で、rolling-updateを用いて安全に新しいバージョンをデプロイしてみる。

## rolling-updateとは

> システム全体を同じ機能を持った複数のコンピュータで構成している場合によく用いられる方式で、システムを稼動状態のまま一台ずつ順番に更新する。更新中の機材は運用を停止しているが、他の機材でシステムの稼動状態を維持する。
[IT用語辞典](http://e-words.jp/w/%E3%83%AD%E3%83%BC%E3%83%AA%E3%83%B3%E3%82%B0%E3%82%A2%E3%83%83%E3%83%97%E3%83%87%E3%83%BC%E3%83%88.html)

サービスを稼働させたまま徐々にコンテナを新しくできる。
roll-backにも対応。

## 手段

- v1を普通にデプロイ
- v2をrolling-updateでデプロイ
- roll-backしてみる

## v1を普通にデプロイ

まずこんな感じの設定ファイルを準備した。
GCRに予め登録しておいたkdy-project/kdy-image:v1を用いてkdy-deploymentをデプロイする。

```deployment-v1.yml
apiVersion: extensions/v1beta1
kind: Deployment
metadata:
  name: kdy-deployment
spec:
  replicas: 2
  template:
    metadata:
      labels:
        app: kdy-deployment
        tier: kdy-deployment
    spec:
      containers:
      - name: test-server
        image: gcr.io/kdy-project/kdy-image:v1
```

```デプロイする
$ kubectl create -f deployment-v1.yml
deployment "kdy-deployment" created
```

```デプロイを確認
$ kubectl get deployment
NAME             DESIRED   CURRENT   UP-TO-DATE   AVAILABLE   AGE
kdy-deployment   2         2         2            2           36s
```

デプロイされてる。

## v2をrolling-updateでデプロイ

使用するdocker-imageをv2に変更。

```deployment-v2.yml
apiVersion: extensions/v1beta1
kind: Deployment
metadata:
  name: kdy-deployment
spec:
  replicas: 2
  template:
    metadata:
      labels:
        app: kdy-deployment
        tier: kdy-deployment
    spec:
      containers:
      - name: test-server
        image: gcr.io/kdy-project/kdy-image:v2
```

```rolling-updateを実行
$ kubectl apply -f deployment-v2.yml
```

### 挙動を見てみる

```rolling-update前
$ kubectl get pods
NAME                              READY     STATUS    RESTARTS   AGE
kdy-deployment-4242080677-2p3xp   1/1       Running   0          11m
kdy-deployment-4242080677-sc06g   1/1       Running   0          11m
```

```rolling-update直後
kubectl get pods
NAME                              READY     STATUS        RESTARTS   AGE
kdy-deployment-2046165440-3r77k   1/1       Running       0          42s
kdy-deployment-2046165440-rtlrs   1/1       Running       0          42s
kdy-deployment-4242080677-2p3xp   0/1       Terminating   0          13m
kdy-deployment-4242080677-sc06g   0/1       Terminating   0          13m
```

v1がterminatingされている

```rolling-update後
kubectl get pods
NAME                              READY     STATUS    RESTARTS   AGE
kdy-deployment-2046165440-3r77k   1/1       Running   0          1m
kdy-deployment-2046165440-rtlrs   1/1       Running   0          1m
```

v2に移行された

## roll-backしてみる

```roll-back
$ kubectl rollout undo deployment kdy-deployment
deployment "kdy-deployment" rolled back
```

```roll-back後
$ kubectl get pods
NAME                              READY     STATUS    RESTARTS   AGE
kdy-deployment-4242080677-fl96r   1/1       Running   0          35s
kdy-deployment-4242080677-vhxvk   1/1       Running   0          35s
```

戻った！
