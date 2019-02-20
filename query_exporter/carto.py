"""Carto wrapper."""
from collections import namedtuple
from typing import Union

from longitude.core.data_sources.carto import CartoDataSource
from longitude.core.common.exceptions import LongitudeConfigError

from db import Query


class DataBase(namedtuple('DataBase', ['name', 'carto'])):
    """A database to perform Queries."""
    data_source: Union[CartoDataSource, None] = None

    async def connect(self):
        """Connect to the database."""
        try:
            self.data_source = CartoDataSource(config=self.carto)
        except Exception as e:
            raise LongitudeConfigError(f'Carto data source cannot be created with the provided config: {e}')

    async def close(self):
        pass

    async def execute(self, query: Query):
        """Execute a query."""
        if self.data_source.is_ready:
            return query.results(self.data_source.query(query_template=query.sql))
        else:
            raise LongitudeConfigError('Carto data source cannot initialize with the provided config.')
