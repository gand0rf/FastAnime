import logging
import os
import re
from typing import List, Optional

from ...core.config import AppConfig
from ...core.constants import APP_CACHE_DIR, PLATFORM, SCRIPTS_DIR
from ...libs.media_api.types import MediaItem
from . import ansi
from .preview_workers import PreviewWorkerManager

logger = logging.getLogger(__name__)

os.environ["SHELL"] = "bash"

PREVIEWS_CACHE_DIR = APP_CACHE_DIR / "previews"
IMAGES_CACHE_DIR = PREVIEWS_CACHE_DIR / "images"
INFO_CACHE_DIR = PREVIEWS_CACHE_DIR / "info"

FZF_SCRIPTS_DIR = SCRIPTS_DIR / "fzf"
TEMPLATE_PREVIEW_SCRIPT = (FZF_SCRIPTS_DIR / "preview.template.sh").read_text(
    encoding="utf-8"
)
DYNAMIC_PREVIEW_SCRIPT = (FZF_SCRIPTS_DIR / "dynamic_preview.template.sh").read_text(
    encoding="utf-8"
)

EPISODE_PATTERN = re.compile(r"^Episode\s+(\d+)\s-\s.*")

# Global preview worker manager instance
_preview_manager: Optional[PreviewWorkerManager] = None


def create_preview_context():
    """
    Create a context manager for preview operations.

    This can be used in menu functions to ensure proper cleanup:

    ```python
    with create_preview_context() as preview_ctx:
        preview_script = preview_ctx.get_anime_preview(items, titles, config)
        # ... use preview_script
    # Workers are automatically cleaned up here
    ```

    Returns:
        PreviewContext: A context manager for preview operations
    """
    return PreviewContext()


class PreviewContext:
    """Context manager for preview operations with automatic cleanup."""

    def __init__(self):
        self._manager = None

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self._manager:
            try:
                self._manager.shutdown_all(wait=False, timeout=3.0)
            except Exception as e:
                logger.warning(f"Failed to cleanup preview context: {e}")

    def get_anime_preview(
        self, items: List[MediaItem], titles: List[str], config: AppConfig
    ) -> str:
        """Get anime preview script with managed workers."""
        if not self._manager:
            self._manager = _get_preview_manager()
        return get_anime_preview(items, titles, config)

    def get_episode_preview(
        self, episodes: List[str], media_item: MediaItem, config: AppConfig
    ) -> str:
        """Get episode preview script with managed workers."""
        if not self._manager:
            self._manager = _get_preview_manager()
        return get_episode_preview(episodes, media_item, config)

    def get_dynamic_anime_preview(self, config: AppConfig) -> str:
        """Get dynamic anime preview script for search functionality."""
        if not self._manager:
            self._manager = _get_preview_manager()
        return get_dynamic_anime_preview(config)

    def cancel_all_tasks(self) -> int:
        """Cancel all running preview tasks."""
        if not self._manager:
            return 0

        cancelled = 0
        if self._manager._preview_worker:
            cancelled += self._manager._preview_worker.cancel_all_tasks()
        if self._manager._episode_worker:
            cancelled += self._manager._episode_worker.cancel_all_tasks()
        return cancelled

    def get_status(self) -> dict:
        """Get status of workers in this context."""
        if self._manager:
            return self._manager.get_status()
        return {"preview_worker": None, "episode_worker": None}


def get_anime_preview(
    items: List[MediaItem], titles: List[str], config: AppConfig
) -> str:
    """
    Generate anime preview script and start background caching.

    Args:
        items: List of media items to preview
        titles: Corresponding titles for each media item
        config: Application configuration

    Returns:
        Preview script content for fzf
    """
    # Ensure cache directories exist on startup
    IMAGES_CACHE_DIR.mkdir(parents=True, exist_ok=True)
    INFO_CACHE_DIR.mkdir(parents=True, exist_ok=True)

    HEADER_COLOR = config.fzf.preview_header_color.split(",")
    SEPARATOR_COLOR = config.fzf.preview_separator_color.split(",")

    preview_script = TEMPLATE_PREVIEW_SCRIPT

    # Start the managed background caching
    try:
        preview_manager = _get_preview_manager()
        worker = preview_manager.get_preview_worker()
        worker.cache_anime_previews(items, titles, config)
        logger.debug("Started background caching for anime previews")
    except Exception as e:
        logger.error(f"Failed to start background caching: {e}")
        # Continue with script generation even if caching fails

    # Prepare values to inject into the template
    path_sep = "\\" if PLATFORM == "win32" else "/"

    # Format the template with the dynamic values
    replacements = {
        "PREVIEW_MODE": config.general.preview,
        "IMAGE_CACHE_PATH": str(IMAGES_CACHE_DIR),
        "INFO_CACHE_PATH": str(INFO_CACHE_DIR),
        "PATH_SEP": path_sep,
        "IMAGE_RENDERER": config.general.image_renderer,
        # Color codes
        "C_TITLE": ansi.get_true_fg(HEADER_COLOR, bold=True),
        "C_KEY": ansi.get_true_fg(HEADER_COLOR, bold=True),
        "C_VALUE": ansi.get_true_fg(HEADER_COLOR, bold=True),
        "C_RULE": ansi.get_true_fg(SEPARATOR_COLOR, bold=True),
        "RESET": ansi.RESET,
        "PREFIX": "",
    }

    for key, value in replacements.items():
        preview_script = preview_script.replace(f"{{{key}}}", value)

    return preview_script


