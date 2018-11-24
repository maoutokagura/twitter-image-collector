# twitter-image-collector
This tool collect twitter image



## System requirements

*python 3.*


## Files 

* get_illustration.py - singleスレッド実装版
* get_illustration_thread.py 複数スレッド実装版、うまく動かない
* get_illustration_concurrent_futures.py - ThreadPoolExecutor実装版。10同時ダウンロードできる。最速。おすすめ
* setting.py - 自分のアクセトークンを設定してください。  

## アクセストークンの設定

    参考  
    https://syncer.jp/Web/API/Twitter/REST_API/
