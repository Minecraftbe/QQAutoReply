from __future__ import annotations
from collections.abc import Iterable
from typing import TYPE_CHECKING
from cv2.typing import MatLike
from enum import Enum

import cv2

if TYPE_CHECKING:
    from paddleocr import PaddleOCR


class Side(Enum):
    UNKNOWN = -1
    LEFT = 0
    RIGHT = 1


type t_point = tuple[int, int]
type t_rect = tuple[t_point, t_point]
type t_sided_rect = tuple[t_rect, Side]
type t_message = tuple[str, Side]
type t_message_list = list[tuple[list[str], Side]]


# TODO: 在未来优化他, 不要裁剪图像, 而是整张丢进ocr然后只提取roi内部的文字
def text_recognition(
    ocr: PaddleOCR, image: MatLike, ROI: Iterable[t_sided_rect]
) -> t_message_list:
    ret: t_message_list = []
    if len(image.shape) == 2:
        image = cv2.cvtColor(image, cv2.COLOR_GRAY2BGR)

    for cnt in ROI:
        (x1, y1), (x2, y2) = cnt[0]
        result = ocr.predict(image[y1:y2, x1:x2])  # pyright: ignore[reportUnknownMemberType]
        length = len(result)
        assert length == 1, (
            f"An unexpected error occurred, length of list was not equal to 1, actual: {length}\nlist of ocr result: {str(result)}"
        )
        msg: list[str] = [t for r in result for t in r["rec_texts"]]  # pyright: ignore[reportUnknownVariableType]
        ret.append((msg, cnt[1]))
    return ret


def levenshtein(s1: str, s2: str, normalize: bool = False) -> float:
    """计算两个字符串的 Levenshtein 距离"""
    m, n = len(s1), len(s2)

    if m == 0 or n == 0:
        return max(m, n)

    if m > n:
        m, n = n, m
        s1, s2 = s2, s1

    dp = [list(range(m + 1)), [0] * (m + 1)]

    for i in range(1, n + 1):
        dp[1][0] = i
        for j in range(1, m + 1):
            if s1[j - 1] == s2[i - 1]:
                dp[1][j] = dp[0][j - 1]
            else:
                dp[1][j] = min(dp[1][j - 1], dp[0][j], dp[0][j - 1]) + 1
        dp[0], dp[1] = dp[1], dp[0]
    return dp[0][m]


# 以下所有的内容都是图像预处理, 来获取文本区域
def process_image(image: MatLike):
    cropped, thresholded = __crop_and_binarize_image(image)
    return __merge_message_blocks(__find_message_contours(thresholded)), cropped


def __crop_and_binarize_image(image: MatLike) -> tuple[MatLike, MatLike]:
    (
        h,
        w,
    ) = image.shape[:2]
    cropped_image = image[5 : h - 4, 5 : w - 4]
    gray: MatLike = cv2.cvtColor(cropped_image, cv2.COLOR_BGR2GRAY)
    threshold: MatLike = cv2.adaptiveThreshold(
        gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV, 11, 2
    )

    return cropped_image, threshold


def __find_message_contours(thresholded_image: MatLike):
    raw_contours = cv2.findContours(
        thresholded_image, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE
    )[0]

    contours: set[t_rect] = set()
    image_height = thresholded_image.shape[0]

    for raw_cnt in raw_contours:
        x1, y1, w, h = cv2.boundingRect(raw_cnt)
        x2, y2 = x1 + w, y1 + h
        rect = ((x1, y1), (x2, y2))
        cy = int(y1 + h / 2)

        if cy < 10 or cy > image_height - 10:
            continue

        if w < 20 or h < 30 or w * h < 700:
            continue

        result, delete = __overlap_detection(rect, contours)
        contours -= delete
        if not result:
            contours.add(rect)

    return sorted(
        (__determine_rect_side(r, thresholded_image) for r in contours),
        key=lambda r: r[0][0][1],
    )


def __merge_message_blocks(message_contours: list[t_sided_rect]):
    ret: list[t_sided_rect] = []
    length = len(message_contours)
    tmp: list[t_sided_rect] = []
    changed = False
    should_stop = False
    for i in range(length):
        if should_stop:
            raise RuntimeError(
                "An error occurred, likely to due an index being out of range or a list containing None."
                f"list:{message_contours}, i:{i}, length: {length}"
            )
        curr = message_contours[i]
        next_ = message_contours[i + 1] if i < length - 1 else None
        changed = False
        if next_ is not None:
            if curr[1] != next_[1]:
                changed = True
        else:
            changed = True
            should_stop = True

        tmp.append(curr)
        if changed:
            unpacked = [r[0] for r in tmp]
            # 一般不会出问题，我还没见过哪个显示器的分辨率大于65536 * 65536
            x1 = y1 = 1 << 16
            x2 = y2 = -1
            for (rx1, ry1), (rx2, ry2) in unpacked:
                x1, y1, x2, y2 = (
                    min(x1, rx1),
                    min(y1, ry1),
                    max(x2, rx2),
                    max(y2, ry2),
                )
            ret.append((((x1, y1), (x2, y2)), tmp[0][1]))
            tmp.clear()
    return ret


def __overlap_detection(new_rect: t_rect, existing_rects: Iterable[t_rect]):
    smaller_rects: set[t_rect] = set()
    (x1, y1), (x2, y2) = new_rect
    area = (x2 - x1) * (y2 - y1)
    ret = False

    for rect in existing_rects:
        (rx1, ry1), (rx2, ry2) = rect
        r_area = (rx2 - rx1) * (ry2 - ry1)

        overlap_area_ = 0
        if x2 >= rx1 and y2 >= ry1 and x1 <= rx2 and y1 <= ry2:
            ox1, oy1, ox2, oy2 = max(x1, rx1), max(y1, ry1), min(x2, rx2), min(y2, ry2)
            overlap_area_ = (ox2 - ox1) * (oy2 - oy1)

        if overlap_area_ > 0.5 * min(area, r_area):
            if area > r_area:
                smaller_rects.add(rect)
            else:
                ret = True

    return ret, smaller_rects


# TODO: improve this in the future
def __determine_rect_side(rect: t_rect, thresholded_image: MatLike) -> t_sided_rect:
    """
    此代码并不够健壮, 例如在非对称截图(一边有头像，而另一边没有)或者纯色头像(无法检测边缘)会出bug\n
    在未来或许会直接使用ocr识别, 而不是先预处理图像
    """
    (x1, y1), (x2, y2) = rect
    r_area = (x2 - x1) * (y2 - y1)
    ih, iw = thresholded_image.shape[:2]
    i_area: int = iw * ih
    side = Side.UNKNOWN

    margin = 2
    l_end = max(0, x1 - margin)
    r_start = min(iw, x2 + margin)

    if r_area >= i_area * 0.7:
        is_left = thresholded_image[y1:y2, :l_end].any()
        is_right = thresholded_image[y1:y2, r_start:].any()
        side = Side.LEFT if is_left else Side.RIGHT
        if is_left == is_right:
            side = Side.UNKNOWN

    else:
        if x1 > iw - x2:
            side = Side.RIGHT
        elif iw - x2 > x1:
            side = Side.LEFT
    if side == Side.UNKNOWN:
        raise RuntimeError("Can't determine the side of the message")

    return rect, side
