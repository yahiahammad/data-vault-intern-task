-- M2: DuckLake's own bookkeeping (table schemas, snapshots, current file lists)
-- lives here as ordinary rows -- that's what gives DuckLake atomic commits for
-- free instead of reinventing transactions on top of files in MinIO.
CREATE DATABASE ducklake_catalog;
