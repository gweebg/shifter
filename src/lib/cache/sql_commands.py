SQL_TABLE_CREATE = 'CREATE TABLE IF NOT EXISTS `cache` (`key` TEXT UNIQUE, `value` BLOB, `last_seen` INTEGER, PRIMARY KEY(`key`)) WITHOUT ROWID;'
SQL_INDEX_CREATE = 'CREATE INDEX IF NOT EXISTS `last_seen_idx` ON `cache` (`last_seen`);'
SQL_ADD_UPDATE_KEY = 'INSERT OR REPLACE INTO `cache` (`key`, `value`, `last_seen`) VALUES (?, ?, ?);'
SQL_GET_KEY_SINCE = 'SELECT `value` FROM `cache` WHERE `key` = ? AND `last_seen` >= ?;'
SQL_UPDATE_KEY_LAST_SEEN = 'UPDATE `cache` SET `last_seen` = ? WHERE `key` = ?;'
SQL_DELETE_KEY = 'DELETE FROM `cache` WHERE `key` = ?;'
SQL_CLEAR = 'DELETE * FROM `cache`;'
