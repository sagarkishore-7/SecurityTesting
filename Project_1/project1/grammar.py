# Implement your grammar here in the `grammar` variable.
# You may define additional functions, e.g. for generators.
# You may not import any other modules written by yourself.
# That is, your entire implementation must be in `grammar.py`
# and `fuzzer.py`.
from fuzzingbook.GeneratorGrammarFuzzer import opts
from fuzzingbook.Grammars import trim_grammar, is_valid_grammar
import random

# Global data structures for database state
db_tables = {}
db_indexes = {}
db_views = []


class DBManager:
    def __init__(self):
        self.active_table = ""
        self.active_column = ""
        self.primary_key_col = ""
        self.table_for_select = ""
        self.old_name_for_alter = ""
        self.new_name_for_alter = ""
        self.old_column_alter = ""
        self.new_column_alter = ""
        self.current_index = ""
        self.column_list = []

    def save_table(self, name):  # store_table_name
        self.active_table = name

        if name not in db_tables:
            # Initialize new table state
            db_tables[name] = {'pk': True, 'columns': ['default_col']}
            return name
        return None

    def save_column(self, name):  # store_column_name
        self.active_column = name
        if self.active_table and name not in db_tables[self.active_table]["columns"]:
            db_tables[self.active_table]["columns"].append(name)
            return name
        return None

    def fetch_indexed_column(self, col_name):  # get_indexed_column_name
        if col_name not in db_tables[self.active_table]["columns"]:
            return random.choice(db_tables[self.active_table]["columns"])
        print("Error: Column for indexing not found")
        return None

    def find_foreign_table(self, table_name):  # get_foreign_table_name
        all_tables = list(db_tables.keys())
        if len(all_tables) > 2:
            all_tables.remove(self.active_table)
            if table_name not in all_tables:
                self.foreign_table = random.choice(all_tables)
                return self.foreign_table
        print("Error: Unable to find foreign table")
        return None

    def fetch_foreign_column(self, col_name):  # get_foreign_column_name
        if col_name not in db_tables[self.foreign_table]["columns"]:
            return random.choice(db_tables[self.foreign_table]["columns"])
        print("Error: Foreign column not found")
        return None

    def select_random_column(self, col_name):  # get_random_own_columnn_name
        if col_name not in db_tables[self.active_table]["columns"]:
            return random.choice(db_tables[self.active_table]["columns"])
        print("Error: Column not found in current table")
        return None

    def remove_table(self, table_name):  # get_drop_table_name
        if table_name in db_tables:
            del db_tables[table_name]
            return table_name
        print("Error: Table not found for removal")
        return None

    def display_state(self):  # print_state
        print(f"Current Table State: {db_tables}")
        print(f"Index Status: {db_indexes}")

    def choose_table_for_selection(self, table_name):  # get_selected_table_name
        if table_name not in db_tables:
            self.table_for_select = random.choice(list(db_tables.keys()))
            self.active_table = self.table_for_select
            return self.active_table
        return None

    def select_index_column(self, index_name):  # get_selected_index_name
        if self.active_table and index_name not in db_tables[self.active_table]["columns"]:
            return random.choice(db_tables[self.active_table]["columns"])
        print("Error: Index column for selection not found")
        return None

    def prepare_table_for_alter(self, table_name):  # get_alter_old_table_name
        if table_name in db_tables:
            self.old_name_for_alter = table_name
            self.active_table = self.old_name_for_alter
            return self.active_table
        self.old_name_for_alter = random.choice(list(db_tables.keys()))
        self.active_table = self.old_name_for_alter
        return self.active_table

    def rename_table(self, new_name):  # set_alter_new_table_name
        if new_name not in db_tables and self.old_name_for_alter:
            self.new_name_for_alter = new_name
            db_tables[self.new_name_for_alter] = db_tables.pop(self.old_name_for_alter)
            self.active_table = self.new_name_for_alter
            return self.new_name_for_alter
        print("Error: Table renaming failed")
        return None

    def prepare_column_for_alter(self, column_name):  # get_alter_old_column_name
        global columns_in_table
        if self.active_table:
            columns_in_table = db_tables[self.active_table]["columns"]

        if columns_in_table:
            if column_name in columns_in_table:
                self.old_column_alter = column_name
            else:
                self.old_column_alter = random.choice(columns_in_table)

            return self.old_column_alter
        else:
            print("Error: Invalid table or column for alteration")
            return None

    def rename_column(self, old_name, new_name):  # set_alter_new_column_name
        if old_name in db_tables[self.active_table]["columns"]:
            db_tables[self.active_table]["columns"].remove(old_name)
            db_tables[self.active_table]["columns"].append(new_name)
            return new_name
        print("Error: Column renaming failed")
        return None

    def add_column(self, col_name):  # alter_add_column
        if col_name not in db_tables[self.active_table]["columns"]:
            db_tables[self.active_table]["columns"].append(col_name)
            return col_name
        print("Error: Column already exists")
        return None

    def remove_column(self, col_name):  # alter_drop_column
        if col_name in db_tables[self.active_table]["columns"]:
            db_tables[self.active_table]["columns"].remove(col_name)
            return col_name
        print("Error: Column not found for removal")
        return None

    def select_index_table(self, table_name):  # get_index_table_name
        if table_name in db_tables:
            self.active_table = table_name
            return table_name
        self.active_table = random.choice(list(db_tables.keys()))
        return self.active_table

    def register_index(self, index_name):  # store_index_name
        if index_name not in db_indexes:
            db_indexes[index_name] = {"table": self.active_table, "index_columns": []}
            return index_name
        print("Error: Index already exists")
        return None

    def add_index_column(self, col_name):  # store_index_column_name
        if col_name not in db_indexes[self.current_index]["index_columns"]:
            db_indexes[self.current_index]["index_columns"].append(col_name)
            return col_name
        print("Error: Column already indexed")
        return None

    def remove_index(self, index_name):  # get_drop_index_name
        if index_name in db_indexes:
            del db_indexes[index_name]
            return index_name
        print("Error: Index not found")
        return None

    def save_view(self, view_name):  # store_view_name
        if view_name not in db_views:
            db_views.append(view_name)
            return view_name
        print("Error: View already exists")
        return None

    def delete_view(self, view_name):  # drop_view_name
        if view_name in db_views:
            db_views.remove(view_name)
            return view_name
        print("Error: View not found")
        return None


