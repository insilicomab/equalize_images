import os
from argparse import ArgumentParser
from pathlib import Path

import cv2
import numpy as np
from tqdm import tqdm


def equalize_image_histogram(image: np.ndarray, grid_size: int) -> np.ndarray:
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    clahe = cv2.createCLAHE(clipLimit=3.0, tileGridSize=(grid_size, grid_size))
    hsv[:, :, 2] = clahe.apply(hsv[:, :, 2])
    hist_equalized_image = cv2.cvtColor(hsv, cv2.COLOR_HSV2BGR)
    return hist_equalized_image


def parse_args():
    parser = ArgumentParser()
    parser.add_argument("-i", "--image_root", type=str, required=True)
    parser.add_argument("-o", "--output", type=str, default="./outputs")
    parser.add_argument("-gs", "--grid_size", type=int, default=8)
    args = parser.parse_args()
    return args


def main(args):
    # outputsフォルダが存在しない場合は作成
    if not os.path.exists(args.output):
        os.makedirs(args.output, exist_ok=True)

    # 入力ディレクトリ内のファイル・ディレクトリを取得
    for root, _, files in tqdm(os.walk(args.image_root), total=len(list(os.walk(args.image_root)))):
        if files is not []:
            # ファイルの保存先を作成
            out_subdir = Path(args.output) / root
            os.makedirs(str(out_subdir), exist_ok=True)

            for file in files:
                # 画像ファイル(png)のみ処理
                if file.lower().endswith((".png", ".PNG", ".jpg", ".jpeg", ".JPG")):
                    # inputパス
                    input_path = Path(root) / file

                    # outputパス
                    out_path = out_subdir / file

                    # 画像の読み込み
                    image = cv2.imread(str(input_path))

                    # ヒストグラムの平坦化
                    hist_equalized_image = equalize_image_histogram(
                        image, grid_size=args.grid_size
                    )

                    # 画像の保存
                    cv2.imwrite(str(out_path), hist_equalized_image)


if __name__ == "__main__":
    args = parse_args()
    main(args)
