# 概要
Redmineでチケットを作成するソフトについて, Alertmanager APIに問い合わせて同名のアラートのチケットresolvedだった時にチケットをClose（完了）させるプログラムです.

## 環境
Python（3.12.3）</br>
Prometheus（2.53.1）</br>
Alertmanager （0.27.0）</br>
Redmine（6.0.4）</br>

### Pythonライブラリ
fastAPI（0.116.1）</br>
requests</br>
json</br>
datetime</br>
os</br>

## 準備
以下のものをインストールしてください.</br>
・python3</br>
・fastAPI</br>
・uvicorn</br>
・request</br>

# 動作
Prometheusがアラートを検知すると, Alertmanagerからの情報でチケットが作成されます.<br>
ここでは実際にAlertmanagerからくる情報をJSON形式を直接送ってアラートが来たことにしてテストで作成しています.

![test1](https://github.com/user-attachments/assets/60727154-2e12-4a8c-89ef-4c6b3258912d)

入力は以下です
```shell
curl -X POST http://localhost:5005/webhook \
-H "Content-Type: application/json" \
-d '{
  "alerts": [
    {
      "status": "firing",
      "labels": {
        "alertname": "Qiita_Manual_Alert",
        "instance": "testhost"
      },
      "annotations": {
        "summary": "Webhookテスト"
      }
    }
  ]
}'
```
チケットが作成されました.

![test2](https://github.com/user-attachments/assets/934cfad5-9627-4a86-8359-e98ed7c9fa87)

同じようにresolvedになったことを擬似的に送ります.

![test3](https://github.com/user-attachments/assets/3938b3c6-d586-4c57-ac9e-eaedc4e02990)

入力は以下です
```shell
curl -X POST http://localhost:5005/webhook \
-H "Content-Type: application/json" \
-d '{
  "alerts": [
    {
      "status": "resolved",
      "labels": {
        "alertname": "Qiita_Manual_Alert",
        "instance": "testhost"
      },
      "annotations": {
        "summary": "Webhookテスト（Resolved）"
      }
    }
  ]
}'
```
無事Closeされました.

![test4](https://github.com/user-attachments/assets/783117ba-4516-463a-a9b6-ffb4c1cd0001)

# 終わりに
手作業でチケットをCloseさせる必要がなくなるので, 効率化のためによかったら使ってください.
