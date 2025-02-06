from __future__ import annotations

import asyncio
import re
from typing import TYPE_CHECKING

from yutto._typing import EpisodeData, FId, MId
from yutto.api.space import get_favourite_avids, get_favourite_info, get_user_name
from yutto.api.ugc_video import UgcVideoListItem, get_ugc_video_list
from yutto.exceptions import NotFoundError
from yutto.extractor._abc import BatchExtractor
from yutto.extractor.common import extract_ugc_video_data
from yutto.mux import 检查视频是否下载过, 单个收藏夹最大允许重复次数
from yutto.utils.asynclib import CoroutineWrapper
from yutto.utils.console.logger import Badge, Logger
from yutto.utils.fetcher import Fetcher, FetcherContext
from yutto.utils.filter import Filter

if TYPE_CHECKING:
    import argparse

    import httpx


class FavouritesExtractor(BatchExtractor):
    """用户单一收藏夹"""

    REGEX_FAV = re.compile(
        r"https?://space\.bilibili\.com/(?P<mid>\d+)/favlist\?fid=(?P<fid>\d+)((&ftype=create)|$)"
    )

    mid: MId
    fid: FId

    def match(self, url: str) -> bool:
        if match_obj := self.REGEX_FAV.match(url):
            self.mid = MId(match_obj.group("mid"))
            self.fid = FId(match_obj.group("fid"))
            return True
        else:
            return False

    async def extract(
        self, ctx: FetcherContext, client: httpx.AsyncClient, args: argparse.Namespace
    ) -> list[CoroutineWrapper[EpisodeData | None] | None]:
        username, favourite_info = await asyncio.gather(
            get_user_name(ctx, client, self.mid),
            get_favourite_info(ctx, client, self.fid),
        )
        Logger.custom(
            favourite_info["title"], Badge("收藏夹", fore="black", back="cyan")
        )

        ugc_video_info_list: list[tuple[UgcVideoListItem, str, int, str]] = []

        repeat = 0
        for avid in await get_favourite_avids(ctx, client, self.fid):
            try:
                ugc_video_list = await get_ugc_video_list(ctx, client, avid)
                # 在使用 SESSDATA 时，如果不去事先 touch 一下视频链接的话，是无法获取 episode_data 的
                # 至于为什么前面那俩（投稿视频页和番剧页）不需要额外 touch，因为在 get_redirected_url 阶段连接过了呀
                if not Filter.verify_timer(ugc_video_list["pubdate"]):
                    Logger.debug(
                        f"因为发布时间为 {ugc_video_list['pubdate']}，跳过 {ugc_video_list['title']}"
                    )
                    continue
                await Fetcher.touch_url(ctx, client, avid.to_url())

                if 检查视频是否下载过(str(avid)):
                    Logger.info(f"已存在 {avid}，跳过")
                    repeat += 1
                    if repeat >= 单个收藏夹最大允许重复次数:
                        Logger.info(
                            f"重复次数达到 {单个收藏夹最大允许重复次数}，跳过剩余视频"
                        )
                        break

                    continue
                else:
                    # 遇到没下载过的视频会重置repeat次数，避免多个收藏夹命中同一个视频
                    repeat = max(repeat - 1, 0)

                for ugc_video_item in ugc_video_list["pages"]:
                    ugc_video_info_list.append(
                        (
                            ugc_video_item,
                            ugc_video_list["title"],
                            ugc_video_list["pubdate"],
                            ugc_video_item["metadata"].get("actor")[0].get("name"),
                        )
                    )
            except NotFoundError as e:
                Logger.error(e.message)
                continue

        return [
            CoroutineWrapper(
                extract_ugc_video_data(
                    ctx,
                    client,
                    ugc_video_item["avid"],
                    ugc_video_item,
                    args,
                    {
                        "title": title,
                        "username": actor_name,
                        "series_title": favourite_info["title"],
                        "pubdate": pubdate,
                    },
                    "{owner_uid}-{username}/{bvid}-{name}-{id}",
                )
            )
            for ugc_video_item, title, pubdate, actor_name in ugc_video_info_list
        ]
