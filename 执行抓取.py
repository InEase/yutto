import time
import os
from yutto.mux import 获取所有下载索引
from loguru import logger

命令行参数 = [
    "-b",
    "--proxy no",
    "--login-strict",
    "--with-metadata",
    "-d",
    "/Users/transmux/Projects/Backup/Bili收藏视频/",
    "-c",
    "b70946c1%2C1754303320%2Cfad6b%2A22CjCpf5aQDhNNLtq7xkLnKcbKZtuf4GeN4q_N9lVdBhVw4IQANy-Wx37N-SN4xLknKIwSVjlMVUNIekxoS2lMX09CRDlKZEFOa0xoeFFoQjhpSE95MEQwSzZ0RFprSk9vcFRWZjhybGRnMk9FWF9TV0J1Zmx6T1R4M2l1NzlKS3RZSWJBU0gwT0RBIIEC",
]


def 执行抓取():
    下载索引 = 获取所有下载索引()["list"]
    下载索引 = [item["链接"] for item in 下载索引]

    logger.info(f"共有 {len(下载索引)} 个下载索引")

    for item in 下载索引:
        logger.info(f"开始下载 {item}")
        # os 执行命令
        os.system(f"yutto {' '.join(命令行参数)} {item}")

        logger.info(f"{item} 抓取完成，等待10秒")
        time.sleep(10)

    logger.info("所有下载完成")


if __name__ == "__main__":
    while True:
        执行抓取()
        logger.info(f"抓取完成，等待3小时")
        time.sleep(3 * 60 * 60)
