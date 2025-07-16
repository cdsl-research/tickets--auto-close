# 概要
Prometheus, Alertmanagerで監視してるシステムにおいて, Redmine上にチケットを作成するプログラムです.</br>
またAlertmanager APIに問い合わせて同名のアラートのチケットresolvedだった時にチケットをClose（完了）してくれます.

## 環境
Python（3.12.3）</br>
Prometheus（2.53.1）</br>
Alertmanager （0.27.0）</br>
Redmine（6.0.4）</br>

### Pythonライブラリ
fastAPI（0.116.1）</br>
requests</br>
json</br>
os</br>

## ディレクトリ構成
```shell-session
c0117304@c0117304-test:~$s
└─tickets-auto-close/
  ├─app.py
  └─venv
```

## 準備
・以下のものをインストールしてください.</br>

python3を確認
　UbuntuはPythonがあらかじめ入っていますが一応確認します
```shell
c0117304@c0117304-test:~$ sudo apt install python3
[sudo] password for c0117304:
Reading package lists... Done
Building dependency tree... Done
Reading state information... Done
python3 is already the newest version (3.12.3-0ubuntu2).
0 upgraded, 0 newly installed, 0 to remove and 75 not upgraded.
c0117304@c0117304-test:~$
```

venvをインストール
```shell
c0117304@c0117304-test:~/tickets-auto-close$ sudo apt install python3-venv
[sudo] password for c0117304:
Reading package lists... Done
Building dependency tree... Done
Reading state information... Done
python3-venv is already the newest version (3.12.3-0ubuntu2).
0 upgraded, 0 newly installed, 0 to remove and 86 not upgraded.
c0117304@c0117304-test:~/tickets-auto-close$
```
仮想環境を作成(venvがあるディレクトリで実行してください)
```shell
c0117304@c0117304-test:~/tickets-auto-close$ python3 -m venv venv
(venv)  c0117304@c0117304-test:~/tickets-auto-close$
```

仮想環境を有効化
```shell
c0117304@c0117304-test:~/tickets-auto-close$ source venv/bin/activate
(venv)  c0117304@c0117304-test:~/tickets-auto-close$
```

fastapi uvicorn requestsをインストール</br>
仮想環境を有効した状態で実行してください
```shell
c0117304@c0117304-test:~/tickets-auto-close$ pip install fastapi uvicorn requests
Requirement already satisfied: fastapi in ./venv/lib/python3.12/site-packages (0.116.1)
Requirement already satisfied: uvicorn in ./venv/lib/python3.12/site-packages (0.35.0)
Requirement already satisfied: requests in ./venv/lib/python3.12/site-packages (2.32.4)
Requirement already satisfied: starlette<0.48.0,>=0.40.0 in ./venv/lib/python3.12/site-packages (from fastapi) (0.47.1)
Requirement already satisfied: pydantic!=1.8,!=1.8.1,!=2.0.0,!=2.0.1,!=2.1.0,<3.0.0,>=1.7.4 in ./venv/lib/python3.12/site-packages (from fastapi) (2.11.7)
Requirement already satisfied: typing-extensions>=4.8.0 in ./venv/lib/python3.12/site-packages (from fastapi) (4.14.1)
Requirement already satisfied: click>=7.0 in ./venv/lib/python3.12/site-packages (from uvicorn) (8.2.1)
Requirement already satisfied: h11>=0.8 in ./venv/lib/python3.12/site-packages (from uvicorn) (0.16.0)
Requirement already satisfied: charset_normalizer<4,>=2 in ./venv/lib/python3.12/site-packages (from requests) (3.4.2)
Requirement already satisfied: idna<4,>=2.5 in ./venv/lib/python3.12/site-packages (from requests) (3.10)
Requirement already satisfied: urllib3<3,>=1.21.1 in ./venv/lib/python3.12/site-packages (from requests) (2.5.0)
Requirement already satisfied: certifi>=2017.4.17 in ./venv/lib/python3.12/site-packages (from requests) (2025.7.9)
Requirement already satisfied: annotated-types>=0.6.0 in ./venv/lib/python3.12/site-packages (from pydantic!=1.8,!=1.8.1,!=2.0.0,!=2.0.1,!=2.1.0,<3.0.0,>=1.7.4->fastapi) (0.7.0)
Requirement already satisfied: pydantic-core==2.33.2 in ./venv/lib/python3.12/site-packages (from pydantic!=1.8,!=1.8.1,!=2.0.0,!=2.0.1,!=2.1.0,<3.0.0,>=1.7.4->fastapi) (2.33.2)
Requirement already satisfied: typing-inspection>=0.4.0 in ./venv/lib/python3.12/site-packages (from pydantic!=1.8,!=1.8.1,!=2.0.0,!=2.0.1,!=2.1.0,<3.0.0,>=1.7.4->fastapi) (0.4.1)
Requirement already satisfied: anyio<5,>=3.6.2 in ./venv/lib/python3.12/site-packages (from starlette<0.48.0,>=0.40.0->fastapi) (4.9.0)
Requirement already satisfied: sniffio>=1.1 in ./venv/lib/python3.12/site-packages (from anyio<5,>=3.6.2->starlette<0.48.0,>=0.40.0->fastapi) (1.3.1)
(venv) c0117304@c0117304-test:~/tickets-auto-close$
```
REDMINE_URL, REDMINE_API_KEY, REDMINE_PROJECT_ID, REDMINE_TRACKER_ID, REDMINE_OPEN_STATUS_ID, REDMINE_CLOSE_STATUS_IDの環境変数を`export`で入力します.</br>

