#!/usr/bin/env python3
# coding: utf-8
if '__PHP2PY_LOADED__' not in globals():
    import cgi
    import os
    import os.path
    import copy
    import sys
    from goto import with_goto
    with open(os.getenv('PHP2PY_COMPAT', 'php_compat.py')) as f:
        exec(compile(f.read(), '<string>', 'exec'))
    # end with
    globals()['__PHP2PY_LOADED__'] = True
# end if
#// 
#// A gettext Plural-Forms parser.
#// 
#// @since 4.9.0
#//
class Plural_Forms():
    OP_CHARS = "|&><!=%?:"
    NUM_CHARS = "0123456789"
    op_precedence = Array({"%": 6, "<": 5, "<=": 5, ">": 5, ">=": 5, "==": 4, "!=": 4, "&&": 3, "||": 2, "?:": 1, "?": 1, "(": 0, ")": 0})
    tokens = Array()
    cache = Array()
    #// 
    #// Constructor.
    #// 
    #// @since 4.9.0
    #// 
    #// @param string $str Plural function (just the bit after `plural=` from Plural-Forms)
    #//
    def __init__(self, str=None):
        
        self.parse(str)
    # end def __init__
    #// 
    #// Parse a Plural-Forms string into tokens.
    #// 
    #// Uses the shunting-yard algorithm to convert the string to Reverse Polish
    #// Notation tokens.
    #// 
    #// @since 4.9.0
    #// 
    #// @param string $str String to parse.
    #//
    def parse(self, str=None):
        
        pos = 0
        len = php_strlen(str)
        #// Convert infix operators to postfix using the shunting-yard algorithm.
        output = Array()
        stack = Array()
        while True:
            
            if not (pos < len):
                break
            # end if
            next = php_substr(str, pos, 1)
            for case in Switch(next):
                if case(" "):
                    pass
                # end if
                if case("   "):
                    pos += 1
                    break
                # end if
                if case("n"):
                    output[-1] = Array("var")
                    pos += 1
                    break
                # end if
                if case("("):
                    stack[-1] = next
                    pos += 1
                    break
                # end if
                if case(")"):
                    found = False
                    while True:
                        
                        if not ((not php_empty(lambda : stack))):
                            break
                        # end if
                        o2 = stack[php_count(stack) - 1]
                        if "(" != o2:
                            output[-1] = Array("op", php_array_pop(stack))
                            continue
                        # end if
                        #// Discard open paren.
                        php_array_pop(stack)
                        found = True
                        break
                    # end while
                    if (not found):
                        raise php_new_class("Exception", lambda : Exception("Mismatched parentheses"))
                    # end if
                    pos += 1
                    break
                # end if
                if case("|"):
                    pass
                # end if
                if case("&"):
                    pass
                # end if
                if case(">"):
                    pass
                # end if
                if case("<"):
                    pass
                # end if
                if case("!"):
                    pass
                # end if
                if case("="):
                    pass
                # end if
                if case("%"):
                    pass
                # end if
                if case("?"):
                    end_operator = strspn(str, self.OP_CHARS, pos)
                    operator = php_substr(str, pos, end_operator)
                    if (not php_array_key_exists(operator, self.op_precedence)):
                        raise php_new_class("Exception", lambda : Exception(php_sprintf("Unknown operator \"%s\"", operator)))
                    # end if
                    while True:
                        
                        if not ((not php_empty(lambda : stack))):
                            break
                        # end if
                        o2 = stack[php_count(stack) - 1]
                        #// Ternary is right-associative in C.
                        if "?:" == operator or "?" == operator:
                            if self.op_precedence[operator] >= self.op_precedence[o2]:
                                break
                            # end if
                        elif self.op_precedence[operator] > self.op_precedence[o2]:
                            break
                        # end if
                        output[-1] = Array("op", php_array_pop(stack))
                    # end while
                    stack[-1] = operator
                    pos += end_operator
                    break
                # end if
                if case(":"):
                    found = False
                    s_pos = php_count(stack) - 1
                    while True:
                        
                        if not (s_pos >= 0):
                            break
                        # end if
                        o2 = stack[s_pos]
                        if "?" != o2:
                            output[-1] = Array("op", php_array_pop(stack))
                            s_pos -= 1
                            continue
                        # end if
                        #// Replace.
                        stack[s_pos] = "?:"
                        found = True
                        break
                    # end while
                    if (not found):
                        raise php_new_class("Exception", lambda : Exception("Missing starting \"?\" ternary operator"))
                    # end if
                    pos += 1
                    break
                # end if
                if case():
                    if next >= "0" and next <= "9":
                        span = strspn(str, self.NUM_CHARS, pos)
                        output[-1] = Array("value", php_intval(php_substr(str, pos, span)))
                        pos += span
                        break
                    # end if
                    raise php_new_class("Exception", lambda : Exception(php_sprintf("Unknown symbol \"%s\"", next)))
                # end if
            # end for
        # end while
        while True:
            
            if not ((not php_empty(lambda : stack))):
                break
            # end if
            o2 = php_array_pop(stack)
            if "(" == o2 or ")" == o2:
                raise php_new_class("Exception", lambda : Exception("Mismatched parentheses"))
            # end if
            output[-1] = Array("op", o2)
        # end while
        self.tokens = output
    # end def parse
    #// 
    #// Get the plural form for a number.
    #// 
    #// Caches the value for repeated calls.
    #// 
    #// @since 4.9.0
    #// 
    #// @param int $num Number to get plural form for.
    #// @return int Plural form value.
    #//
    def get(self, num=None):
        
        if (php_isset(lambda : self.cache[num])):
            return self.cache[num]
        # end if
        self.cache[num] = self.execute(num)
        return self.cache[num]
    # end def get
    #// 
    #// Execute the plural form function.
    #// 
    #// @since 4.9.0
    #// 
    #// @param int $n Variable "n" to substitute.
    #// @return int Plural form value.
    #//
    def execute(self, n=None):
        
        stack = Array()
        i = 0
        total = php_count(self.tokens)
        while True:
            
            if not (i < total):
                break
            # end if
            next = self.tokens[i]
            i += 1
            if "var" == next[0]:
                stack[-1] = n
                continue
            elif "value" == next[0]:
                stack[-1] = next[1]
                continue
            # end if
            #// Only operators left.
            for case in Switch(next[1]):
                if case("%"):
                    v2 = php_array_pop(stack)
                    v1 = php_array_pop(stack)
                    stack[-1] = v1 % v2
                    break
                # end if
                if case("||"):
                    v2 = php_array_pop(stack)
                    v1 = php_array_pop(stack)
                    stack[-1] = v1 or v2
                    break
                # end if
                if case("&&"):
                    v2 = php_array_pop(stack)
                    v1 = php_array_pop(stack)
                    stack[-1] = v1 and v2
                    break
                # end if
                if case("<"):
                    v2 = php_array_pop(stack)
                    v1 = php_array_pop(stack)
                    stack[-1] = v1 < v2
                    break
                # end if
                if case("<="):
                    v2 = php_array_pop(stack)
                    v1 = php_array_pop(stack)
                    stack[-1] = v1 <= v2
                    break
                # end if
                if case(">"):
                    v2 = php_array_pop(stack)
                    v1 = php_array_pop(stack)
                    stack[-1] = v1 > v2
                    break
                # end if
                if case(">="):
                    v2 = php_array_pop(stack)
                    v1 = php_array_pop(stack)
                    stack[-1] = v1 >= v2
                    break
                # end if
                if case("!="):
                    v2 = php_array_pop(stack)
                    v1 = php_array_pop(stack)
                    stack[-1] = v1 != v2
                    break
                # end if
                if case("=="):
                    v2 = php_array_pop(stack)
                    v1 = php_array_pop(stack)
                    stack[-1] = v1 == v2
                    break
                # end if
                if case("?:"):
                    v3 = php_array_pop(stack)
                    v2 = php_array_pop(stack)
                    v1 = php_array_pop(stack)
                    stack[-1] = v2 if v1 else v3
                    break
                # end if
                if case():
                    raise php_new_class("Exception", lambda : Exception(php_sprintf("Unknown operator \"%s\"", next[1])))
                # end if
            # end for
        # end while
        if php_count(stack) != 1:
            raise php_new_class("Exception", lambda : Exception("Too many values remaining on the stack"))
        # end if
        return php_int(stack[0])
    # end def execute
# end class Plural_Forms
