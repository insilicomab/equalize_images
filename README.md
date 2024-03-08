# Equalize Images

## 環境構築(Docker)

### コンテナの作成と仮想環境の起動

1. コンテナの作成と実行

```
docker compose up -d
```

2. コンテナのシェルを起動する

```
docker compose exec -it equalization /bin/bash
```

3. シェルから抜ける

```
exit
```

### コンテナの停止

```
docker compose stop
```

再起動する際は以下のコマンドを実行する。

```
docker compose start
```

### コンテナの削除

```
docker compose down
```

## 画像の平滑化

1\. [input]("./input")フォルダに変換したい画像(.png)を含むフォルダを格納する

2\. 以下のコマンドを実行する

```
python src/equalize_images.py -i /path/to/data_dir
```

3\. 出力先のフォルダに格納したフォルダの構造と同じものが生成される

### 引数

- `-i, --image_root`: [input]("./input")フォルダの相対パス
- `-o, --output`: 出力ディレクトリ（デフォルト: [outputs]("./outputs)）
- `-gs, grid_size`: グリッドサイズ（デフォルト: 8）
