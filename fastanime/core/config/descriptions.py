# GeneralConfig
from .defaults import SESSIONS_DIR

GENERAL_PYGMENT_STYLE = "The pygment style to use"
GENERAL_API_CLIENT = "The media database API to use (e.g., 'anilist', 'jikan')."
GENERAL_PREFERRED_TRACKER = (
    "The preferred watch history tracker (local,remote) in cases of conflicts"
)
GENERAL_PROVIDER = "The default anime provider to use for scraping."
GENERAL_SELECTOR = "The interactive selector tool to use for menus."
GENERAL_AUTO_SELECT_ANIME_RESULT = (
    "Automatically select the best-matching search result from a provider."
)
GENERAL_ICONS = "Display emoji icons in the user interface."
GENERAL_PREVIEW = "Type of preview to display in selectors."
GENERAL_IMAGE_RENDERER = (
    "The command-line tool to use for rendering images in the terminal."
)
GENERAL_MANGA_VIEWER = "The external application to use for viewing manga pages."
GENERAL_CHECK_FOR_UPDATES = (
    "Automatically check for new versions of FastAnime on startup."
)
GENERAL_CACHE_REQUESTS = (
    "Enable caching of network requests to speed up subsequent operations."
)
GENERAL_MAX_CACHE_LIFETIME = "Maximum lifetime for a cached request in DD:HH:MM format."
GENERAL_NORMALIZE_TITLES = (
    "Attempt to normalize provider titles to match AniList titles."
)
GENERAL_DISCORD = "Enable Discord Rich Presence to show your current activity."
GENERAL_RECENT = "Number of recently watched anime to keep in history."

# StreamConfig
STREAM_PLAYER = "The media player to use for streaming."
STREAM_QUALITY = "Preferred stream quality."
STREAM_TRANSLATION_TYPE = "Preferred audio/subtitle language type."
STREAM_SERVER = (
    "The default server to use from a provider. 'top' uses the first available."
)
STREAM_AUTO_NEXT = "Automatically play the next episode when the current one finishes."
STREAM_CONTINUE_FROM_WATCH_HISTORY = (
    "Automatically resume playback from the last known episode and position."
)
STREAM_PREFERRED_WATCH_HISTORY = (
    "Which watch history to prioritize: local file or remote AniList progress."
)
STREAM_AUTO_SKIP = "Automatically skip openings/endings if skip data is available."
STREAM_EPISODE_COMPLETE_AT = (
    "Percentage of an episode to watch before it's marked as complete."
)
STREAM_YTDLP_FORMAT = "The format selection string for yt-dlp."
STREAM_FORCE_FORWARD_TRACKING = (
    "Prevent updating AniList progress to a lower episode number."
)
STREAM_DEFAULT_MEDIA_LIST_TRACKING = (
    "Default behavior for tracking progress on AniList."
)
STREAM_SUB_LANG = "Preferred language code for subtitles (e.g., 'en', 'es')."
STREAM_USE_IPC = "Use IPC communication with the player for advanced features like episode navigation."

# ServiceConfig
SERVICE_ENABLED = "Whether the background service should be enabled by default."
SERVICE_WATCHLIST_CHECK_INTERVAL = (
    "Minutes between checking AniList watchlist for new episodes."
)
SERVICE_QUEUE_PROCESS_INTERVAL = "Minutes between processing the download queue."
SERVICE_MAX_CONCURRENT_DOWNLOADS = "Maximum number of concurrent downloads."
SERVICE_AUTO_RETRY_COUNT = "Number of times to retry failed downloads."
SERVICE_CLEANUP_COMPLETED_DAYS = (
    "Days to keep completed/failed jobs in queue before cleanup."
)
SERVICE_NOTIFICATION_ENABLED = "Whether to show notifications for new episodes."

