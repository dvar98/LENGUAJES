// grammar.c
#include "parser.h"

void *_PyPegen_parse(Parser *p)
{
    // Inicializar palabras clave
    p->keywords = reserved_keywords;
    p->n_keyword_lists = n_keyword_lists;
    p->soft_keywords = soft_keywords;

    // Selección de la regla de inicio según el tipo de entrada
    void *result = NULL;
    if (p->start_rule == Py_file_input) {
        result = file_rule(p);
    } else if (p->start_rule == Py_single_input) {
        result = interactive_rule(p);
    } else if (p->start_rule == Py_eval_input) {
        result = eval_rule(p);
    } else if (p->start_rule == Py_func_type_input) {
        result = func_type_rule(p);
    }

    return result;
}
