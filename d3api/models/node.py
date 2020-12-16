from sqlalchemy import Column, TIMESTAMP, Index, text
from sqlalchemy.dialects.postgresql import JSONB, VARCHAR
from sqlalchemy.ext.mutable import MutableDict
from sqlalchemy.sql import func

from d3api.extensions import db


class Node(db.Model):
    __tablename__ = 'nodes'
    id = Column(VARCHAR, index=True, primary_key=True)
    context = Column(VARCHAR, index=True, primary_key=True)
    aspect = Column(VARCHAR, index=True, nullable=False)
    created = Column(TIMESTAMP(timezone=True), index=True, nullable=False, default=func.now())
    modified = Column(TIMESTAMP(timezone=True), index=True)
    validNotBefore = Column(TIMESTAMP(timezone=True), index=True,
                            nullable=False, default=func.now())
    validNotAfter = Column(TIMESTAMP(timezone=True), index=True)
    json = Column(MutableDict.as_mutable(JSONB))
    expanded = Column(MutableDict.as_mutable(JSONB))
    __table_args__ = (Index('ix_nodes_json',
                            text("json"),
                            postgresql_using="gin"),)

# CREATE INVERTED INDEX ON nodes (json)
# CREATE INDEX ON nodes USING GIN (json)
# CREATE INDEX ix_btree_json_long_desc1 ON nodes USING BTREE ((json->>‘long_desc’))
# CREATE INDEX ix_btree_json_long_desc2 ON nodes USING HASH ((json->>‘long_desc’))
# CREATE INDEX ix_nodes_json_long_desc3 ON nodes USING gin ((json->>'long_desc'));
