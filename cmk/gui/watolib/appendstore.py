#!/usr/bin/env python3
# Copyright (C) 2019 tribe29 GmbH - License: GNU General Public License v2
# This file is part of Checkmk (https://checkmk.com). It is subject to the terms and
# conditions defined in the file COPYING, which is part of this source code package.

import abc
import ast
import os
from collections.abc import Callable, Iterable, Sequence
from pathlib import Path
from typing import Generic, TypeVar

import cmk.utils.store as store
from cmk.utils.exceptions import MKGeneralException

from cmk.gui.i18n import _

_VT = TypeVar("_VT")


class ABCAppendStore(Generic[_VT], abc.ABC):
    """Managing a file with structured data that can be appended in a cheap way

    The file holds basic python structures separated by "\0".
    """

    @staticmethod
    @abc.abstractmethod
    def _serialize(entry: _VT) -> object:
        """Prepare _VT objects for serialization

        Note:
            Abstract static methods do not make any sense.  This should
            either be a free function or on `entry : _VT`.

        Override this to execute some logic before repr()"""
        raise NotImplementedError()

    @staticmethod
    @abc.abstractmethod
    def _deserialize(raw: object) -> _VT:
        """Create _VT objects from serialized data

        Note:
            Abstract static methods do not make any sense.  This should
            either be a free function or on `entry : _VT`.

        Override this to execute some logic after literal_eval() to produce _VT objects"""
        raise NotImplementedError()

    def __init__(self, path: Path) -> None:
        self._path = path

    def exists(self) -> bool:
        return self._path.exists()

    # TODO: Implement this locking as context manager
    def __read(self, *, lock: bool) -> Sequence[_VT]:
        """Parse the file and return the entries"""
        path = self._path

        if lock:
            store.acquire_lock(path)

        entries = []
        try:
            with path.open("rb") as f:
                for entry in f.read().split(b"\0"):
                    if entry:
                        entries.append(self._deserialize(ast.literal_eval(entry.decode("utf-8"))))
        except FileNotFoundError:
            pass
        except Exception:
            if lock:
                store.release_lock(path)
            raise

        return entries

    def read(self) -> Sequence[_VT]:
        return self.__read(lock=False)

    def write(self, entries: Iterable[_VT]) -> None:
        # First truncate the file
        with self._path.open("wb"):
            pass

        for entry in entries:
            self.append(entry)

    def append(self, entry: _VT) -> None:
        path = self._path
        with store.locked(path):
            try:
                with path.open("ab+") as f:
                    f.write(repr(self._serialize(entry)).encode("utf-8") + b"\0")
                    f.flush()
                    os.fsync(f.fileno())
                path.chmod(0o660)
            except Exception as e:
                raise MKGeneralException(_('Cannot write file "%s": %s') % (path, e))

    def transform(self, transformer: Callable[[Sequence[_VT]], Sequence[_VT]]) -> None:
        entries = self.__read(lock=True)
        try:
            entries = transformer(entries)
        finally:
            self.write(entries)