db_instance = DBManager()

sql_grammar = {

    "<global_regex_match>": ["GLOB", "REGEXP", "MATCH"],

    # HANDLERS GRAMMAR
    "<null_handling>": ["ISNULL", "NOTNULL", "NOT NULL"],
    "<raise_handling>": ["IGNORE", "ROLLBACK, <error_message>", "ABORT, <error_message>", "FAIL, <error_message>"],
    "<foreign_key_handling>": ["", "ON DELETE SET NULL", "ON DELETE SET DEFAULT", "ON DELETE CASCADE",
                               "ON DELETE RESTICT",
                               "ON DELETE NO ACTION", "ON UPDATE SET NULL", "ON UPDATE SET DEFAULT",
                               "ON UPDATE CASCADE",
                               "ON UPDATE RESTICT",
                               "ON UPDATE NO ACTION", "DEFERRABLE", "DEFERRABLE INITIALLY DEFERRED",
                               "DEFERRABLE INITIALLY IMMEDIATE",
                               "NOT DEFERRABLE", "NOT DEFERRABLE INITIALLY DEFERRED",
                               "NOT DEFERRABLE INITALLY DEFERRED",
                               "NOT DEFERRABLE INITIALLY IMMEDIATE", ],

    "<deferrable_handling>": ["", "INITIALLY DEFERRED", "INITIALLY IMMEDIATE"],
    "<handling_1>": ["<table_name>", "<table_function_name> ()", "<table_function_name> (<multiple_expression>)"],
    "<update_handling>": ["", "OR ABORT", "OR FAIL", "OR IGNORE", "OR REPLACE", "OR ROLLBACK"],
    "<conflict_handling>": ["ROLLBACK", "ABORT", "FAIL", "IGNORE", "REPLACE"],

    # EXPRESSION GRAMMAR
    "<NOT>": ["", "NOT"],
    "<digit>": ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"],
    "<letter>": ["a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m",
                 "n", "o", "p", "q", "r", "s", "t", "u", "v", "w", "x", "y", "z",
                 "A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M",
                 "N", "O", "P", "Q", "R", "S", "T", "U", "V", "W", "X", "Y", "Z"],
    "<unary_operator>": ["+", "-", "NOT", ],
    "<binary_operator>": ["+", "-", "*", "/", "%",
                          "=", "<", ">", "!=", ">=", "<=",
                          "AND", "OR",
                          "||",
                          "&", "|", "<<", ">>", ],
    "<compound_operator>": ["UNION", "UNION ALL", "INTERSECT", "EXCEPT"],
    "<literal_value>": ["<numeric_literal>", "'<string_literal>'", "NULL", "TRUE", "FALSE", "CURRENT_TIME",
                        "CURRENT_DATE", "CURRENT_TIMESTAMP"],
    "<expression>": ["<literal_value>",
                     "<table_name_dot><column_name>",
                     "<unary_operator> <expression>",
                     "<expression> <binary_operator> <expression>",
                     "<function_name> ( <function_arguments> ) <filter_clause> ",
                     "( <multiple_expression> )",
                     "CAST ( <expression> AS <type_name> )",
                     "<expression> COLLATE <collation_name>",
                     "<expression> <NOT> LIKE <expression> <escape_expression>",
                     "<expression> <NOT> <global_regex_match> <expression>",
                     "<expression> <null_handling>",
                     "<expression> IS <NOT> <DISTINCT_FROM> <expression>",
                     "<expression> <NOT> BETWEEN <expression> AND <expression>",
                     "<expression> <NOT> IN <handling_1>",
                     "CASE <expression> <multiple_when_then> <if_else_expression> END",
                     "<raise_function>"],
    "<data_type>": ["TEXT", "INTEGER", "REAL", "BLOB", "NULL"],

    "<natural_join>": ["NATURAL JOIN", "NATURAL LEFT JOIN", "NATURAL RIGHT JOIN",
                       "NATURAL FULL JOIN", "NATURAL INNER JOIN", "NATURAL LEFT OUTER JOIN",
                       "NATURAL RIGHT OUTER JOIN", "NATURAL FULL INNER JOIN"],
    "<nulls_first_last>": ["", "NULLS FIRST", "NULLS LAST"],
    "<asc_desc>": ["", "ASC", "DESC"],

    "<schema_name>": ["<string>"],
    "<function_arguments>": ["", "<DISTINCT> <multiple_expression> <order_by_clause>", "*"],
    "<multiple_ordering_term>": ["<ordering_term>", "<ordering_term>, <multiple_ordering_term>"],
    "ordering_term": ["<expression> <collate> <asc_desc> <nulls_first_last>"],
    "<filter_clause>": ["", "FILTER ( WHERE <expression> )"],
    "<type_name>": ["<multiple_name> <if_signed_number>"],
    "<multiple_name>": ["<name>", "<name> <multiple_name>"],
    "<if_signed_number>": ["", "( <signed_number> )", "( <signed_number>, <signed_number>)"],
    "<escape_expression>": ["", "ESCAPE <expression>"],
    "<multiple_when_then>": ["WHEN <expression> THEN <expression>"],
    "<if_else_expression>": ["", "ELSE <expression>"],
    "<raise_function>": ["RAISE (<raise_handling>)"],
    "<DISTINCT_FROM>": ["", "DISTINCT FROM"],
    "<DISTINCT>": ["", "DISTINCT"],
    "<EXISTS>": ["", "<EXISTS>"],
    "<function_name>": ["<string>"],
    "<table_function_name>": ["<string>"],
    "<name>": ["<string>"],
    "<table_name_dot>": ["", "<string>."],
    "<table_name>": ["<string>"],
    "<error_message>": ["<string>"],
    "<simple_function_invocation>": ["SELECT <simple_func>()",
                                     "SELECT <simple_func>(*)",
                                     ("SELECT <simple_func>(<multiple_expression>)",
                                      opts(order=[1, 2])
                                      )],
    "<multiple_expression>": ["<expression>", "<expression>, <multiple_expression>", ],
    "<simple_func>": ["abs", "changes", "char", "coalesce", "concat", "concat_ws", "format", "glob", "hex",
                      "ifnull", "iif", "instr", "last_insert_rowid", "length", "like", "like", "likelihood",
                      "likely", "load_extension", "load_extension", "lower", "ltrim", "ltrim", "max", "min",
                      "nullif", "octet_length", "printf", "quote", "random", "randomblob", "replace", "round",
                      "round", "rtrim", "rtrim", "sign", "soundex", "sqlite_compileoption_get",
                      "sqlite_compileoption_used", "sqlite_offset", "sqlite_source_id", "sqlite_version",
                      "substr", "substr", "substring", "substring", "total_changes", "trim", "trim", "typeof",
                      "unhex", "unhex", "unicode", "unlikely", "upper", "zeroblob"
                      ],
    "<date_time_functions>": [("SELECT date(<time_value>, <multiple_date_modifier>)",
                               opts(order=[1, 2])
                               ),
                              ("SELECT time(<time_value>, <multiple_date_modifier>)",
                               opts(order=[1, 2])
                               ),
                              ("SELECT datetime(<time_value>, <multiple_date_modifier>)",
                               opts(order=[1, 2])
                               ),
                              ("SELECT julianday(<time_value>, <multiple_date_modifier>)",
                               opts(order=[1, 2])
                               ),
                              ("SELECT unixepoch(<time_value>, <multiple_date_modifier>)",
                               opts(order=[1, 2])
                               ),
                              ("SELECT strftime(<multiple_date_format>, <time_value>, <multiple_date_modifier>)",
                               opts(order=[1, 2, 3])
                               ),
                              ("SELECT timediff(<c_time_value>, <c_time_value>)",
                               opts(order=[1, 2])
                               )],
    "<time_value>": ["", "<year>-<month>-<d_date>",
                     "<year>-<month>-<d_date> <hour>:<minutes>", "<year>-<month>-<d_date> <hour>:<minutes>:<seconds>",
                     "<year>-<month>-<d_date> <hour>:<minutes>:<seconds>.<seconds><digit>",
                     "<year>-<month>-<d_date>T<hour>:<minutes>", "<year>-<month>-<d_date>T<hour>:<minutes>:<seconds>",
                     "<year>-<month>-<d_date>T<hour>:<minutes>:<seconds>.<seconds><digit>",
                     "<hour>:<minutes>", "<hour>:<minutes>:<seconds>", "<hour>:<minutes>:<seconds>.<seconds>digit",
                     "now", "<d_date><d_date><d_date><d_date><d_date>"
                     ],
    "<multiple_date_modifier>": ["<date_modifier>", "<date_modifier>, <multiple_date_modifier>"],
    "<date_modifier>": ["+<digit><digit> days", "-<digit><digit> days",
                        "+<digit><digit> hours", "-<digit><digit> hours",
                        "+<digit><digit> minutes", "-<digit><digit> minutes",
                        "+<digit><digit> seconds", "-<digit><digit> seconds",
                        "+<digit><digit> months", "-<digit><digit> months",
                        "+<digit><digit> years", "-<digit><digit> years",
                        "+<hour>:<minutes>", "-<hour>:<minutes>",
                        "+<hour>:<minutes>:<seconds>", "-<hour>:<minutes>:<seconds>",
                        "+<hour>:<minutes>:<seconds>.<seconds><digit>", "-<hour>:<minutes>:<seconds>.<seconds><digit>",
                        "+<year>-<month>-<d_date>", "-<year>-<month>-<d_date>",
                        "+<year>-<month>-<d_date> <hour>:<minutes>", "-<year>-<month>-<d_date> <hour>:<minutes>",
                        "+<year>-<month>-<d_date> <hour>:<minutes>:<seconds>",
                        "-<year>-<month>-<d_date> <hour>:<minutes>:<seconds>",
                        "+<year>-<month>-<d_date> <hour>:<minutes>:<seconds>.<seconds><digit>",
                        "-<year>-<month>-<d_date> <hour>:<minutes>:<seconds>.<seconds><digit>",
                        "start of month", "start of year", "start of day", "weekday <digit>", "unixepoch", "julianday",
                        "auto", "localtime", "utc", "subsec", "subsecond",
                        ],
    "<multiple_date_format>": ["<date_format>", "<date_format> <multiple_date_format>"],
    "<date_format>": ["%/d", "%/e", "%/f", "%/F", "%H", "%I", "%j", "%J", "%k", "%l", "%m", "%M", "%p",
                      "%P", "%R", "%/s", "%S", "%T", "%T", "%/u", "%w", "%W", "%Y", "%/%/"],

    "<c_time_value>": ["<year>-<month>-<d_date>",
                       "<year>-<month>-<d_date> <hour>:<minutes>", "<year>-<month>-<d_date> <hour>:<minutes>:<seconds>",
                       "<year>-<month>-<d_date> <hour>:<minutes>:<seconds>.<seconds><digit>",
                       "<year>-<month>-<d_date>T<hour>:<minutes>", "<year>-<month>-<d_date>T<hour>:<minutes>:<seconds>",
                       "<year>-<month>-<d_date>T<hour>:<minutes>:<seconds>.<seconds><digit>",
                       "<hour>:<minutes>", "<hour>:<minutes>:<seconds>", "<hour>:<minutes>:<seconds>.<seconds>digit",
                       "now", "<d_date><d_date><d_date><d_date><d_date>",
                       ],
    "<year>": ["<digit><digit><digit><digit>"],
    "<month>": ["<digit><digit>"],
    "<d_date>": ["<digit><digit>"],
    "<hour>": ["<digit><digit>"],
    "<minutes>": ["<digit><digit>"],
    "<seconds>": ["<digit><digit>"],
    "<create_virtual_table_statement>": [("CREATE VIRTUAL TABLE <virtual_table_name> USING <virtual_module_name>",
                                          opts(order=[1, 2])
                                          ),
                                         (
                                             "CREATE VIRTUAL TABLE <virtual_table_name> USING <virtual_module_name> (<multiple_virtual_module_args>)",
                                             opts(order=[1, 2, 3])
                                         ),
                                         (
                                             "CREATE VIRTUAL TABLE IF NOT EXISTS <virtual_table_name> USING <virtual_module_name>",
                                             opts(order=[1, 2])
                                         ),
                                         (
                                             "CREATE VIRTUAL TABLE IF NOT EXISTS <virtual_table_name> USING <virtual_module_name> (<multiple_virtual_module_args>)",
                                             opts(order=[1, 2, 3])
                                         ),
                                         ],
    "<multiple_virtual_module_args>": ["<virtual_module_args>",
                                       ("<virtual_module_args>, <multiple_virtual_module_args>",
                                        opts(order=[1, 2]))],
    "<virtual_module_args>": [
        ("<virtual_column_name> <column_type> DEFAULT <default_literal_or_number> <virtual_column_constraint>",
         opts(order=[1, 2, 3, 4])
         )],
    "<virtual_column_constraint>": ["NOT NULL <conflict_clause>",
                                    "UNIQUE <conflict_clause>",
                                    "COLLATE <collation_name>", ],
    "<virtual_table_name>": ["<string>"],
    "<virtual_module_name>": ["<string>"],
    "<virtual_column_name>": ["<string>"],
    "<create_index_statement>": [("CREATE INDEX <index_name> ON <index_table_name> (<multiple_indexed_columns>)",
                                  opts(order=[2, 1, 3])
                                  ),
                                 (
                                     "CREATE INDEX <index_name> ON <index_table_name> (<multiple_indexed_columns>) WHERE <expression>",
                                     opts(order=[2, 1, 3, 4])
                                 ),
                                 (
                                     "CREATE INDEX IF NOT EXISTS <index_name> ON <index_table_name> (<multiple_indexed_columns>)",
                                     opts(order=[2, 1, 3])
                                 ),
                                 (
                                     "CREATE INDEX IF NOT EXISTS <index_name> ON <index_table_name> (<multiple_indexed_columns>) WHERE <expression>",
                                     opts(order=[2, 1, 3, 4])
                                 ),
                                 ("CREATE UNIQUE INDEX <index_name> ON <index_table_name> (<multiple_indexed_columns>)",
                                  opts(order=[2, 1, 3])
                                  ),
                                 (
                                     "CREATE UNQIE INDEX <index_name> ON <index_table_name> (<multiple_indexed_columns>) WHERE <expression>",
                                     opts(order=[2, 1, 3, 4])
                                 ),
                                 (
                                     "CREATE UNIQUE INDEX IF NOT EXISTS <index_name> ON <index_table_name> (<multiple_indexed_columns>)",
                                     opts(order=[2, 1, 3])
                                 ),
                                 (
                                     "CREATE UNIQUE INDEX IF NOT EXISTS <index_name> ON <index_table_name> (<multiple_indexed_columns>) WHERE <expression>",
                                     opts(order=[2, 1, 3, 4])
                                 ),
                                 ],
    "<multiple_indexed_columns>": ["<index_column_name>",
                                   ("<index_column_name>, <multiple_indexed_columns>", opts(order=[1, 2]))],
    "<index_table_name>": [("<string>",
                            opts(post=lambda index_table_name: db_instance.select_index_table(index_table_name))
                            )],
    "<index_column_name>": [("<string>",
                             opts(post=lambda index_column_name: db_instance.fetch_indexed_column(index_column_name))
                             )],
    "<multiple_result_column>": ["<result_column>",
                                 ("<result_column>, <multiple_result_column>",
                                  opts(order=[1, 2])
                                  )],
    "<alter_table_statement>": [("ALTER TABLE <alter_old_table_name> RENAME TO <alter_new_table_name>",
                                 opts(order=[1, 2])
                                 ),
                                (
                                    "ALTER TABLE <alter_old_table_name> RENAME COLUMN <alter_old_column_name> TO <alter_new_column_name>",
                                    opts(order=[1, 2, 3])
                                ),
                                ("ALTER TABLE <alter_old_table_name> ADD COLUMN <alter_column_definition>",
                                 opts(order=[1, 2])
                                 ),
                                ("ALTER TABLE <alter_old_table_name> DROP COLUMN <alter_drop_column_name>",
                                 opts(order=[1, 2])
                                 ),
                                ],
    "<alter_column_definition>": [
        ("<alter_column_name> <column_type> DEFAULT <default_literal_or_number> <column_constraint>",
         opts(order=[1, 2, 3, 4])
         )],
    "<column_constraint>": ["NOT NULL <conflict_clause>",
                            "UNIQUE <conflict_clause>",
                            "COLLATE <collation_name>",
                            ],
    "<alter_drop_column_name>": [("<string>",
                                  opts(post=lambda drop_column_name: db_instance.remove_column(drop_column_name))
                                  )],
    "<alter_new_table_name>": [("<string>",
                                opts(post=lambda alter_table_name: db_instance.rename_table(alter_table_name))
                                )],
    "<alter_old_table_name>": [("<string>",
                                opts(
                                    post=lambda alter_table_name: db_instance.prepare_table_for_alter(alter_table_name))
                                )],
    "<alter_old_column_name>": [("<string>",
                                 opts(post=lambda alter_column_name: db_instance.prepare_column_for_alter(
                                     alter_column_name))
                                 )],
    "<alter_new_column_name>": [("<string>",
                                 opts(post=lambda alter_column_name: db_instance.rename_column(alter_column_name))
                                 )],
    "<alter_column_name>": [("<string>",
                             opts(post=lambda alter_column_name: db_instance.add_column(alter_column_name))
                             )],
    "<delete_statement>": ["DELETE FROM <delete_qualified_table_name>",
                           "DELETE FROM <delete_qualified_table_name> WHERE <expression>"],
    "<delete_qualified_table_name>": ["<delete_table_name> <indexed>",
                                      "<delete_table_name> AS <alias>"],
    "<delete_table_name>": ["<string>"],
    "<alias>": ["<string>"],
    "<indexed>": ["", "INDEXED BY <index_name>", "NOT INDEXED"],
    "<index_name>": ["<string>"],
    "<drop_index_statement>": ["DROP INDEX <drop_index_name>",
                               "DROP INDEX IF EXISTS <drop_index_name>",
                               ],
    "<drop_index_name>": [("<string>",
                           opts(post=lambda drop_index_name: db_instance.remove_index(drop_index_name))
                           )],
    "<drop_table_statement>": ["DROP TABLE <drop_table_name>",
                               "DROP TABLE IF EXISTS <drop_table_name>",
                               ],
    "<drop_table_name>": [("<string>",
                           opts(post=lambda drop_table_name: db_instance.remove_table(drop_table_name))
                           )],
    "<drop_view_statement>": ["DROP TABLE <view_name>",
                              "DROP TABLE IF EXISTS <view_name>",
                              ],
    "<pragma_statement>": ["PRAGMA <pragma_name>",
                           "PRAGMA <pragma_name> = <pragma_value>",
                           "PRAGMA <pragma_name> (<pragma_value>)",
                           ],
    "<pragma_value>": ["<signed_number>"],
    "<pragma_name>": ["analysis_limit", "application_id", "auto_vacuum", "automatic_index", "busy_timeout",
                      "cache_size", "cache_spill", "cell_size_check", "checkpoint_fullfsync", "collation_list",
                      "compile_handling", "data_version", "database_list", "defer_foreign_keys", "encoding",
                      "foreign_key_check", "foreign_key_list", "foreign_keys", "freelist_count", "fullfsync",
                      "function_list", "hard_heap_limit", "ignore_check_constraints", "incremental_vacuum",
                      "index_info", "index_list", "index_xinfo", "integrity_check", "journal_mode",
                      "journal_size_limit", "legacy_alter_table", "legacy_file_format", "locking_mode",
                      "max_page_count", "mmap_size", "module_list", "optimize", "page_count", "page_size",
                      "pragma_list", "query_only", "quick_check", "read_uncommitted", "recursive_triggers",
                      "reverse_unordered_selects", "secure_delete", "shrink_memory", "soft_heap_limit", "synchronous",
                      "table_info", "table_list", "table_xinfo", "temp_store", "threads", "trusted_schema",
                      "user_version", "wal_autocheckpoint", "wal_checkpoint"],
    "<update_statement>": [
        "UPDATE <update_handling> <update_qualified_table_name> SET <update_column_name> = <expression>",
        "UPDATE <update_handling> <update_qualified_table_name> SET <update_column_name> = <expression> <from_clause>",
        "UPDATE <update_handling> <update_qualified_table_name> SET <update_column_name> = <expression> <where_clause>",
        "UPDATE <update_handling> <update_qualified_table_name> SET <update_column_name> = <expression> <from_clause> <where_clause>",
        "UPDATE <update_handling> <update_qualified_table_name> SET <update_column_list> = <expression>",
        "UPDATE <update_handling> <update_qualified_table_name> SET <update_column_list> = <expression> <from_clause>",
        "UPDATE <update_handling> <update_qualified_table_name> SET <update_column_list> = <expression> <where_clause>",
        "UPDATE <update_handling> <update_qualified_table_name> SET <update_column_list> = <expression> <from_clause> <where_clause>",
        ],
    "<update_qualified_table_name>": ["<update_table_name>",
                                      "<update_table_name> AS <update_alias>",
                                      "<update_table_name> INDEXED BY <update_index_name>",
                                      "<update_table_name> AS <update_alias> INDEXED BY <update_index_name>",
                                      "<update_table_name> NOT INDEXED",
                                      "<update_table_name> AS <update_alias> NOT INDEXED"],
    "<update_column_list>": ["(<multiple_update_column_name>)"],
    "<multiple_update_column_name>": ["<update_column_name>", "<update_column_name>, <multiple_update_column_name>"],
    "<update_table_or_subquery>": ["<update_table_name>",
                                   ("<update_table_name> <update_alias>",
                                    opts(order=[1, 2])
                                    ),
                                   ("<update_table_name> AS <update_alias>",
                                    opts(order=[1, 2])
                                    ),
                                   ("<update_table_name> INDEXED BY <update_index_name>",
                                    opts(order=[1, 2])
                                    ),
                                   ("<update_table_name> <update_alias> INDEXED BY <update_index_name>",
                                    opts(order=[1, 3, 2])
                                    ),
                                   ("<update_table_name> AS <update_alias> INDEXED BY <update_index_name>",
                                    opts(order=[1, 3, 2])
                                    ),
                                   "<update_table_name> NOT INDEXED",
                                   ("<update_table_name> <update_alias> NOT INDEXED",
                                    opts(order=[1, 2])
                                    ),
                                   ("<update_table_name> AS <update_alias> NOT INDEXED",
                                    opts(order=[1, 2])
                                    ),
                                   "(<update_table_or_subquery>)",
                                   "(<join_clause>)"],
    "<having_expression>": ["HAVING <expression>"],
    "<update_table_name>": [("<string>",
                             opts(post=lambda u_table_name: db_instance.choose_table_for_selection(u_table_name))
                             )],
    "<update_alias>": ["<string>"],
    "<update_index_name>": ["<string>"],
    "<update_column_name>": ["<string>"],
    "<create_view_statement>": [("CREATE VIEW <view_name> AS <select_statement>",
                                 opts(order=[1, 2])
                                 ),
                                ("CREATE VIEW IF NOT EXISTS <view_name> AS <select_statement>",
                                 opts(order=[1, 2])
                                 ),
                                ("CREATE VIEW <view_name> (<multiple_view_column>) AS <select_statement>",
                                 opts(order=[1, 2, 3])
                                 ),
                                ("CREATE VIEW IF NOT EXISTS <view_name> (<multiple_view_column>) AS <select_statement>",
                                 opts(order=[1, 2, 3])
                                 ),
                                ],
    "<view_name>": [("<string>",
                     opts(post=lambda view_name: db_instance.save_view(view_name))
                     )],
    "<multiple_view_column>": ["<view_column>", ("<view_column>, <multiple_view_column>", opts(order=[1, 2]))],
    "<view_column>": ["<string>"],
    "<create_table_statement>": [("CREATE TABLE <table_table_name> <column_def_table_constraint>",
                                  opts(order=[1, 2])
                                  ),
                                 ("CREATE TABLE IF NOT EXISTS <table_table_name> <column_def_table_constraint>",
                                  opts(order=[1, 2])
                                  ),
                                 #    "CREATE TEMP TABLE IF NOT EXISTS <table_name> <column_def_table_constraint>",
                                 #    "CREATE TEMPORARY TABLE IF NOT EXISTS <table_name> <column_def_table_constraint>",
                                 #    "CREATE TEMP TABLE <table_name> <column_def_table_constraint>",
                                 #    "CREATE TEMPORARY TABLE <table_name> <column_def_table_constraint>",
                                 ],
    "<column_def_table_constraint>": [
        ("(col1 INTEGER PRIMARY KEY AUTOINCREMENT, <multiple_column_definiton>, <table_constraint>)",
         opts(order=[1, 2])
         )],
    "<multiple_column_definiton>": ["<column_definiton>",
                                    ("<column_definiton>, <multiple_column_definiton>",
                                     opts(order=[1, 2])
                                     )],
    "<column_definiton>": [("<table_column_name> <column_type> DEFAULT <default_literal_or_number> <column_constraint>",
                            opts(order=[1, 2, 3, 4])
                            )],
    "<column_constraint_create_table>": ["NOT NULL <conflict_clause>",
                                         "UNIQUE <conflict_clause>",
                                         "COLLATE <collation_name_create_table>",
                                         ],
    "<default_literal_or_number>": ["<literal_value>", "<signed_number>", ],
    "<signed_number>": ["<numeric_literal>", "+<numeric_literal>", "-<numeric_literal>"],
    "<table_constraint>": [("UNIQUE (<indexed_column>) <conflict_clause>",
                            opts(order=[1, 2])
                            ),
                           "CHECK (<expression>)", ],
    "<conflict_clause>": ["", "ON CONFLICT <conflict_handling>"],
    "<multiple_column_name>": ["<column_name>, ", "<column_name><multiple_column_name>"],
    "<collation_name_create_table>": ["BINARY", "RTRIM", "NOCASE"],
    "<column_type>": ["", "TEXT", "NUM", "INTEGER", "REAL"],
    "<indexed_column>": [
        ("<string>", opts(post=lambda index_column_name: db_instance.fetch_indexed_column(index_column_name)))],
    "<table_table_name>": [("<string>",
                            opts(post=lambda table_name: db_instance.save_table(table_name))
                            )],
    "<table_column_name>": [("<string>",
                             opts(post=lambda column_name: db_instance.save_column(column_name))
                             )],
    "<column_name>": ["<string>"],
    "<string_literal>": ["<string>"],
    "<numeric_literal>": ["<digits>"],
    "<digits>": ["<digit>", "<digit><digits>"],
    "<select_statement>": [("<select_core> <order_or_limit>",
                            opts(order=[1, 2])
                            ),
                           ("<select_core> <compound_operator> <select_statement>",
                            opts(order=[1, 2, 3])
                            )],
    "<select_core>": [("SELECT <multipleresult_column> <from_clause> <where_clause> <group_by_clause>",
                       opts(order=[1, 2, 3, 4])
                       ),
                      ("SELECT DISTINCT <multipleresult_column> <from_clause> <where_clause> <group_by_clause>",
                       opts(order=[1, 2, 3, 4])
                       ),
                      ("SELECT ALL <multipleresult_column> <from_clause> <where_clause> <group_by_clause>",
                       opts(order=[1, 2, 3, 4])
                       ),
                      ("SELECT <aggregate_functions>(<select_index_name>) FROM <select_table_name>",
                       opts(order=[1, 2, 3])
                       ),
                      ("SELECT <aggregate_functions>(DISTINCT <select_index_name>) FROM <select_table_name>",
                       opts(order=[1, 2, 3])
                       ),
                      ],
    "<aggregate_functions>": ["sum", "avg", "count", "min", "max", "total", ],
    "<order_or_limit>": ["", "<order_by_clause>", "<order_by_clause> <limit_clause>", "<limit_clause>", ],
    "<multipleresult_column>": ["<result_column>",
                                ("<result_column>, <multipleresult_column>",
                                 opts(order=[1, 2])
                                 )],
    "<result_column>": [
        "*",
        "<select_table_name>.*"],
    "<from_clause>": ["", "FROM <select_table_or_subquery>", "FROM <join_clause>"],
    "<select_table_or_subquery>": ["<select_table_name>",
                                   ("<select_table_name> <table_alias>",
                                    opts(order=[1, 2])
                                    ),
                                   ("<select_table_name> AS <table_alias>",
                                    opts(order=[1, 2])
                                    ),
                                   ("<select_table_name> INDEXED BY <select_index_name>",
                                    opts(order=[1, 2])
                                    ),
                                   ("<select_table_name> <table_alias> INDEXED BY <select_index_name>",
                                    opts(order=[1, 3, 2])
                                    ),
                                   ("<select_table_name> AS <table_alias> INDEXED BY <select_index_name>",
                                    opts(order=[1, 3, 2])
                                    ),
                                   "<select_table_name> NOT INDEXED",
                                   ("<select_table_name> <table_alias> NOT INDEXED",
                                    opts(order=[1, 2])
                                    ),
                                   ("<select_table_name> AS <table_alias> NOT INDEXED",
                                    opts(order=[1, 2])
                                    ),
                                   "(<select_table_or_subquery>)",
                                   "(<join_clause>)"],
    "<join_clause>": ["<select_table_or_subquery>",
                      ("<select_table_or_subquery> <join_operator> <select_table_or_subquery> <join_constraint>",
                       opts(order=[1, 2, 3, 4])
                       ),
                      ],
    "<join_operator>": [",", "JOIN", "<natural_join>", "CROSS JOIN"],
    "<join_constraint>": ["ON <expression>",],
    "<where_clause>": ["", "WHERE <expression>", "WHERE <expression> <having_expression>"],
    "<group_by_clause>": ["", "GROUP BY <multipleexpression>", "GROUP BY <multipleexpression> <having_expression>"],
    "<multipleexpression>": ["<expression>", "<expression>, <multipleexpression>"],
    "<having_expression>": ["HAVING <expression>"],
    "<order_by_clause>": ["ORDER BY <multipleordering_term>"],
    "<multipleordering_term>": ["<ordering_term>", "<ordering_term>, <multipleordering_term>"],
    "<ordering_term>": ["<expression>", "<expression> <collate>", "<expression> <collate> <asc_desc> <nulls_first_last>"],
    "<collate>": ["COLLATE <collation_name>"],
    "<limit_clause>": ["LIMIT <expression>", "LIMIT <expression> OFFSET <expression>", "LIMIT <expression> , <expression>"],
    "<table_alias>": ["", "<string>"],
    "<column_alias>": ["<string>"],
    "<select_table_name>": [("<string>",
                             opts(post=lambda select_table_name: db_instance.choose_table_for_selection(select_table_name))
                             )],
    "<select_table_function_name>": ["<string>"],
    "<select_index_name>": [("<string>",
                             opts(post=lambda select_index_name: db_instance.select_index_column(select_index_name))
                             )],
    "<collation_name>": ["<string>"],
    "<string>": ["<letter>", "<letter><string>"],

}

sql_fuzz_grammar = {
    "<start>": ["<create_table>", "<create_index_or_view>", "<additional_commands>"],

    "<create_table>": ["<create_table_statement>", ],
    "<create_index_or_view>": ["<create_index_statement>", "<create_view_statement>",
                               "<create_virtual_table_statement>"
                               ],
    "<additional_commands>": ["<select_statement>", "<alter_table_statement>", "<delete_statement>"
                                                                               "<pragma_statement>",
                              "<simple_function_invocation>",
                              "<date_time_functions>",
                              "<drop_index_statement>", "<drop_table_statement>", "<drop_view_statement>"
                              ],

    **sql_grammar,
}

grammar = trim_grammar(sql_fuzz_grammar)
assert is_valid_grammar(grammar)