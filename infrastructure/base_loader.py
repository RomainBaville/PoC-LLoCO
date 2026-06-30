# SPDX-License-Identifier: Apache-2.0
# SPDX-FileCopyrightText: Copyright 2025-2026 AKKODIS.
# SPDX-FileContributor: Romain Baville

from abc import ABC, abstractmethod


class DataLoader( ABC ):

    @abstractmethod
    def load( self, source ) -> tuple[ list[ str ], list[ dict[ str, str ] ] ]:
        ...
