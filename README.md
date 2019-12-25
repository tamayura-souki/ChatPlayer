# ChatPlayer
YouTubeLive のチャットで遊ぶためのコード。チャットを取得して、コマンドを認識して、GBで表示したりするアプリ、配信画面に乗せて使う。

デフォルトでコメントがウインドウ上に右から左に流れる。

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

## 使い方
起動して出てくるウィンドウのIDと書かれた横に、配信のID(URLの中にあるやつ)を入力して、okボタンを押してください。
何もなければ、緑色の画面にコメントが流れます。

- setting.json
    - "chat_id" ここに配信のIDを入力します。(起動時にソフト上で入力できます)
	- "win_size" の [縦の解像度, 横の解像度] でウィンドウの解像度を変更できます。
	- "back_color" の [R, G, B] で背景色を指定出来ます。

- chat_setting.json
	- "plain_font_path" でデフォルトで使用するフォントファイルを指定できます。
		
	- "sound_commands" で音声系のコマンドの設定が出来ます。\
	    新規に増やすことも出来ます。\
	    ※pygame(使用しているライブラリ)の仕様上、wavとoggのみロード出来ます。
		
	- "speed_commands" で文字の速度を変更するコマンドを設定できます。\
	    "speed" でマイナスを指定すると、逆から流れます。
		
	- "color_commands" で文字色を変更するコマンドを設定できます。\
		[R,G,B]で指定してください。\
		"outline_color" は1ドットだけついてる縁色お設定です。

	- "rain_commands" で文字がランダムに降ってくるコマンドを設定できます。\
		"time" の秒数だけ、ランダムに"drops" 内のいずれかの文字が上から降ります。\
		初速と加速度を設定できます。

# Requirements
- pychat(https://github.com/taizan-hokuto/pytchat)
- pygame

# License
[![MIT License](http://img.shields.io/badge/license-MIT-blue.svg?style=flat)](LICENSE)