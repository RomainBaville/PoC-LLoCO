# SPDX-License-Identifier: Apache-2.0
# SPDX-FileCopyrightText: Copyright 2025-2026 AKKODIS.
# SPDX-FileContributor: Romain Baville

from abc import ABC, abstractmethod
from typing import List, Dict, Tuple


class DataLoader(ABC):
    @abstractmethod
    def load(self, path: str) -> Tuple[List[str], List[Dict[str, str]]]:
        ...
