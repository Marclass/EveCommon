import sqlite3


class SDEConnector(object):
    def __init__(self, db_name='', host='127.0.0.1', port=3306, user='root', passwd=''):
        self.db_name = db_name
        self.host = host
        self.port = port

        self.user = user
        self.passwd = passwd

        self.connection = sqlite3.connect(db_name)
        self.connection.row_factory = sqlite3.Row
        self.connection.text_factory = str
        self.cursor = self.connection.cursor()

    def __del__(self):
        self.cursor.close()
        self.connection.close()

    def get_type_id_by_type_name(self, type_name):
        self.cursor.execute("SELECT typeID FROM invtypes WHERE typeName = %s; " % type_name)
        type_id = 0
        for row in self.cursor:
            type_id = row[0]
        return type_id

    def get_type_name_by_type_id(self, type_id):
        self.cursor.execute("SELECT typeName FROM invtypes WHERE typeID = %s; " % type_id)
        type_name = ''
        for row in self.cursor:
            type_name = row[0]
        return type_name

    def type_id_has_group_id(self, type_id):
        self.cursor.execute("SELECT marketGroupID FROM invtypes WHERE typeID = %s; " % type_id)
        return self.cursor.fetchone() is not None

    def type_id_is_in_group_id(self, type_id, group_id):
        self.cursor.execute("SELECT marketGroupID FROM invtypes WHERE typeID = %s; " % type_id)
        return self.cursor.fetchone() == group_id

    def get_types_with_market_group(self):
        self.cursor.execute("SELECT * FROM invtypes WHERE marketGroupId <> ''")
        types = []
        for row in self.cursor:
            types.append(row)
        return types


    def execute_raw(self, sql):
        return self.cursor.execute(sql)

