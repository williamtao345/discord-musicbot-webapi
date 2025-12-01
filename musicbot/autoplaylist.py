import asyncio
import logging
import pathlib
import shutil
import time
from collections import UserList
from typing import TYPE_CHECKING, Dict, List, Optional, Set

from .constants import (
    APL_FILE_APLCOPY,
    APL_FILE_DEFAULT,
    APL_FILE_HISTORY,
    OLD_BUNDLED_AUTOPLAYLIST_FILE,
    OLD_DEFAULT_AUTOPLAYLIST_FILE,
)

if TYPE_CHECKING:
    from .bot import MusicBot

    StrUserList = UserList[str]
else:
    StrUserList = UserList

log = logging.getLogger(__name__)


class AutoPlaylist(StrUserList):
    def __init__(self, filename: pathlib.Path, bot: "MusicBot") -> None:
        super().__init__()

        self._bot: "MusicBot" = bot
        self._file: pathlib.Path = filename
        self._removed_file = filename.with_name(f"{filename.stem}.removed.log")

        self._update_lock: asyncio.Lock = asyncio.Lock()
        self._file_lock: asyncio.Lock = asyncio.Lock()
        self._is_loaded: bool = False

    @property
    def filename(self) -> str:
        """The base file name of this playlist."""
        return self._file.name

    @property
    def loaded(self) -> bool:
        """
        Returns the load status of this playlist.
        When False, no playlist data will be available.
        """
        return self._is_loaded

    @property
    def rmlog_file(self) -> pathlib.Path:
        """Returns the generated removal log file name."""
        return self._removed_file

    def create_file(self) -> None:
        """Creates the playlist file if it does not exist."""
        if not self._file.is_file():
            self._file.touch(exist_ok=True)

    async def load(self, force: bool = False) -> None:
        """
        Loads the playlist file if it has not been loaded.
        """
        # ignore loaded lists unless forced.
        if (self._is_loaded or self._file_lock.locked()) and not force:
            return

        # Load the actual playlist file.
        async with self._file_lock:
            try:
                self.data = self._read_playlist()
            except OSError:
                log.warning("Error loading auto playlist file:  %s", self._file)
                self.data = []
                self._is_loaded = False
                return
            self._is_loaded = True

    def _read_playlist(self) -> List[str]:
        """
        Read and parse the playlist file for track entries.
        """
        # Comments in apl files are only handled based on start-of-line.
        # Inline comments are not supported due to supporting non-URL entries.
        comment_char = "#"

        # Read in the file and add non-comments to the playlist.
        playlist: List[str] = []
        with open(self._file, "r", encoding="utf8") as fh:
            for line in fh:
                line = line.strip()
                if not line or line.startswith(comment_char):
                    continue
                playlist.append(line)
        return playlist

    async def remove_track(
        self,
        song_subject: str,
        *,
        ex: Optional[Exception] = None,
        delete_from_ap: bool = False,
    ) -> None:
        """
        Handle clearing the given `song_subject` from the autoplaylist queue,
        and optionally from the configured autoplaylist file.

        :param: ex:  an exception that is given as the reason for removal.
        :param: delete_from_ap:  should the configured list file be updated?
        """
        if song_subject not in self.data:
            return

        async with self._update_lock:
            self.data.remove(song_subject)
            log.info(
                "Removing%s song from playlist, %s: %s",
                " unplayable" if ex and not isinstance(ex, UserWarning) else "",
                self._file.name,
                song_subject,
            )

            if not self._removed_file.is_file():
                self._removed_file.touch(exist_ok=True)

            try:
                with open(self._removed_file, "a", encoding="utf8") as f:
                    ctime = time.ctime()
                    # add 10 spaces to line up with # Reason:
                    e_str = str(ex).replace("\n", "\n#" + " " * 10)
                    sep = "#" * 32
                    f.write(
                        f"# Entry removed {ctime}\n"
                        f"# Track:  {song_subject}\n"
                        f"# Reason: {e_str}\n"
                        f"\n{sep}\n\n"
                    )
            except (OSError, PermissionError, FileNotFoundError, IsADirectoryError):
                log.exception(
                    "Could not log information about the playlist URL removal."
                )

            if delete_from_ap:
                log.info("Updating playlist file...")

                def _filter_replace(line: str, url: str) -> str:
                    target = line.strip()
                    if target == url:
                        return f"# Removed # {url}"
                    return line

                # read the original file in and update lines with the URL.
                # this is done to preserve the comments and formatting.
                try:
                    data = self._file.read_text(encoding="utf8").split("\n")
                    data = [_filter_replace(x, song_subject) for x in data]
                    text = "\n".join(data)
                    self._file.write_text(text, encoding="utf8")
                except (OSError, PermissionError, FileNotFoundError):
                    log.exception("Failed to save playlist file:  %s", self._file)
                self._bot.filecache.remove_autoplay_cachemap_entry_by_url(song_subject)

    async def add_track(self, song_subject: str) -> None:
        """
        Add the given `song_subject` to the auto playlist file and in-memory
        list.  Does not update the player's current autoplaylist queue.
        """
        if song_subject in self.data:
            log.debug("URL already in playlist %s, ignoring", self._file.name)
            return

        async with self._update_lock:
            # Note, this does not update the player's copy of the list.
            self.data.append(song_subject)
            log.info(
                "Adding new URL to playlist, %s: %s",
                self._file.name,
                song_subject,
            )

            try:
                # make sure the file exists.
                if not self._file.is_file():
                    self._file.touch(exist_ok=True)

                # append to the file to preserve its formatting.
                with open(self._file, "r+", encoding="utf8") as fh:
                    lines = fh.readlines()
                    if not lines:
                        lines.append("# MusicBot Auto Playlist\n")
                    if lines[-1].endswith("\n"):
                        lines.append(f"{song_subject}\n")
                    else:
                        lines.append(f"\n{song_subject}\n")
                    fh.seek(0)
                    fh.writelines(lines)
            except (OSError, PermissionError, FileNotFoundError):
                log.exception("Failed to save playlist file:  %s", self._file)

    async def save(self) -> None:
        """
        Write current in-memory data to file (URLs only, one per line).
        This overwrites the file completely without preserving comments.
        """
        async with self._file_lock:
            try:
                content = "\n".join(self.data)
                if content and not content.endswith("\n"):
                    content += "\n"
                self._file.write_text(content, encoding="utf8")
                log.info("Saved playlist file: %s", self._file.name)
            except (OSError, PermissionError, FileNotFoundError):
                log.exception("Failed to save playlist file: %s", self._file)
                raise

    async def insert_track(self, index: int, url: str) -> None:
        """
        Insert a track at a specific index.

        :param index: Position to insert at (0-based)
        :param url: URL or search query to insert
        :raises IndexError: If index is out of bounds
        """
        async with self._update_lock:
            if index < 0 or index > len(self.data):
                raise IndexError(
                    f"Index {index} out of bounds for playlist of length {len(self.data)}"
                )
            self.data.insert(index, url)
            log.info(
                "Inserted track at index %d in playlist %s: %s",
                index,
                self._file.name,
                url,
            )
        await self.save()

    async def remove_at_index(self, index: int) -> str:
        """
        Remove a track by its index.

        :param index: Index of track to remove (0-based)
        :returns: The removed URL
        :raises IndexError: If index is out of bounds
        """
        async with self._update_lock:
            if index < 0 or index >= len(self.data):
                raise IndexError(
                    f"Index {index} out of bounds for playlist of length {len(self.data)}"
                )
            removed = self.data.pop(index)
            log.info(
                "Removed track at index %d from playlist %s: %s",
                index,
                self._file.name,
                removed,
            )
        await self.save()
        return removed

    async def move_track(self, from_index: int, to_index: int) -> None:
        """
        Move a track from one position to another.

        :param from_index: Current index of the track
        :param to_index: Target index for the track
        :raises IndexError: If either index is out of bounds
        """
        async with self._update_lock:
            if from_index < 0 or from_index >= len(self.data):
                raise IndexError(
                    f"from_index {from_index} out of bounds for playlist of length {len(self.data)}"
                )
            if to_index < 0 or to_index >= len(self.data):
                raise IndexError(
                    f"to_index {to_index} out of bounds for playlist of length {len(self.data)}"
                )
            track = self.data.pop(from_index)
            self.data.insert(to_index, track)
            log.info(
                "Moved track from index %d to %d in playlist %s",
                from_index,
                to_index,
                self._file.name,
            )
        await self.save()

    async def reorder(self, new_order: List[int]) -> None:
        """
        Reorder all tracks based on a list of indices.

        :param new_order: List of indices representing the new order
        :raises ValueError: If new_order doesn't match playlist length or contains invalid indices
        """
        async with self._update_lock:
            if len(new_order) != len(self.data):
                raise ValueError(
                    f"new_order length ({len(new_order)}) must match playlist length ({len(self.data)})"
                )
            if set(new_order) != set(range(len(self.data))):
                raise ValueError(
                    "new_order must contain each index exactly once"
                )
            self.data = [self.data[i] for i in new_order]
            log.info("Reordered playlist %s", self._file.name)
        await self.save()

    async def replace_track(self, index: int, new_url: str) -> str:
        """
        Replace a track at a specific index with a new URL.

        :param index: Index of track to replace
        :param new_url: New URL to put at that index
        :returns: The old URL that was replaced
        :raises IndexError: If index is out of bounds
        """
        async with self._update_lock:
            if index < 0 or index >= len(self.data):
                raise IndexError(
                    f"Index {index} out of bounds for playlist of length {len(self.data)}"
                )
            old_url = self.data[index]
            self.data[index] = new_url
            log.info(
                "Replaced track at index %d in playlist %s: %s -> %s",
                index,
                self._file.name,
                old_url,
                new_url,
            )
        await self.save()
        return old_url

    def delete_file(self) -> bool:
        """
        Delete the playlist file from disk.

        :returns: True if file was deleted, False if it didn't exist
        """
        try:
            if self._file.is_file():
                self._file.unlink()
                self.data = []
                self._is_loaded = False
                log.info("Deleted playlist file: %s", self._file.name)
                return True
            return False
        except (OSError, PermissionError):
            log.exception("Failed to delete playlist file: %s", self._file)
            raise