def get_episode_preview(
    episodes: List[str], media_item: MediaItem, config: AppConfig
) -> str:
    """
    Generate episode preview script and start background caching.

    Args:
        episodes: List of episode identifiers
        media_item: Media item containing episode data
        config: Application configuration

    Returns:
        Preview script content for fzf
    """
    IMAGES_CACHE_DIR.mkdir(parents=True, exist_ok=True)
    INFO_CACHE_DIR.mkdir(parents=True, exist_ok=True)

    HEADER_COLOR = config.fzf.preview_header_color.split(",")
    SEPARATOR_COLOR = config.fzf.preview_separator_color.split(",")

    preview_script = TEMPLATE_PREVIEW_SCRIPT

    # Start managed background caching for episodes
    try:
        preview_manager = _get_preview_manager()
        worker = preview_manager.get_episode_worker()
        worker.cache_episode_previews(episodes, media_item, config)
        logger.debug("Started background caching for episode previews")
    except Exception as e:
        logger.error(f"Failed to start episode background caching: {e}")
        # Continue with script generation even if caching fails

    # Prepare values to inject into the template
    path_sep = "\\" if PLATFORM == "win32" else "/"

    # Format the template with the dynamic values
    replacements = {
        "PREVIEW_MODE": config.general.preview,
        "IMAGE_CACHE_PATH": str(IMAGES_CACHE_DIR),
        "INFO_CACHE_PATH": str(INFO_CACHE_DIR),
        "PATH_SEP": path_sep,
        "IMAGE_RENDERER": config.general.image_renderer,
        # Color codes
        "C_TITLE": ansi.get_true_fg(HEADER_COLOR, bold=True),
        "C_KEY": ansi.get_true_fg(HEADER_COLOR, bold=True),
        "C_VALUE": ansi.get_true_fg(HEADER_COLOR, bold=True),
        "C_RULE": ansi.get_true_fg(SEPARATOR_COLOR, bold=True),
        "RESET": ansi.RESET,
        "PREFIX": f"{media_item.title.english}_Episode_",
    }

    for key, value in replacements.items():
        preview_script = preview_script.replace(f"{{{key}}}", value)

    return preview_script


def get_dynamic_anime_preview(config: AppConfig) -> str:
    """
    Generate dynamic anime preview script for search functionality.

    This is different from regular anime preview because:
    1. We don't have media items upfront
    2. The preview needs to work with search results as they come in
    3. Preview is handled entirely in shell by parsing JSON results

    Args:
        config: Application configuration

    Returns:
        Preview script content for fzf dynamic search
    """
    # Ensure cache directories exist
    IMAGES_CACHE_DIR.mkdir(parents=True, exist_ok=True)
    INFO_CACHE_DIR.mkdir(parents=True, exist_ok=True)

    HEADER_COLOR = config.fzf.preview_header_color.split(",")
    SEPARATOR_COLOR = config.fzf.preview_separator_color.split(",")

    # Use the dynamic preview script template
    preview_script = DYNAMIC_PREVIEW_SCRIPT

    # We need to return the path to the search results file
    from ...core.constants import APP_CACHE_DIR

    search_cache_dir = APP_CACHE_DIR / "search"
    search_results_file = search_cache_dir / "current_search_results.json"

    # Prepare values to inject into the template
    path_sep = "\\" if PLATFORM == "win32" else "/"

    # Format the template with the dynamic values
    replacements = {
        "PREVIEW_MODE": config.general.preview,
        "IMAGE_CACHE_PATH": str(IMAGES_CACHE_DIR),
        "INFO_CACHE_PATH": str(INFO_CACHE_DIR),
        "PATH_SEP": path_sep,
        "IMAGE_RENDERER": config.general.image_renderer,
        "SEARCH_RESULTS_FILE": str(search_results_file),
        # Color codes
        "C_TITLE": ansi.get_true_fg(HEADER_COLOR, bold=True),
        "C_KEY": ansi.get_true_fg(HEADER_COLOR, bold=True),
        "C_VALUE": ansi.get_true_fg(HEADER_COLOR, bold=True),
        "C_RULE": ansi.get_true_fg(SEPARATOR_COLOR, bold=True),
        "RESET": ansi.RESET,
    }

    for key, value in replacements.items():
        preview_script = preview_script.replace(f"{{{key}}}", value)

    return preview_script


def _get_preview_manager() -> PreviewWorkerManager:
    """Get or create the global preview worker manager."""
    global _preview_manager
    if _preview_manager is None:
        _preview_manager = PreviewWorkerManager(IMAGES_CACHE_DIR, INFO_CACHE_DIR)
    return _preview_manager


def shutdown_preview_workers(wait: bool = True, timeout: Optional[float] = 5.0) -> None:
    """
    Shutdown all preview workers.

    Args:
        wait: Whether to wait for tasks to complete
        timeout: Maximum time to wait for shutdown
    """
    global _preview_manager
    if _preview_manager:
        _preview_manager.shutdown_all(wait=wait, timeout=timeout)
        _preview_manager = None


def get_preview_worker_status() -> dict:
    """Get status of all preview workers."""
    global _preview_manager
    if _preview_manager:
        return _preview_manager.get_status()
    return {"preview_worker": None, "episode_worker": None}