```shell
export REDMINE_URL="http://your-redmine-server:32300"
export REDMINE_API_KEY="your_redmine_api_key"
export REDMINE_PROJECT_ID="your_project_id"
export REDMINE_TRACKER_ID="1"
export REDMINE_OPEN_STATUS_ID="1"
export REDMINE_CLOSE_STATUS_ID="8"
```

REDMINE_URL → <"redmineがあるIPアドレスorホスト名":"ポート番号"></br>
REDMINE_API_KEY → redmineにログインし, 右上の個人設定を開くと右側に"APIアクセスキ"があります.</br>
REDMINE_PROJECT_I → redmineでチケットを出力するプロジェクトの識別子をいれてください.</br>
REDMINE_TRACKER_ID → 1（デフォルトの設定でBagに登録されます）.</br>
REDMINE_OPEN_STATUS_ID → 1（未着手）
REDMINE_CLOSE_STATUS_ID → 8（完了）

fastAPIを起動
```shell
c0117304@c0117304-test:~/tickets-auto-close$ uvicorn app:app --reload --host 0.0.0.0 --port 5005
INFO:     Will watch for changes in these directories: ['/home/c0117304/Alert-Ticket-Grouping']
INFO:     Uvicorn running on http://0.0.0.0:5005 (Press CTRL+C to quit)
INFO:     Started reloader process [4225] using StatReload
INFO:     Started server process [4227]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
```
以上のようになっていれば作動しています.</br>
# 動作
Prometheusがアラートを検知すると, Alertmanagerからの情報でチケットが作成されます.<br>
ここでは実際にAlertmanagerから来る情報を`curl`で直接送ってチケットを作成しています.

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
Redmineのプロジェクトページを開くとチケットが作成されたことが確認できます.
<img width="1484" height="403" alt="スクリーンショット 2025-07-15 130232" src="https://github.com/user-attachments/assets/a2de6776-2b51-4126-9989-9dda2f271f14" />
<img width="1457" height="453" alt="スクリーンショット 2025-07-15 130647" src="https://github.com/user-attachments/assets/5a6098b4-ddbf-48a2-b9ef-5d6b00c1086e" />

先ほどのチケットがresolved状態になったとして, プログラムがAPIに問い合わせるとCloseされます.</br>
↓ではそれを疑似的行っています.

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
<img width="1492" height="637" alt="スクリーンショット 2025-07-15 141352" src="https://github.com/user-attachments/assets/49049786-6d34-45e0-9f91-627e5ff474f4" />

# 終わりに
手作業でチケットをCloseさせる必要がなくなるので, 効率化のためによかったら使ってください.