class AutoPlaylistManager:
    """Manager class that facilitates multiple playlists."""

    def __init__(self, bot: "MusicBot") -> None:
        """
        Initialize the manager, checking the file system for usable playlists.
        """
        self._bot: "MusicBot" = bot
        self._apl_dir: pathlib.Path = bot.config.auto_playlist_dir
        self._apl_file_default = self._apl_dir.joinpath(APL_FILE_DEFAULT)
        self._apl_file_history = self._apl_dir.joinpath(APL_FILE_HISTORY)
        self._apl_file_usercopy = self._apl_dir.joinpath(APL_FILE_APLCOPY)

        self._playlists: Dict[str, AutoPlaylist] = {}

        self.setup_autoplaylist()

    def setup_autoplaylist(self) -> None:
        """
        Ensure directories for auto playlists are available and that historic
        playlist files are copied.
        """
        if not self._apl_dir.is_dir():
            self._apl_dir.mkdir(parents=True, exist_ok=True)

        # Files from previous versions of MusicBot
        old_usercopy = pathlib.Path(OLD_DEFAULT_AUTOPLAYLIST_FILE)
        old_bundle = pathlib.Path(OLD_BUNDLED_AUTOPLAYLIST_FILE)

        # Copy or rename the old auto-playlist files if new files don't exist yet.
        if old_usercopy.is_file() and not self._apl_file_usercopy.is_file():
            # rename the old autoplaylist.txt into the new playlist directory.
            old_usercopy.rename(self._apl_file_usercopy)
        if old_bundle.is_file() and not self._apl_file_default.is_file():
            # copy the bundled playlist into the default, shared playlist.
            shutil.copy(old_bundle, self._apl_file_default)

        if (
            not self._apl_file_history.is_file()
            and self._bot.config.enable_queue_history_global
        ):
            self._apl_file_history.touch(exist_ok=True)

        self.discover_playlists()

    @property
    def _default_pl(self) -> AutoPlaylist:
        """Returns the default playlist, even if the file is deleted."""
        if self._apl_file_default.stem in self._playlists:
            return self._playlists[self._apl_file_default.stem]

        self._playlists[self._apl_file_default.stem] = AutoPlaylist(
            filename=self._apl_file_default,
            bot=self._bot,
        )
        return self._playlists[self._apl_file_default.stem]

    @property
    def _usercopy_pl(self) -> Optional[AutoPlaylist]:
        """Returns the copied autoplaylist.txt playlist if it exists."""
        # return mapped copy if possible.
        if self._apl_file_usercopy.stem in self._playlists:
            return self._playlists[self._apl_file_usercopy.stem]

        # if no mapped copy, check if file exists and map it.
        if self._apl_file_usercopy.is_file():
            self._playlists[self._apl_file_usercopy.stem] = AutoPlaylist(
                filename=self._apl_file_usercopy,
                bot=self._bot,
            )

        return self._playlists.get(self._apl_file_usercopy.stem, None)

    @property
    def global_history(self) -> AutoPlaylist:
        """Returns the MusicBot global history file."""
        if self._apl_file_history.stem in self._playlists:
            return self._playlists[self._apl_file_history.stem]

        self._playlists[self._apl_file_history.stem] = AutoPlaylist(
            filename=self._apl_file_history,
            bot=self._bot,
        )
        return self._playlists[self._apl_file_history.stem]

    @property
    def playlist_names(self) -> List[str]:
        """Returns all discovered playlist names."""
        return list(self._playlists.keys())

    @property
    def loaded_playlists(self) -> List[AutoPlaylist]:
        """Returns all loaded AutoPlaylist objects."""
        return [pl for pl in self._playlists.values() if pl.loaded]

    @property
    def loaded_tracks(self) -> List[str]:
        """
        Contains a list of all unique playlist entries, from each loaded playlist.
        """
        tracks: Set[str] = set()
        for pl in self._playlists.values():
            if pl.loaded:
                tracks = tracks.union(set(pl))
        return list(tracks)

    def discover_playlists(self) -> None:
        """
        Look for available playlist files but do not load them into memory yet.
        This method makes playlists available for display or selection.
        """
        for pfile in self._apl_dir.iterdir():
            # only process .txt files
            if pfile.suffix.lower() == ".txt":
                # ignore already discovered playlists.
                if pfile.stem in self._playlists:
                    continue

                pl = AutoPlaylist(pfile, self._bot)
                self._playlists[pfile.stem] = pl

    def get_default(self) -> AutoPlaylist:
        """
        Gets the appropriate default playlist based on which files exist.
        """
        # If the old autoplaylist.txt was copied, use it.
        if self._usercopy_pl is not None:
            return self._usercopy_pl
        return self._default_pl

    def get_playlist(self, filename: str) -> AutoPlaylist:
        """Get or create a playlist with the given filename."""
        # using pathlib .name here prevents directory traversal attack.
        pl_file = self._apl_dir.joinpath(pathlib.Path(filename).name)

        # Return the existing instance if we have one.
        if pl_file.stem in self._playlists:
            return self._playlists[pl_file.stem]

        # otherwise, make a new instance with this filename
        self._playlists[pl_file.stem] = AutoPlaylist(pl_file, self._bot)
        return self._playlists[pl_file.stem]

    def playlist_exists(self, filename: str) -> bool:
        """Check for the existence of the given playlist file."""
        # using pathlib .name prevents directory traversal attack.
        return self._apl_dir.joinpath(pathlib.Path(filename).name).is_file()

    def create_playlist(self, name: str) -> AutoPlaylist:
        """
        Create a new empty playlist file.

        :param name: Name for the playlist (without .txt extension)
        :returns: The created AutoPlaylist instance
        :raises ValueError: If playlist already exists or name is invalid
        """
        # Sanitize name - remove path components and extension
        safe_name = pathlib.Path(name).stem
        if not safe_name:
            raise ValueError("Playlist name cannot be empty")

        # Check for invalid characters
        invalid_chars = '<>:"/\\|?*'
        if any(c in safe_name for c in invalid_chars):
            raise ValueError(f"Playlist name contains invalid characters: {invalid_chars}")

        filename = f"{safe_name}.txt"
        pl_file = self._apl_dir.joinpath(filename)

        if pl_file.is_file():
            raise ValueError(f"Playlist '{safe_name}' already exists")

        # Create the file
        pl_file.touch(exist_ok=False)
        log.info("Created new playlist: %s", filename)

        # Create and register the AutoPlaylist instance
        playlist = AutoPlaylist(pl_file, self._bot)
        playlist._is_loaded = True  # Mark as loaded since it's empty
        self._playlists[safe_name] = playlist

        return playlist

    def delete_playlist(self, name: str) -> bool:
        """
        Delete a playlist file and remove it from the manager.

        :param name: Name of the playlist to delete
        :returns: True if deleted successfully
        :raises ValueError: If playlist doesn't exist
        """
        safe_name = pathlib.Path(name).stem
        pl_file = self._apl_dir.joinpath(f"{safe_name}.txt")

        if not pl_file.is_file():
            raise ValueError(f"Playlist '{safe_name}' does not exist")

        # Get the playlist instance if it exists
        if safe_name in self._playlists:
            playlist = self._playlists[safe_name]
            playlist.delete_file()
            del self._playlists[safe_name]
        else:
            # File exists but not in our registry - just delete it
            pl_file.unlink()

        log.info("Deleted playlist: %s", safe_name)
        return True

    def rename_playlist(self, old_name: str, new_name: str) -> AutoPlaylist:
        """
        Rename a playlist file.

        :param old_name: Current name of the playlist
        :param new_name: New name for the playlist
        :returns: The renamed AutoPlaylist instance
        :raises ValueError: If old playlist doesn't exist or new name is invalid/taken
        """
        old_safe = pathlib.Path(old_name).stem
        new_safe = pathlib.Path(new_name).stem

        if not new_safe:
            raise ValueError("New playlist name cannot be empty")

        # Check for invalid characters
        invalid_chars = '<>:"/\\|?*'
        if any(c in new_safe for c in invalid_chars):
            raise ValueError(f"Playlist name contains invalid characters: {invalid_chars}")

        old_file = self._apl_dir.joinpath(f"{old_safe}.txt")
        new_file = self._apl_dir.joinpath(f"{new_safe}.txt")

        if not old_file.is_file():
            raise ValueError(f"Playlist '{old_safe}' does not exist")

        if new_file.is_file():
            raise ValueError(f"Playlist '{new_safe}' already exists")

        # Rename the file
        old_file.rename(new_file)
        log.info("Renamed playlist: %s -> %s", old_safe, new_safe)

        # Update registry
        if old_safe in self._playlists:
            playlist = self._playlists.pop(old_safe)
            playlist._file = new_file
            playlist._removed_file = new_file.with_name(f"{new_safe}.removed.log")
            self._playlists[new_safe] = playlist
        else:
            # Create new instance for renamed file
            playlist = AutoPlaylist(new_file, self._bot)
            self._playlists[new_safe] = playlist

        return playlist
