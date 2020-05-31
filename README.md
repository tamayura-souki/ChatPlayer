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
起動して出てくるウィンドウのURLと書かれた横に、配信のURLを入力して、okボタンを押してください。
何もなければ、緑色の画面にコメントが流れます。

- config.json
    - "chat_id" ここに配信のIDを入力します。(起動時にソフト上で入力できます)
	- "window_size" の [縦の解像度, 横の解像度] でウィンドウの解像度を変更できます。
	- "background_color" の [R, G, B] で背景色を指定出来ます。

- chat_config.json
	- "taboo_words" : ["単語", "単語", ...] で指定した単語を含むコメントを表示しません。

	- "oo_words" : ["単語", "単語", ...] で指定した単語を"〇〇"に置き換えます。

	- "font"
		- "name" : "path or name" 使用したいフォントファイルのパスを入力してください。
		- "size" で フォントのサイズを指定できます。

	- "sound_commands" で音声系のコマンドの設定が出来ます。\
	    新規に増やすことも出来ます。\
	    ※pygame(使用しているライブラリ)の仕様上、wavとoggのみロード出来ます。

	- "niconico_commands" で 横に流れる文字について設定できます。
		- "line_n" で行数を設定できます。
		- "speed" で文字の流れる速さを設定できます。

		- "speed_commands" で文字の速度を変更するコマンドを設定できます。\
		    "speed" でマイナスを指定すると、逆から流れます。

		- "color_commands" で文字色を変更するコマンドを設定できます。\
			[R,G,B]で指定してください。\
			"outline_color" は1ドットだけついてる縁色の設定です。

	- "rain_commands" で文字がランダムに降ってくるコマンドを設定できます。\
		"time" の秒数だけ、ランダムに"drops" 内のいずれかの文字が上から降ります。\
		初速と加速度を設定できます。

# Requirements
- pytchat(https://github.com/taizan-hokuto/pytchat)
- pygame(https://github.com/pygame/pygame)
- emoji(https://github.com/carpedm20/emoji/)

# License
MIT