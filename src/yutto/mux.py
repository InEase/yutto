from nocodb.nocodb import NocoDBProject, APIToken
from nocodb.infra.requests_client import NocoDBRequestsClient


# Usage with API Token
client = NocoDBRequestsClient(
    # Your API Token retrieved from NocoDB conf
    APIToken("mvLZoKHMk4qAMvoS6YrKw2XoKPdH-gDBEMlZSvsQ"),
    # Your nocodb root path
    "http://localhost:8080",
)

B站数据库 = NocoDBProject("noco", "plmocv0je8gfamj")
收藏夹下载索引_id = "m9u9qneyouwzm6i"
下载视频记录_id = "m7ks6h2zrkoqgbm"
