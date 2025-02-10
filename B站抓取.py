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
    "ca7749c9%2C1754708388%2C766da%2A22CjDSuqLQN7vTkZsZyJD4eQ07mUEGfl7bTe49Xp3eV8w7OoG2QMj0RBfLOfmO9qkTi6kSVmYxQkRiaTZ0TmE0UG9hSEtXSzRVSWtwRWprdWlvdmp3eDRNcHMzRHdLZnhIVUZGWWI4MHFjbEpJbmxXcnkyc1l4RXdKMXlVN0xJTWFwaE1UM2JaZHZnIIEC",
]


def 执行抓取():
    下载索引 = 获取所有下载索引()["list"]
    下载索引 = [item["链接"] for item in 下载索引]

    logger.info(f"共有 {len(下载索引)} 个下载索引")

    for index, item in enumerate(下载索引):
        logger.info(f"开始下载 {item} ({index + 1}/{len(下载索引)})")
        # os 执行命令
        os.system(f"yutto {' '.join(命令行参数)} {item}")

        logger.info(f"{item} 抓取完成，等待10秒 ({index + 1}/{len(下载索引)})")
        time.sleep(10)

    logger.info("所有下载完成")


if __name__ == "__main__":
    while True:
        执行抓取()
        logger.info(f"抓取完成，等待3小时")
        time.sleep(3 * 60 * 60)
