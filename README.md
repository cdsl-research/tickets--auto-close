# 概要
既存のRedmine向けチケットソフトについて, Alertmanagerからresolvedを受け取ったら自動でチケットをClose（完了）させる追加プログラムです.

## 環境
Python</br>
Prometheus（2.53.1）</br>
Alertmanager （0.27.0）</br>
Redmine（6.0.4）</br>

## Pythonライブラリ
flask</br>
requests</br>
json</br>
datetime</br>
os</br>

# 動作
Alertmanagerからのアラートでチケット作成されます. ここでは擬似的にアラートが来たことにしてテストで作成しています.

### 注意！
あくまでCloseさせるための追加部分です. このプログラム自体はチケットは作成しません.

![test1](https://github.com/user-attachments/assets/60727154-2e12-4a8c-89ef-4c6b3258912d)

チケットが作成されました.

![test2](https://github.com/user-attachments/assets/934cfad5-9627-4a86-8359-e98ed7c9fa87)

同じようにresolvedになったことを擬似的に送ります.

![test3](https://github.com/user-attachments/assets/3938b3c6-d586-4c57-ac9e-eaedc4e02990)

無事Closeされました.

![test4](https://github.com/user-attachments/assets/783117ba-4516-463a-a9b6-ffb4c1cd0001)

# 終わりに
手作業でチケットをCloseさせる必要がなくなるので, 効率化のためによかったら使ってください.
