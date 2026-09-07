# SPDX-License-Identifier: Apache-2.0
# SPDX-FileCopyrightText: Copyright 2025-2026 AKKODIS.
# SPDX-FileContributor: Romain Baville

import types
from dataclasses import dataclass, field, fields, is_dataclass
from typing import get_args, get_origin, get_type_hints

from typing_extensions import Self

from domain.assignment.base import AssignmentProblem


def type_name( tp: type ) -> str:
    """Format the type of an object to be user readable.

    Args:
        tp (type): The type of the object.

    Returns:
        str: The type of the object redable.
    """
    origin = get_origin( tp )

    if origin is None:
        return getattr( tp, "__name__", str( tp ) )

    type_str = str( tp ).replace( "typing.", "" )
    if "domain" in type_str:
        type_str = type_str.split( "." )[ -1 ]

    return type_str


@dataclass
class DomainType:
    """Describe an available optimization domain."""

    key: str = field( metadata={
        "description": "Unique domain identifier."
    } )

    label: str = field( metadata={
        "description": "Human-readable domain name."
    } )

    description: str = field( metadata={
        "description": "Short domain description."
    } )

    root_object: type = field( metadata={
        "description": "Root class of the domain model."
    } )

    def __str__( self: Self ) -> str:
        """Print the Domain label.

        Returns:
            str: The Domain label.
        """
        return self.label

    def get_schema( self: Self ) -> str:
        """Get all the atributes andel by the domain.

        Retunrs:
            str: All the attributes andel by the domain.
        """
        lines: list[ str ] = []
        visited: set[ type ] = set()

        def visit( cls: type, level: int = 0 ) -> None:
            """Visit the attribute if it is a dataclass."""
            if cls in visited:
                return

            visited.add( cls )
            hints = get_type_hints( cls )
            indent = "  " * level

            lines.append( f"{ indent }{ cls.__name__ }" )
            for field_ in fields( cls ):
                field_type = hints[ field_.name ]
                description = field_.metadata[ "description" ]

                lines.append( f"{ indent }- { field_.name }: { type_name( field_type ) }" )
                lines.append( f"{ indent }  { description }" )

                # Direct dataclass
                if isinstance( field_type, type ) and is_dataclass( field_type ):
                    visit( field_type, level + 1 )
                    continue

                origin = get_origin( field_type )
                if origin in ( types.UnionType, ):
                    for arg in get_args( field_type ):
                        if arg is type( None ):
                            continue

                        if ( isinstance( arg, type ) and is_dataclass( arg ) ):
                            visit( arg, level + 1 )

        visit( self.root_object )

        return "\n".join( lines )


DOMAIN_REGISTRY: list[ DomainType ] = [
    DomainType(
        key="assignment",
        label="Assignment Problem",
        description="Assign left entities to right entities.",
        root_object=AssignmentProblem
    )
]
