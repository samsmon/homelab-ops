#!/opt/pipx/venvs/gamdl/bin/python
"""gamdl wrapper that adds randomized delays so bulk downloads don't hammer Apple's API.

gamdl has no native rate limiting (only retries on 429/5xx), so this monkeypatches
AppleMusicDownloader in-process, then runs the normal gamdl CLI. All gamdl args pass through.

  gamdl-safe -r urls.txt          # one URL per line, processed sequentially
  gamdl-safe <album-url> ...

Delays (seconds, "min-max", random uniform), override via env:
  GAMDL_TRACK_DELAY   default 8-20     after each downloaded track
  GAMDL_ALBUM_DELAY   default 60-180   before each URL (album/playlist/artist) after the first
  GAMDL_STOREFRONT    default jp       rewrite URL storefront (id/us/...) so titles are in original language
                                       (jp gives e.g. "01 心の奥.m4a" where id gave "Deep Down"); set empty to disable
Single instance only (flock on /tmp/gamdl-safe.lock).
"""
import asyncio
import fcntl
import os
import random
import re
import sys


def _rng(name, default):
    lo, hi = (float(x) for x in os.environ.get(name, default).split("-"))
    return lo, hi


TRACK = _rng("GAMDL_TRACK_DELAY", "8-20")
ALBUM = _rng("GAMDL_ALBUM_DELAY", "60-180")
STOREFRONT = os.environ.get("GAMDL_STOREFRONT", "jp").strip().lower()  # "" disables rewriting

lock = open("/tmp/gamdl-safe.lock", "w")
try:
    fcntl.flock(lock, fcntl.LOCK_EX | fcntl.LOCK_NB)
except OSError:
    sys.exit("gamdl-safe already running (lock held) - refusing to run in parallel")

from gamdl.downloader.downloader import AppleMusicDownloader  # noqa: E402
from gamdl.downloader.exceptions import (  # noqa: E402
    GamdlDownloaderMediaFileExistsError,
    GamdlDownloaderSyncedLyricsOnlyError,
)

_orig_get = AppleMusicDownloader.get_download_item_from_url
_orig_download = AppleMusicDownloader.download
_state = {"first": True}


def _storefront(url):
    """Rewrite music.apple.com/<storefront>/ to the configured one (default jp) so titles come back in original language."""
    if not STOREFRONT:
        return url
    return re.sub(r"(https?://(?:classical\.)?music\.apple\.com/)[a-z]{2}/", rf"\g<1>{STOREFRONT}/", url, count=1)


async def _get(self, *args, **kwargs):
    if args and isinstance(args[0], str):
        new = _storefront(args[0])
        if new != args[0]:
            print(f"[gamdl-safe] storefront -> {STOREFRONT}: {new}", flush=True)
        args = (new, *args[1:])
    elif isinstance(kwargs.get("url"), str):
        kwargs["url"] = _storefront(kwargs["url"])
    if not _state["first"]:
        d = random.uniform(*ALBUM)
        print(f"[gamdl-safe] album delay {d:.0f}s", flush=True)
        await asyncio.sleep(d)
    _state["first"] = False
    async for item in _orig_get(self, *args, **kwargs):
        yield item


async def _download_delayed(self, item):
    try:
        await _orig_download(self, item)
    except (GamdlDownloaderMediaFileExistsError, GamdlDownloaderSyncedLyricsOnlyError):
        raise  # nothing fetched, no need to wait
    except BaseException:
        await asyncio.sleep(random.uniform(*TRACK) * 2)  # errors back off harder
        raise
    d = random.uniform(*TRACK)
    print(f"[gamdl-safe] track delay {d:.0f}s", flush=True)
    await asyncio.sleep(d)


AppleMusicDownloader.get_download_item_from_url = _get
AppleMusicDownloader.download = _download_delayed

from gamdl.cli.cli import main  # noqa: E402

main()
