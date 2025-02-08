from nocodb.nocodb import NocoDBProject, APIToken
from nocodb.infra.requests_client import NocoDBRequestsClient
from nocodb.filters import LikeFilter, EqFilter, And

# Usage with API Token
client = NocoDBRequestsClient(
    # Your API Token retrieved from NocoDB conf
    APIToken("mvLZoKHMk4qAMvoS6YrKw2XoKPdH-gDBEMlZSvsQ"),
    # Your nocodb root path
    "http://localhost:8080",
)

# 🔗 elchicodepython/python-nocodb: NocoDB Python API Client
# https://github.com/ElChicoDePython/python-nocodb

B站数据库 = NocoDBProject("noco", "plmocv0je8gfamj")
收藏夹下载索引_id = "m9u9qneyouwzm6i"
下载视频记录_id = "m7ks6h2zrkoqgbm"
之前抓取的视频记录_id = "mntafuio1pn0a2a"

单个收藏夹最大允许重复次数 = 3


def 检查视频是否下载过(bvid: str) -> bool:
    之前是否下载过 = client.table_find_one(
        B站数据库,
        之前抓取的视频记录_id,
        filter_obj=EqFilter("bvid", bvid),
        params={"sort": "-created_at"},
    )
    if 之前是否下载过:
        return True
    return client.table_find_one(
        B站数据库,
        下载视频记录_id,
        filter_obj=EqFilter("bvid", bvid),
        params={"sort": "-created_at"},
    )


def 插入视频下载记录(视频信息: dict):
    return client.table_row_create(
        B站数据库,
        下载视频记录_id,
        视频信息,
    )


def 获取所有下载索引():
    return client.table_row_list(
        B站数据库,
        收藏夹下载索引_id,
        params={"limit": 1000},
        filter_obj=EqFilter("视频抓取", True),
    )


if __name__ == "__main__":
    print(获取所有下载索引())
