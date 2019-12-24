# ChatPlayer
youtubeチャットで遊ぶためのコード。チャットを取得して、コマンドを認識して、GBで表示したりするアプリ、配信画面に乗せて使う。

デフォルトでコメントがウインドウ上に右から左に流れるようになっている。

## 実装済みのコマンド
/police /medic サイレンを鳴らす\
/w 笑い声を鳴らす\
/tot トリックオアトリート

/red /blue /green /bk 文字色を変更する

/fast /slow 文字の流れる速度を変える \
/-fast /-run /-slow 文字を逆から流す

/snow 雪を降らす \
/rain 雨を降らす \
/blood 血が降る \
/pray 十字架が降りてきて登っていく \
/ray 光が降る

/unk チャンネル名非表示

# Requirements
- pychat(https://github.com/taizan-hokuto/pytchat)
- pygame

# License
[![MIT License](http://img.shields.io/badge/license-MIT-blue.svg?style=flat)](LICENSE)