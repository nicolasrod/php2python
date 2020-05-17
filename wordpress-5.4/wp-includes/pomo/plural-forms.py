#!/usr/bin/env python3
# coding: utf-8
if '__PHP2PY_LOADED__' not in globals():
    import os
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
    #// 
    #// Operator precedence.
    #// 
    #// Operator precedence from highest to lowest. Higher numbers indicate
    #// higher precedence, and are executed first.
    #// 
    #// @see https://en.wikipedia.org/wiki/Operators_in_C_and_C%2B%2B#Operator_precedence
    #// 
    #// @since 4.9.0
    #// @var array $op_precedence Operator precedence from highest to lowest.
    #//
    op_precedence = Array({"%": 6, "<": 5, "<=": 5, ">": 5, ">=": 5, "==": 4, "!=": 4, "&&": 3, "||": 2, "?:": 1, "?": 1, "(": 0, ")": 0})
    #// 
    #// Tokens generated from the string.
    #// 
    #// @since 4.9.0
    #// @var array $tokens List of tokens.
    #//
    tokens = Array()
    #// 
    #// Cache for repeated calls to the function.
    #// 
    #// @since 4.9.0
    #// @var array $cache Map of $n => $result
    #//
    cache = Array()
    #// 
    #// Constructor.
    #// 
    #// @since 4.9.0
    #// 
    #// @param string $str Plural function (just the bit after `plural=` from Plural-Forms)
    #//
    def __init__(self, str_=None):
        
        
        self.parse(str_)
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
    def parse(self, str_=None):
        
        
        pos_ = 0
        len_ = php_strlen(str_)
        #// Convert infix operators to postfix using the shunting-yard algorithm.
        output_ = Array()
        stack_ = Array()
        while True:
            
            if not (pos_ < len_):
                break
            # end if
            next_ = php_substr(str_, pos_, 1)
            for case in Switch(next_):
                if case(" "):
                    pass
                # end if
                if case("   "):
                    pos_ += 1
                    break
                # end if
                if case("n"):
                    output_[-1] = Array("var")
                    pos_ += 1
                    break
                # end if
                if case("("):
                    stack_[-1] = next_
                    pos_ += 1
                    break
                # end if
                if case(")"):
                    found_ = False
                    while True:
                        
                        if not ((not php_empty(lambda : stack_))):
                            break
                        # end if
                        o2_ = stack_[php_count(stack_) - 1]
                        if "(" != o2_:
                            output_[-1] = Array("op", php_array_pop(stack_))
                            continue
                        # end if
                        #// Discard open paren.
                        php_array_pop(stack_)
                        found_ = True
                        break
                    # end while
                    if (not found_):
                        raise php_new_class("Exception", lambda : Exception("Mismatched parentheses"))
                    # end if
                    pos_ += 1
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
                    end_operator_ = strspn(str_, self.OP_CHARS, pos_)
                    operator_ = php_substr(str_, pos_, end_operator_)
                    if (not php_array_key_exists(operator_, self.op_precedence)):
                        raise php_new_class("Exception", lambda : Exception(php_sprintf("Unknown operator \"%s\"", operator_)))
                    # end if
                    while True:
                        
                        if not ((not php_empty(lambda : stack_))):
                            break
                        # end if
                        o2_ = stack_[php_count(stack_) - 1]
                        #// Ternary is right-associative in C.
                        if "?:" == operator_ or "?" == operator_:
                            if self.op_precedence[operator_] >= self.op_precedence[o2_]:
                                break
                            # end if
                        elif self.op_precedence[operator_] > self.op_precedence[o2_]:
                            break
                        # end if
                        output_[-1] = Array("op", php_array_pop(stack_))
                    # end while
                    stack_[-1] = operator_
                    pos_ += end_operator_
                    break
                # end if
                if case(":"):
                    found_ = False
                    s_pos_ = php_count(stack_) - 1
                    while True:
                        
                        if not (s_pos_ >= 0):
                            break
                        # end if
                        o2_ = stack_[s_pos_]
                        if "?" != o2_:
                            output_[-1] = Array("op", php_array_pop(stack_))
                            s_pos_ -= 1
                            continue
                        # end if
                        #// Replace.
                        stack_[s_pos_] = "?:"
                        found_ = True
                        break
                    # end while
                    if (not found_):
                        raise php_new_class("Exception", lambda : Exception("Missing starting \"?\" ternary operator"))
                    # end if
                    pos_ += 1
                    break
                # end if
                if case():
                    if next_ >= "0" and next_ <= "9":
                        span_ = strspn(str_, self.NUM_CHARS, pos_)
                        output_[-1] = Array("value", php_intval(php_substr(str_, pos_, span_)))
                        pos_ += span_
                        break
                    # end if
                    raise php_new_class("Exception", lambda : Exception(php_sprintf("Unknown symbol \"%s\"", next_)))
                # end if
            # end for
        # end while
        while True:
            
            if not ((not php_empty(lambda : stack_))):
                break
            # end if
            o2_ = php_array_pop(stack_)
            if "(" == o2_ or ")" == o2_:
                raise php_new_class("Exception", lambda : Exception("Mismatched parentheses"))
            # end if
            output_[-1] = Array("op", o2_)
        # end while
        self.tokens = output_
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
    def get(self, num_=None):
        
        
        if (php_isset(lambda : self.cache[num_])):
            return self.cache[num_]
        # end if
        self.cache[num_] = self.execute(num_)
        return self.cache[num_]
    # end def get
    #// 
    #// Execute the plural form function.
    #// 
    #// @since 4.9.0
    #// 
    #// @param int $n Variable "n" to substitute.
    #// @return int Plural form value.
    #//
    def execute(self, n_=None):
        
        
        stack_ = Array()
        i_ = 0
        total_ = php_count(self.tokens)
        while True:
            
            if not (i_ < total_):
                break
            # end if
            next_ = self.tokens[i_]
            i_ += 1
            if "var" == next_[0]:
                stack_[-1] = n_
                continue
            elif "value" == next_[0]:
                stack_[-1] = next_[1]
                continue
            # end if
            #// Only operators left.
            for case in Switch(next_[1]):
                if case("%"):
                    v2_ = php_array_pop(stack_)
                    v1_ = php_array_pop(stack_)
                    stack_[-1] = v1_ % v2_
                    break
                # end if
                if case("||"):
                    v2_ = php_array_pop(stack_)
                    v1_ = php_array_pop(stack_)
                    stack_[-1] = v1_ or v2_
                    break
                # end if
                if case("&&"):
                    v2_ = php_array_pop(stack_)
                    v1_ = php_array_pop(stack_)
                    stack_[-1] = v1_ and v2_
                    break
                # end if
                if case("<"):
                    v2_ = php_array_pop(stack_)
                    v1_ = php_array_pop(stack_)
                    stack_[-1] = v1_ < v2_
                    break
                # end if
                if case("<="):
                    v2_ = php_array_pop(stack_)
                    v1_ = php_array_pop(stack_)
                    stack_[-1] = v1_ <= v2_
                    break
                # end if
                if case(">"):
                    v2_ = php_array_pop(stack_)
                    v1_ = php_array_pop(stack_)
                    stack_[-1] = v1_ > v2_
                    break
                # end if
                if case(">="):
                    v2_ = php_array_pop(stack_)
                    v1_ = php_array_pop(stack_)
                    stack_[-1] = v1_ >= v2_
                    break
                # end if
                if case("!="):
                    v2_ = php_array_pop(stack_)
                    v1_ = php_array_pop(stack_)
                    stack_[-1] = v1_ != v2_
                    break
                # end if
                if case("=="):
                    v2_ = php_array_pop(stack_)
                    v1_ = php_array_pop(stack_)
                    stack_[-1] = v1_ == v2_
                    break
                # end if
                if case("?:"):
                    v3_ = php_array_pop(stack_)
                    v2_ = php_array_pop(stack_)
                    v1_ = php_array_pop(stack_)
                    stack_[-1] = v2_ if v1_ else v3_
                    break
                # end if
                if case():
                    raise php_new_class("Exception", lambda : Exception(php_sprintf("Unknown operator \"%s\"", next_[1])))
                # end if
            # end for
        # end while
        if php_count(stack_) != 1:
            raise php_new_class("Exception", lambda : Exception("Too many values remaining on the stack"))
        # end if
        return php_int(stack_[0])
    # end def execute
# end class Plural_Forms
