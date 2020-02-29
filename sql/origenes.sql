SELECT
	'file_store'.'files'.'id' AS 'idfile',
    'file_store'.'uris'.'id' AS 'iduri',
    'file_store'.'files'.'sha256sum' AS 'storename',
    'file_store'.'uris'.'path' AS 'originpath',
    'file_store'.'uris'.'filename' AS 'originname',
    'file_store'.'properties'.'userid' AS 'userid',
    'file_store'.'properties'.'uname' AS 'uname',
    'file_store'.'properties'.'gid' AS 'gid',
    'file_store'.'properties'.'gname' AS 'gname',
    'file_store'.'properties'.'size' AS 'size',
    'file_store'.'properties'.'rights' AS 'rights',
	'file_store'.'properties'
.'timeaccess' AS 'timeaccess',
    'file_store'.'properties'.'timemod' AS 'timemod',
    'file_store'.'properties'.'timechang' AS 'timechang',
    'file_store'.'properties'.'timecreat' AS 'timecreat',
    'file_store'.'properties'.'mime' AS 'mime'
FROM
(
        (
            'file_store'.'files'
        JOIN 'file_store'.'uris' ON
(
                'file_store'.'uris'.'file_id' = 'file_store'.'files'.'id'
            )
        )
    JOIN 'file_store'.'properties' ON
(
            'file_store'.'properties'.'uri_id' = 'file_store'.'uris'.'id'
        )
    )
ORDER BY
    'file_store'.'files'.'sha256sum';