# FzfConfig
FZF_HEADER_COLOR = "RGB color for the main TUI header."
FZF_PREVIEW_HEADER_COLOR = "RGB color for preview pane headers."
FZF_PREVIEW_SEPARATOR_COLOR = "RGB color for preview pane separators."
FZF_OPTS = "The FZF options, formatted with leading tabs for the config file."
FZF_HEADER_ASCII_ART = "The ASCII art to display as a header in the FZF interface."


# RofiConfig
ROFI_THEME_MAIN = "Path to the main Rofi theme file."
ROFI_THEME_PREVIEW = "Path to the Rofi theme file for previews."
ROFI_THEME_CONFIRM = "Path to the Rofi theme file for confirmation prompts."
ROFI_THEME_INPUT = "Path to the Rofi theme file for user input prompts."

# MpvConfig
MPV_ARGS = "Comma-separated arguments to pass to the MPV player."
MPV_PRE_ARGS = "Comma-separated arguments to prepend before the MPV command."

# VlcConfig
VLC_ARGS = "Comma-separated arguments to pass to the Vlc player."

# AnilistConfig
ANILIST_PER_PAGE = "Number of items to fetch per page from AniList."
ANILIST_SORT_BY = "Default sort order for AniList search results."
ANILIST_MEDIA_LIST_SORT_BY = "Default medai list sort order for AniList search results."
ANILIST_PREFERRED_LANGUAGE = "Preferred language for anime titles from AniList."

# DownloadsConfig
DOWNLOADS_DOWNLOADER = "The downloader to use"
DOWNLOADS_DOWNLOADS_DIR = "The default directory to save downloaded anime."
DOWNLOADS_ENABLE_TRACKING = "Enable download tracking and management"
DOWNLOADS_AUTO_ORGANIZE = "Automatically organize downloads by anime title"
DOWNLOADS_MAX_CONCURRENT = "Maximum concurrent downloads"
DOWNLOADS_AUTO_CLEANUP_FAILED = "Automatically cleanup failed downloads"
DOWNLOADS_RETENTION_DAYS = "Days to keep failed downloads before cleanup"
DOWNLOADS_SYNC_WITH_WATCH_HISTORY = "Sync download status with watch history"
DOWNLOADS_AUTO_MARK_OFFLINE = (
    "Automatically mark downloaded episodes as available offline"
)
DOWNLOADS_NAMING_TEMPLATE = "File naming template for downloaded episodes"
DOWNLOADS_PREFERRED_QUALITY = "Preferred download quality"
DOWNLOADS_DOWNLOAD_SUBTITLES = "Download subtitles when available"
DOWNLOADS_SUBTITLE_LANGUAGES = "Preferred subtitle languages"
DOWNLOADS_QUEUE_MAX_SIZE = "Maximum number of items in download queue"
DOWNLOADS_AUTO_START_DOWNLOADS = "Automatically start downloads when items are queued"
DOWNLOADS_RETRY_ATTEMPTS = "Number of retry attempts for failed downloads"
DOWNLOADS_RETRY_DELAY = "Delay between retry attempts in seconds"

# RegistryConfig
MEDIA_REGISTRY_DIR = "The default directory to save media registry"
MEDIA_REGISTRY_INDEX_DIR = "The default directory to save media registry index"

# AppConfig
APP_GENERAL = "General configuration settings for application behavior."
APP_STREAM = "Settings related to video streaming and playback."
APP_DOWNLOADS = "Settings related to downloading"
APP_ANILIST = "Configuration for AniList API integration."
APP_JIKAN = "Configuration for Jikan API integration."
APP_SERVICE = "Configuration for the background download service."
APP_FZF = "Settings for the FZF selector interface."
APP_ROFI = "Settings for the Rofi selector interface."
APP_MPV = "Configuration for the MPV media player."
APP_MEDIA_REGISTRY = "Configuration for the media registry."
APP_SESSIONS = "Configuration for sessions."

# session config
SESSIONS_DIR = "The default directory to save sessions."
