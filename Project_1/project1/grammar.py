# Implement your grammar here in the `grammar` variable.
# You may define additional functions, e.g. for generators.
# You may not import any other modules written by yourself.
# That is, your entire implementation must be in `grammar.py`
# and `fuzzer.py`.

grammar = {"<start>": ["<select_stmt>", "<insert_stmt>", "<drop_view_stmt>", "<detach_stmt>", "<rollback_stmt>",
                       "<release_stmt>", "<savepoint_stmt>", "<conflict_clause>", "<pragma_stmt>", "<re>",
                       "<create_index>", "<create_table>", "<alter_table>", "<analyze_stmt>", "<attach_stmt>",
                       "<transaction_control>", "<comment>", "<create_virtual_table_stmt>", "<drop_table_stmt>"],
           "<create_table>": ["CREATE TABLE <table_name> (<table_columns_def>);"],
           "<table_name>": ["<identifier>"],
           "<table_columns_def>": ["<table_column_def>", "<table_columns_def>, <table_column_def>"],
           "<table_column_def>": ["<column_name> <column_type> <column_constraint>"],
           "<column_name>": ["<identifier>"],
           "<column_type>": ["TEXT", "INTEGER", "REAL", "BLOB", "NUMERIC"],
           "<column_constraint>": ["<constraint_type>"],
           "<constraint_type>": ["PRIMARY KEY", "UNIQUE", "NOT NULL"],

           "<drop_view_stmt>": ["DROP VIEW <if_exists> <schema_name><view_name>"],
           "<if_exists>": ["IF EXISTS", ""],
           "<schema_name>": ["<identifier>.", ""],
           "<view_name>": ["<identifier>"],

           "<insert_stmt>": [
               "<with_clause> <insert_or_replace> INTO <table_with_schema_and_alias> <column_name_list> "
               "<values_or_select> <upsert_clause>"
           ],
           "<with_clause>": ["WITH <recursive> <common_table_expression>", ""],
           "<recursive>": ["RECURSIVE", ""],
           "<common_table_expression>": [
               "<table_name> AS <materialized_clause> <select_stmt>", ""
           ],
           "<materialized_clause>": ["<materialized>", ""],
           "<materialized>": ["NOT MATERIALIZED", "MATERIALIZED"],

           "<insert_or_replace>": ["REPLACE", "INSERT OR <conflict_resolution>", "INSERT"],
           "<conflict_resolution>": ["ABORT", "FAIL", "IGNORE", "REPLACE", "ROLLBACK"],

           "<table_with_schema_and_alias>": [
               "<schema_name><table_name> <alias>",
               "<schema_name><table_name>",
               "<table_name> <alias>",
               "<table_name>"
           ],
           "<schema_name>": ["<identifier>.", ""],
           "<table_name>": ["<identifier>"],
           "<alias>": ["AS <identifier>", ""],

           "<column_name_list>": ["(<column_name_list_contents>)", ""],
           "<column_name_list_contents>": [
               "<column_name>",
               "<column_name_list_contents>, <column_name>"
           ],
           "<column_name>": ["<identifier>"],

           "<values_or_select>": [
               "VALUES (<expr_list>)",
               "<select_stmt>",
               "DEFAULT VALUES"
           ],
           "<expr_list>": ["<expr>", "<expr_list>, <expr>"],
           "<upsert_clause>": [
               "ON CONFLICT <conflict_target> DO <resolution>", ""
           ],
           "<conflict_target>": [
               "(<indexed_column>) WHERE <expr>",
               "<indexed_column>", ""
           ],
           "<indexed_column>": ["<identifier>"],

           "<resolution>": [
               "NOTHING",
               "UPDATE SET <column_update_list> WHERE <expr>", ""
           ],
           "<column_update_list>": [
               "<column_name> = <expr>",
               "<column_update_list>, <column_name> = <expr>"
           ],
           "<select_stmt>": [
               "SELECT <distinct_or_all> <result_columns> FROM <table_or_subquery> <join_clause> <where_clause> "
               "<group_by_clause> <window_clause> <order_by_clause> <limit_clause>"
           ],
           "<distinct_or_all>": ["DISTINCT", "ALL", ""],
           "<result_columns>": ["<result_column>", "<result_columns>, <result_column>"],
           "<result_column>": ["<expr> AS <column_alias>", "<expr>"],

           "<table_or_subquery>": [
               "<table_with_schema_and_alias>",
               "<table_function_name>(<expr>) AS <alias>",
               "(<select_stmt>) AS <alias>",
               "..."
           ],
           "<join_clause>": [
               "<table_or_subquery> <join_operator> <table_or_subquery> ON <join_constraint>",
               ""
           ],
           "<join_operator>": ["INNER JOIN", "LEFT JOIN", "CROSS JOIN", "..."],
           "<join_constraint>": ["<expr>"],

           "<window_clause>": [
               "WINDOW <window_name> AS (<window_definition>)",
               ""
           ],
           "<window_definition>": [
               "<base_window_name> <partition_by> <order_by> <frame_spec>",
               ""
           ],
           "<base_window_name>": ["<identifier>"],
           "<partition_by>": ["PARTITION BY <expr>", ""],
           "<order_by>": ["ORDER BY <ordering_term>", ""],

           "<where_clause>": ["WHERE <expr>", ""],
           "<group_by_clause>": ["GROUP BY <expr>", ""],
           "<order_by_clause>": ["ORDER BY <ordering_term>", ""],
           "<limit_clause>": ["LIMIT <expr> OFFSET <expr>", "LIMIT <expr>", ""],
           "<column_alias>": ["<identifier>"],
           "<table_function_name>": ["<identifier>"],

           "<drop_table_stmt>": [
               "DROP TABLE IF EXISTS <schema_name>.<table_name>",
               "DROP TABLE IF EXISTS <table_name>",
               "DROP <table_name>",
               "DROP TABLE <schema_name>.<table_name>",
           ],

           "<re>": ["REINDEX <reindex_target>"],
           "<reindex_target>": ["<collation_name>", "<schema_name>.<table_or_index_name>", "<table_or_index_name>"],
           "<collation_name>": ["<identifier>"],
           "<schema_name>": ["<identifier>"],
           "<table_or_index_name>": ["<table_name>", "<index_name>"],
           "<table_name>": ["<identifier>"],
           "<index_name>": ["<identifier>"],

           "<pragma_stmt>": ["PRAGMA <optional_schema>.<pragma_name><optional_value>"],
           "<optional_schema>": ["<identifier>.", ""],
           "<pragma_name>": ["<identifier>"],
           "<optional_value>": ["= <pragma_value>", ""],
           "<pragma_value>": ["<signed_number>", "<name>", "<signed_literal>"],
           "<signed_number>": ["<number>", "-<number>"],
           "<name>": ["<identifier>"],
           "<signed_literal>": ["<literal_value>", "-<literal_value>"],
           "<number>": ["<digit><number_tail>"],
           "<number_tail>": ["<digit><number_tail>", ""],
           "<digit>": ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"],
           "<literal_value>": ["<numeric_literal>", "<identifier>", "<blob>", "NULL", "TRUE", "FALSE", "CURRENT_TIME",
                               "CURRENT_DATE", "CURRENT_TIMESTAMP"],
           "<numeric_literal>": ["<integer_literal>", "<real_literal>"],
           "<integer_literal>": ["<digit>", "<digit><integer_literal>"],
           "<real_literal>": ["<digit><integer_literal>.<digit><integer_literal>",
                              "<integer_literal>.<digit><integer_literal>", "<digit><integer_literal>",
                              ".<digit><integer_literal>"],
           "<digit>": ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"],
           "<blob>": ["X'<hex_digit>*'"],
           "<hex_digit>": ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "A", "B", "C", "D", "E", "F", "a", "b",
                           "c", "d", "e", "f"],

           "<create_index>": [
               "CREATE <unique> INDEX <if_not_exists> <schema_name><index_name> ON <table_name> (<indexed_columns>) "
               "<where_clause>;"],
           "<unique>": ["UNIQUE", ""],
           "<if_not_exists>": ["IF NOT EXISTS", ""],
           "<schema_name>": ["<identifier>.", ""],
           "<index_name>": ["<column_name> <collate_clause> <ordering>"],
           "<column_name>": ["<identifier>"],
           "<collate_clause>": ["COLLATE <collation_name>", ""],
           "<collation_name>": ["<identifier>"],
           "<ordering>": ["ASC", "DESC", ""],
           "<table_name>": ["<identifier>"],
           "<indexed_columns>": ["<indexed_column>", "<indexed_columns>, <indexed_column>"],
           "<indexed_column>": ["<identifier>"],
           "<where_clause>": ["WHERE <expr>", ""],
           "<expr>": ["<identifier>"],

           "<alter_table>": ["ALTER TABLE <schema_opt> <identifier> <alter_opt>;"],
           "<schema_opt>": ["<identifier>.", ""],
           "<alter_opt>": ["RENAME TO <identifier>", "RENAME <is_column> <identifier> TO <identifier>",
                           "ADD <is_column> <column_def>", "DROP <is_column> <identifier>"],
           "<is_column>": ["COLUMN", ""],
           "<column_def>": ["<table_column_def>"],
           "<table_column_def>": ["<column_name> <column_type> <column_constraint>"],
           "<column_constraint>": ["<constraint_type>"],
           "<constraint_type>": ["PRIMARY KEY", "UNIQUE", "NOT NULL"],

           "<analyze_stmt>": ["ANALYZE <analyze_target>;", "ANALYZE;"],
           "<analyze_target>": ["<schema_name>.", "<schema_name>.<table_or_index_name>", "<table_or_index_name>"],
           "<schema_name>": ["<identifier>"],
           "<table_or_index_name>": ["<index_or_table_name>"],
           "<index_or_table_name>": ["<identifier>"],

           "<attach_stmt>": ["ATTACH DATABASE <expr> AS <schema_name>;", "ATTACH DATABASE <expr>;",
                             "ATTACH DATABASE <expr> AS <schema_name>"],
           "<expr>": ["<literal_value>",
                      "<bind_parameter>",
                      "<schema_name>.<table_name>.<column_name>",
                      "<unary_operator>",
                      "<column_name>",
                      "<expr> <binary_operator> <expr>",
                      "<function_name> (<function_arguments>)<filter_clause> <over_clause>",
                      "<function_name> (<function_arguments>)<filter_clause>",
                      "<function_name> (<function_arguments>)<over_clause>",
                      "CAST (<expr> AS <column_type>)",
                      "<expr> COLLATE <identifier>",
                      "<<expr>  LIKE <expr> ,<expr> LIKE <expr> ESCAPE <expr>,<expr> GLOB <expr>,<expr> REGEXP "
                      "<expr>,<expr> MATCH <expr>, <expr>  NOT LIKE <expr>,<expr>  NOT LIKE <expr> ESCAPE <expr>,"
                      "<expr>  NOT GLOB <expr>,<expr>  NOT REGEXP <expr>,<expr>  NOT MATCH <expr>",
                      "<expr> ISNULL, <expr> NOTNULL, <expr>  NOT NULL",
                      "<expr> IS <expr> ,<expr> IS NOT <expr> ,<expr>  IS NOT DISTINCT FROM <expr>,<expr>  IS  "
                      "DISTINCT FROM <expr>",
                      "<expr> NOT BETWEEN <expr> AND <expr>,<expr>  BETWEEN <expr> AND <expr>",
                      "CASE <expr> WHEN <expr> THEN <expr> ELSE <expr> END",
                      "<raise_function>"
                      ],

           "<function_name>": ["<identifier>", "abs", "changes", "char", "coalesce", "concat", "concat_ws", "format",
                               "glob", "hex", "ifnull", "iif", "instr", "last_insert_rowid", "length", "like",
                               "likelihood", "likely", "load_extension", "lower", "ltrim", "max", "min",
                               "nullif",
                               "octet_length",
                               "printf",
                               "quote",
                               "random",
                               "randomblob",
                               "replace",
                               "round",
                               "rtrim",
                               "sign",
                               "soundex",
                               "sqlite_compileoption_get",
                               "sqlite_compileoption_used",
                               "sqlite_offset",
                               "sqlite_source_id",
                               "sqlite_version",
                               "substr",
                               "substring",
                               "total_changes",
                               "trim",
                               "typeof",
                               "unhex",
                               "unicode",
                               "unlikely",
                               "upper",
                               "zeroblob"
                               ],

           "<over_clause>": [
               "OVER <window_name> (<base_window_name> PARTITION BY <expr>, ORDER BY <ordering_term>, <frame_spec>)",
               "OVER <window_name> (<base_window_name> PARTITION BY <expr>, ORDER BY <ordering_term>)",
               "OVER <window_name> (<base_window_name> ORDER BY <ordering_term>)",
               "OVER <window_name> (<base_window_name>)",
               "OVER <window_name>"
           ],
           "<window_name>": ["<identifier>"],
           "<base_window_name>": ["<identifier>"],
           "<frame_spec>": ["<frame_start>", "<frame_start> <frame_extent>"],
           "<frame_start>": ["UNBOUNDED PRECEDING", "<expr> PRECEDING", "CURRENT ROW", "UNBOUNDED FOLLOWING",
                             "<expr> FOLLOWING"],
           "<frame_extent>": ["ROWS", "RANGE"],

           "<raise_function>": [
               "RAISE(ROLLBACK,<error_message>)",
               "RAISE(IGNORE)",
               "RAISE(ABORT,<error_message>)",
               "RAISE(FAIL,<error_message>)"
           ],
           "<error_message>": ["<identifier>"],
           "<filter_clause>": ["FILTER (<where_clause>)"],
           "<where_clause>": ["WHERE <expr>"],

           "<literal_value>": ["<numeric_literal>", "<identifier>", "<blob>", "NULL", "TRUE", "FALSE", "CURRENT_TIME",
                               "CURRENT_DATE", "CURRENT_TIMESTAMP"],
           "<numeric_literal>": ["<integer_literal>", "<real_literal>"],
           "<integer_literal>": ["<digit>", "<digit><integer_literal>"],
           "<real_literal>": ["<digit><integer_literal>.<digit><integer_literal>",
                              "<integer_literal>.<digit><integer_literal>", "<digit><integer_literal>",
                              ".<digit><integer_literal>"],
           "<digit>": ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"],
           "<blob>": ["X'<hex_digit>*'"],
           "<hex_digit>": ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "A", "B", "C", "D", "E", "F", "a", "b",
                           "c", "d", "e", "f"],

           "<bind_parameter>": ["?"],
           "<unary_operator>": ["+ <expr>", "- <expr>"],
           "<binary_operator>": ["+", "-", "*", "/", "%", "&", "|", "<<", ">>", "<", ">", "<=", ">=", "==", "!=", "AND",
                                 "OR", "LIKE", "GLOB", "MATCH", "IS", "IN", "BETWEEN", "||"],

           "<function_arguments>": ["<distinct_clause> <expr>", "*", "ORDER BY <ordering_term>"],
           "<ordering_term>": ["<expr>", "<collation_clause> <ordering_direction> <nulls_clause>"],
           "<collation_clause>": ["COLLATE <identifier>"],
           "<ordering_direction>": ["DESC", "ASC"],
           "<nulls_clause>": ["NULLS FIRST", "NULLS LAST"],
           "<distinct_clause>": ["DISTINCT"],

           "<transaction_control>": ["<begin_stmt>", "<commit_stmt>", "<rollback_stmt>"],
           "<begin_stmt>": ["BEGIN <transaction_mode> TRANSACTION", "BEGIN TRANSACTION", "BEGIN <transaction_mode>",
                            "BEGIN"],
           "<commit_stmt>": ["COMMIT TRANSACTION", "COMMIT", "END TRANSACTION", "END"],
           "<rollback_stmt>": ["ROLLBACK TRANSACTION TO SAVEPOINT <savepoint_name>", "ROLLBACK TRANSACTION",
                               "ROLLBACK TO SAVEPOINT <savepoint_name>", "ROLLBACK"],
           "<transaction_mode>": ["DEFERRED", "IMMEDIATE", "EXCLUSIVE"],
           "<savepoint_name>": ["<identifier>"],

           "<comment>": ["<single_line_comment>", "<multi_line_comment>"],
           "<single_line_comment>": ["--<anything_except_newline><newline>",
                                     "--<anything_except_newline><end_of_input>"],
           "<multi_line_comment>": ["/<multi_line_content>/"],
           "<anything_except_newline>": ["<any_character_except_newline>*"],
           "<multi_line_content>": ["<multi_line_chars>*"],
           "<multi_line_chars>": ["<anything_except_ending_sequence>", "<multi_line_comment>"],
           "<anything_except_ending_sequence>": ["<any_character_except_star>", "<star_not_followed_by_slash>"],
           "<star_not_followed_by_slash>": ["<star><any_character_except_slash>"],
           "<any_character_except_newline>": ["<any_valid_character>"],
           "<any_character_except_star>": ["<any_valid_character>"],
           "<any_character_except_slash>": ["<any_valid_character>"],
           "<star>": ["*"],
           "<newline>": ["\\n"],
           "<end_of_input>": ["EOF"],
           "<any_valid_character>": ["a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m",
                                     "n", "o", "p", "q", "r", "s", "t", "u", "v", "w", "x", "y", "z",
                                     "A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M",
                                     "N", "O", "P", "Q", "R", "S", "T", "U", "V", "W", "X", "Y", "Z",
                                     "0", "1", "2", "3", "4", "5", "6", "7", "8", "9",
                                     " ", "!", "@", "#", "$", "%", "^", "&", "*", "(", ")", "-", "_",
                                     "+", "=", "{", "}", "[", "]", ";", ":", "<", ">", ",", ".", "?",
                                     "/", "|", "\\", "~", "`"],

           "<create_virtual_table_stmt>": [
               "CREATE VIRTUAL TABLE <if_not_exists> <schema_name><table_name> USING <module_name> (<module_arguments>)"
           ],
           "<if_not_exists>": ["IF NOT EXISTS", ""],
           "<schema_name>": ["<identifier>.", ""],
           "<table_name>": ["<identifier>"],
           "<module_name>": ["<identifier>"],
           "<module_arguments>": ["<module_argument>", "<module_arguments>, <module_argument>"],
           "<module_argument>": ["<identifier>"],

           "<conflict_clause>": ["ON CONFLICT <action>"],
           "<action>": ["ROLLBACK", "ABORT", "FAIL", "IGNORE", "REPLACE"],

           "<savepoint_stmt>": ["SAVEPOINT <savepoint_name>"],
           "<release_stmt>": ["RELEASE SAVEPOINT <savepoint_name>"],
           "<rollback_stmt>": ["ROLLBACK TRANSACTION TO SAVEPOINT <savepoint_name>"],
           "<savepoint_name>": ["<identifier>"],

           "<detach_stmt>": ["DETACH DATABASE <schema_name>"],
           "<schema_name>": ["<identifier>"],

           "<identifier>": ["<letter>", "<letter><identifier>", ""],
           "<letter>": ["a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m",
                        "n", "o", "p", "q", "r", "s", "t", "u", "v", "w", "x", "y", "z"]

           }
