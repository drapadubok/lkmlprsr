import parsimonious
import os


# TODO: correctly process all:
# https://docs.looker.com/reference/lookml-quick-reference

# TODO: parse into lookml-gen nodes.

# TODO: find out why comment parsing is problematic in the bigger text
# Problematic
expr_syntax = r"""
    comment = "#" ~r"[\w\s+]*"
"""
grammar = Grammar(expr_syntax)
data = "# I am a comment"
parsed = grammar.parse(data)


data = """
view: api_requests {

    sql_table_name: prod.api_requests ;;

    dimension: root_id {
        type: string
        sql: ${TABLE}.root_id ;;
    }

    dimension: group {
        type: string
        sql: ${TABLE}.group ;;
    }

    dimension: group {
        type: string
        sql: ${TABLE}.group ;;
    }

    measure: total_profit {
        type: number
        sql: ${total_revenue} - ${total_cost} ;;
        value_format_name: usd
    }it
}
"""

# use block type instead of specific term
view_syntax = r"""
    view                 = _? "view" _? ":" _? view_name _? block _?
    sql_table            = _? "sql_table_name" _? ":" _? sql_table_name _? double_semicolon? _?
    dimension            = _? "dimension" _? ":" _? dimension_name _? block _?
    dimension_group      = _? "dimension_group" _? ":" _? dimension_group_name _? block _?
    measure              = _? "measure" _? ":" _? measure_name _? block _?
    type                 = _? "type" _? ":" _? type_name _?
    view_name            = string
    dimension_name       = string
    dimension_group_name = string
    sql_table_name       = string
    measure_name         = string
    type_name            = string
    sql_expr             = _? "sql" _? ":" _? text _? double_semicolon? _?
    expr                 = _? lhand _? ":" _? rhand _?
    lhand                = string
    rhand                = _? (block / string)+ _?
    string               = ~"[A-Z0-9_\.{}$]*"i
    text                 = ~"[A-Z0-9 \.{}$_-]*"i
    block                = "{" block_content+ "}"
    block_name           = string
    block_content        = (sql_table / dimension / dimension_group / sql_expr / expr / measure / type)
    ws                   = ~r"\s+"
    newline              = ~r"\n*"
    comment              = "#" ~r"[\w\s+]*"
    _                    = (ws / newline / comment)*
    double_semicolon     = ";;"
"""
grammar = Grammar(view_syntax)
parsed = grammar.parse(data)
print(parsed.prettily())
