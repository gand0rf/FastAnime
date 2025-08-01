from typing import TYPE_CHECKING

import click
from fastanime.cli.service.player.service import PlayerService

from ...core.config import AppConfig
from ...core.exceptions import FastAnimeError
from ..utils.completion import anime_titles_shell_complete
from . import examples

if TYPE_CHECKING:
    from typing import TypedDict

    from typing_extensions import Unpack

    from ...libs.provider.anime.base import BaseAnimeProvider
    from ...libs.provider.anime.types import Anime
    from ...libs.selectors.base import BaseSelector

    class Options(TypedDict):
        anime_title: list[str]
        episode_range: str | None


@click.command(
    help="This subcommand directly interacts with the provider to enable basic streaming. Useful for binging anime.",
    short_help="Binge anime",
    epilog=examples.search,
)
@click.option(
    "--anime-title",
    "-t",
    required=True,
    shell_complete=anime_titles_shell_complete,
    multiple=True,
    help="Specify which anime to download",
)
@click.option(
    "--episode-range",
    "-r",
    help="A range of episodes to binge (start-end)",
)
@click.pass_obj
def search(config: AppConfig, **options: "Unpack[Options]"):
    from rich import print
    from rich.progress import Progress

    from ...core.exceptions import FastAnimeError
    from ...libs.provider.anime.params import (
        AnimeParams,
        SearchParams,
    )
    from ...libs.provider.anime.provider import create_provider
    from ...libs.selectors.selector import create_selector

    provider = create_provider(config.general.provider)
    selector = create_selector(config)

    anime_titles = options["anime_title"]
    print(f"[green bold]Streaming:[/] {anime_titles}")
    for anime_title in anime_titles:
        # ---- search for anime ----
        print(f"[green bold]Searching for:[/] {anime_title}")
        with Progress() as progress:
            progress.add_task("Fetching Search Results...", total=None)
            search_results = provider.search(
                SearchParams(
                    query=anime_title, translation_type=config.stream.translation_type
                )
            )
        if not search_results:
            raise FastAnimeError("No results were found matching your query")

        _search_results = {
            search_result.title: search_result
            for search_result in search_results.results
        }

        selected_anime_title = selector.choose(
            "Select Anime", list(_search_results.keys())
        )
        if not selected_anime_title:
            raise FastAnimeError("No title selected")
        anime_result = _search_results[selected_anime_title]

        # ---- fetch selected anime ----
        with Progress() as progress:
            progress.add_task("Fetching Anime...", total=None)
            anime = provider.get(AnimeParams(id=anime_result.id, query=anime_title))

        if not anime:
            raise FastAnimeError(f"Failed to fetch anime {anime_result.title}")

        available_episodes: list[str] = sorted(
            getattr(anime.episodes, config.stream.translation_type), key=float
        )

        if options["episode_range"]:
            from ..utils.parser import parse_episode_range

            try:
                episodes_range = parse_episode_range(
                    options["episode_range"], available_episodes
                )

                for episode in episodes_range:
                    stream_anime(
                        config, provider, selector, anime, episode, anime_title
                    )
            except (ValueError, IndexError) as e:
                raise FastAnimeError(f"Invalid episode range: {e}") from e
        else:
            episode = selector.choose(
                "Select Episode",
                getattr(anime.episodes, config.stream.translation_type),
            )
            if not episode:
                raise FastAnimeError("No episode selected")
            stream_anime(config, provider, selector, anime, episode, anime_title)


def stream_anime(
    config: AppConfig,
    provider: "BaseAnimeProvider",
    selector: "BaseSelector",
    anime: "Anime",
    episode: str,
    anime_title: str,
):
    from rich import print
    from rich.progress import Progress

    from ...libs.player.params import PlayerParams
    from ...libs.provider.anime.params import EpisodeStreamsParams

    player_service = PlayerService(config, provider)

    with Progress() as progress:
        progress.add_task("Fetching Episode Streams...", total=None)
        streams = provider.episode_streams(
            EpisodeStreamsParams(
                anime_id=anime.id,
                query=anime_title,
                episode=episode,
                translation_type=config.stream.translation_type,
            )
        )
        if not streams:
            raise FastAnimeError(
                f"Failed to get streams for anime: {anime.title}, episode: {episode}"
            )

    if config.stream.server.value == "TOP":
        with Progress() as progress:
            progress.add_task("Fetching top server...", total=None)
            server = next(streams, None)
            if not server:
                raise FastAnimeError(
                    f"Failed to get server for anime: {anime.title}, episode: {episode}"
                )
    else:
        with Progress() as progress:
            progress.add_task("Fetching servers", total=None)
            servers = {server.name: server for server in streams}
        servers_names = list(servers.keys())
        if config.stream.server.value in servers_names:
            server = servers[config.stream.server.value]
        else:
            server_name = selector.choose("Select Server", servers_names)
            if not server_name:
                raise FastAnimeError("Server not selected")
            server = servers[server_name]
    stream_link = server.links[0].link
    if not stream_link:
        raise FastAnimeError(
            f"Failed to get stream link for anime: {anime.title}, episode: {episode}"
        )
    print(f"[green bold]Now Streaming:[/] {anime.title} Episode: {episode}")

    player_service.play(
        PlayerParams(
            url=stream_link,
            title=f"{anime.title}; Episode {episode}",
            query=anime_title,
            episode=episode,
            subtitles=[sub.url for sub in server.subtitles],
            headers=server.headers,
        ),
        anime,
    )
