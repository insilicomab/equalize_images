import os
from argparse import ArgumentParser
from pathlib import Path

import cv2
import numpy as np
from tqdm import tqdm


class EqualizeImage:
    def __init__(self) -> None:
        pass

    def _equalize_image_v_histogram(
        self, image: np.ndarray, grid_size: int
    ) -> np.ndarray:
        hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
        clahe = cv2.createCLAHE(clipLimit=3.0, tileGridSize=(grid_size, grid_size))
        hsv[:, :, 2] = clahe.apply(hsv[:, :, 2])
        v_hist_equalized_image = cv2.cvtColor(hsv, cv2.COLOR_HSV2BGR)
        return v_hist_equalized_image

    def _equalize_image_l_histogram(
        self, image: np.ndarray, grid_size: int
    ) -> np.ndarray:
        hsl = cv2.cvtColor(image, cv2.COLOR_BGR2HLS)
        clahe = cv2.createCLAHE(clipLimit=3.0, tileGridSize=(grid_size, grid_size))
        hsl[:, :, 1] = clahe.apply(hsl[:, :, 1])
        l_hist_equalized_image = cv2.cvtColor(hsl, cv2.COLOR_HLS2BGR)
        return l_hist_equalized_image

    def __call__(self, image: np.ndarray, channel: str, grid_size: int) -> np.ndarray:
        if channel == "v":
            hist_equalized_image = self._equalize_image_v_histogram(image, grid_size)
            return hist_equalized_image

        elif channel == "l":
            hist_equalized_image = self._equalize_image_l_histogram(image, grid_size)
            return hist_equalized_image

        else:
            raise ValueError(f"Unknown channel: {channel}")


def parse_args():
    parser = ArgumentParser()
    parser.add_argument("-i", "--image_root", type=str, required=True)
    parser.add_argument("-o", "--output", type=str, default="./outputs")
    parser.add_argument("-gs", "--grid_size", type=int, default=8)
    parser.add_argument("-ch", "--channel", type=str, choices=["v", "l"])
    args = parser.parse_args()
    return args


def main(args):
    # outputsフォルダが存在しない場合は作成
    if not os.path.exists(args.output):
        os.makedirs(args.output, exist_ok=True)

    equalize_image = EqualizeImage()

    # 入力ディレクトリ内のファイル・ディレクトリを取得
    for root, _, files in tqdm(
        os.walk(args.image_root), total=len(list(os.walk(args.image_root)))
    ):
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
                    hist_equalized_image = equalize_image(
                        image, channel=args.channel, grid_size=args.grid_size
                    )

                    # 画像の保存
                    cv2.imwrite(str(out_path), hist_equalized_image)


if __name__ == "__main__":
    args = parse_args()
    main(args)
