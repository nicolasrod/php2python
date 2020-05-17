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
#// Block Serialization Parser
#// 
#// @package WordPress
#// 
#// 
#// Class WP_Block_Parser_Block
#// 
#// Holds the block structure in memory
#// 
#// @since 3.8.0
#//
class WP_Block_Parser_Block():
    #// 
    #// Name of block
    #// 
    #// @example "core/paragraph"
    #// 
    #// @since 3.8.0
    #// @var string
    #//
    blockName = Array()
    #// 
    #// Optional set of attributes from block comment delimiters
    #// 
    #// @example null
    #// @example array( 'columns' => 3 )
    #// 
    #// @since 3.8.0
    #// @var array|null
    #//
    attrs = Array()
    #// 
    #// List of inner blocks (of this same class)
    #// 
    #// @since 3.8.0
    #// @var WP_Block_Parser_Block[]
    #//
    innerBlocks = Array()
    #// 
    #// Resultant HTML from inside block comment delimiters
    #// after removing inner blocks
    #// 
    #// @example "...Just <!-- wp:test /--> testing..." -> "Just testing..."
    #// 
    #// @since 3.8.0
    #// @var string
    #//
    innerHTML = Array()
    #// 
    #// List of string fragments and null markers where inner blocks were found
    #// 
    #// @example array(
    #// 'innerHTML'    => 'BeforeInnerAfter',
    #// 'innerBlocks'  => array( block, block ),
    #// 'innerContent' => array( 'Before', null, 'Inner', null, 'After' ),
    #// )
    #// 
    #// @since 4.2.0
    #// @var array
    #//
    innerContent = Array()
    #// 
    #// Constructor.
    #// 
    #// Will populate object properties from the provided arguments.
    #// 
    #// @since 3.8.0
    #// 
    #// @param string $name         Name of block.
    #// @param array  $attrs        Optional set of attributes from block comment delimiters.
    #// @param array  $innerBlocks  List of inner blocks (of this same class).
    #// @param string $innerHTML    Resultant HTML from inside block comment delimiters after removing inner blocks.
    #// @param array  $innerContent List of string fragments and null markers where inner blocks were found.
    #//
    def __init__(self, name_=None, attrs_=None, innerBlocks_=None, innerHTML_=None, innerContent_=None):
        
        
        self.blockName = name_
        self.attrs = attrs_
        self.innerBlocks = innerBlocks_
        self.innerHTML = innerHTML_
        self.innerContent = innerContent_
    # end def __init__
# end class WP_Block_Parser_Block
#// 
#// Class WP_Block_Parser_Frame
#// 
#// Holds partial blocks in memory while parsing
#// 
#// @internal
#// @since 3.8.0
#//
class WP_Block_Parser_Frame():
    #// 
    #// Full or partial block
    #// 
    #// @since 3.8.0
    #// @var WP_Block_Parser_Block
    #//
    block = Array()
    #// 
    #// Byte offset into document for start of parse token
    #// 
    #// @since 3.8.0
    #// @var int
    #//
    token_start = Array()
    #// 
    #// Byte length of entire parse token string
    #// 
    #// @since 3.8.0
    #// @var int
    #//
    token_length = Array()
    #// 
    #// Byte offset into document for after parse token ends
    #// (used during reconstruction of stack into parse production)
    #// 
    #// @since 3.8.0
    #// @var int
    #//
    prev_offset = Array()
    #// 
    #// Byte offset into document where leading HTML before token starts
    #// 
    #// @since 3.8.0
    #// @var int
    #//
    leading_html_start = Array()
    #// 
    #// Constructor
    #// 
    #// Will populate object properties from the provided arguments.
    #// 
    #// @since 3.8.0
    #// 
    #// @param WP_Block_Parser_Block $block              Full or partial block.
    #// @param int                   $token_start        Byte offset into document for start of parse token.
    #// @param int                   $token_length       Byte length of entire parse token string.
    #// @param int                   $prev_offset        Byte offset into document for after parse token ends.
    #// @param int                   $leading_html_start Byte offset into document where leading HTML before token starts.
    #//
    def __init__(self, block_=None, token_start_=None, token_length_=None, prev_offset_=None, leading_html_start_=None):
        if prev_offset_ is None:
            prev_offset_ = None
        # end if
        if leading_html_start_ is None:
            leading_html_start_ = None
        # end if
        
        self.block = block_
        self.token_start = token_start_
        self.token_length = token_length_
        self.prev_offset = prev_offset_ if (php_isset(lambda : prev_offset_)) else token_start_ + token_length_
        self.leading_html_start = leading_html_start_
    # end def __init__
# end class WP_Block_Parser_Frame
#// 
#// Class WP_Block_Parser
#// 
#// Parses a document and constructs a list of parsed block objects
#// 
#// @since 3.8.0
#// @since 4.0.0 returns arrays not objects, all attributes are arrays
#//
class WP_Block_Parser():
    #// 
    #// Input document being parsed
    #// 
    #// @example "Pre-text\n<!-- wp:paragraph -->This is inside a block!<!-- /wp:paragraph -->"
    #// 
    #// @since 3.8.0
    #// @var string
    #//
    document = Array()
    #// 
    #// Tracks parsing progress through document
    #// 
    #// @since 3.8.0
    #// @var int
    #//
    offset = Array()
    #// 
    #// List of parsed blocks
    #// 
    #// @since 3.8.0
    #// @var WP_Block_Parser_Block[]
    #//
    output = Array()
    #// 
    #// Stack of partially-parsed structures in memory during parse
    #// 
    #// @since 3.8.0
    #// @var WP_Block_Parser_Frame[]
    #//
    stack = Array()
    #// 
    #// Empty associative array, here due to PHP quirks
    #// 
    #// @since 4.4.0
    #// @var array empty associative array
    #//
    empty_attrs = Array()
    #// 
    #// Parses a document and returns a list of block structures
    #// 
    #// When encountering an invalid parse will return a best-effort
    #// parse. In contrast to the specification parser this does not
    #// return an error on invalid inputs.
    #// 
    #// @since 3.8.0
    #// 
    #// @param string $document Input document being parsed.
    #// @return WP_Block_Parser_Block[]
    #//
    def parse(self, document_=None):
        
        
        self.document = document_
        self.offset = 0
        self.output = Array()
        self.stack = Array()
        self.empty_attrs = php_json_decode("{}", True)
        while True:
            pass
            
            if self.proceed():
                break
            # end if
        # end while
        return self.output
    # end def parse
    #// 
    #// Processes the next token from the input document
    #// and returns whether to proceed eating more tokens
    #// 
    #// This is the "next step" function that essentially
    #// takes a token as its input and decides what to do
    #// with that token before descending deeper into a
    #// nested block tree or continuing along the document
    #// or breaking out of a level of nesting.
    #// 
    #// @internal
    #// @since 3.8.0
    #// @return bool
    #//
    def proceed(self):
        
        
        next_token_ = self.next_token()
        token_type_, block_name_, attrs_, start_offset_, token_length_ = next_token_
        stack_depth_ = php_count(self.stack)
        #// we may have some HTML soup before the next block.
        leading_html_start_ = self.offset if start_offset_ > self.offset else None
        for case in Switch(token_type_):
            if case("no-more-tokens"):
                #// if not in a block then flush output.
                if 0 == stack_depth_:
                    self.add_freeform()
                    return False
                # end if
                #// 
                #// Otherwise we have a problem
                #// This is an error
                #// 
                #// we have options
                #// - treat it all as freeform text
                #// - assume an implicit closer (easiest when not nesting)
                #// 
                #// for the easy case we'll assume an implicit closer.
                if 1 == stack_depth_:
                    self.add_block_from_stack()
                    return False
                # end if
                #// 
                #// for the nested case where it's more difficult we'll
                #// have to assume that multiple closers are missing
                #// and so we'll collapse the whole stack piecewise
                #//
                while True:
                    
                    if not (0 < php_count(self.stack)):
                        break
                    # end if
                    self.add_block_from_stack()
                # end while
                return False
            # end if
            if case("void-block"):
                #// 
                #// easy case is if we stumbled upon a void block
                #// in the top-level of the document
                #//
                if 0 == stack_depth_:
                    if (php_isset(lambda : leading_html_start_)):
                        self.output[-1] = self.freeform(php_substr(self.document, leading_html_start_, start_offset_ - leading_html_start_))
                    # end if
                    self.output[-1] = php_new_class("WP_Block_Parser_Block", lambda : WP_Block_Parser_Block(block_name_, attrs_, Array(), "", Array()))
                    self.offset = start_offset_ + token_length_
                    return True
                # end if
                #// otherwise we found an inner block.
                self.add_inner_block(php_new_class("WP_Block_Parser_Block", lambda : WP_Block_Parser_Block(block_name_, attrs_, Array(), "", Array())), start_offset_, token_length_)
                self.offset = start_offset_ + token_length_
                return True
            # end if
            if case("block-opener"):
                #// track all newly-opened blocks on the stack.
                php_array_push(self.stack, php_new_class("WP_Block_Parser_Frame", lambda : WP_Block_Parser_Frame(php_new_class("WP_Block_Parser_Block", lambda : WP_Block_Parser_Block(block_name_, attrs_, Array(), "", Array())), start_offset_, token_length_, start_offset_ + token_length_, leading_html_start_)))
                self.offset = start_offset_ + token_length_
                return True
            # end if
            if case("block-closer"):
                #// 
                #// if we're missing an opener we're in trouble
                #// This is an error
                #//
                if 0 == stack_depth_:
                    #// 
                    #// we have options
                    #// - assume an implicit opener
                    #// - assume _this_ is the opener
                    #// - give up and close out the document
                    #//
                    self.add_freeform()
                    return False
                # end if
                #// if we're not nesting then this is easy - close the block.
                if 1 == stack_depth_:
                    self.add_block_from_stack(start_offset_)
                    self.offset = start_offset_ + token_length_
                    return True
                # end if
                #// 
                #// otherwise we're nested and we have to close out the current
                #// block and add it as a new innerBlock to the parent
                #//
                stack_top_ = php_array_pop(self.stack)
                html_ = php_substr(self.document, stack_top_.prev_offset, start_offset_ - stack_top_.prev_offset)
                stack_top_.block.innerHTML += html_
                stack_top_.block.innerContent[-1] = html_
                stack_top_.prev_offset = start_offset_ + token_length_
                self.add_inner_block(stack_top_.block, stack_top_.token_start, stack_top_.token_length, start_offset_ + token_length_)
                self.offset = start_offset_ + token_length_
                return True
            # end if
            if case():
                #// This is an error.
                self.add_freeform()
                return False
            # end if
        # end for
    # end def proceed
    #// 
    #// Scans the document from where we last left off
    #// and finds the next valid token to parse if it exists
    #// 
    #// Returns the type of the find: kind of find, block information, attributes
    #// 
    #// @internal
    #// @since 3.8.0
    #// @since 4.6.1 fixed a bug in attribute parsing which caused catastrophic backtracking on invalid block comments
    #// @return array
    #//
    def next_token(self):
        
        
        matches_ = None
        #// 
        #// aye the magic
        #// we're using a single RegExp to tokenize the block comment delimiters
        #// we're also using a trick here because the only difference between a
        #// block opener and a block closer is the leading `/` before `wp:` (and
        #// a closer has no attributes). we can trap them both and process the
        #// match back in PHP to see which one it was.
        #//
        has_match_ = php_preg_match("/<!--\\s+(?P<closer>\\/)?wp:(?P<namespace>[a-z][a-z0-9_-]*\\/)?(?P<name>[a-z][a-z0-9_-]*)\\s+(?P<attrs>{(?:(?:[^}]+|}+(?=})|(?!}\\s+\\/?-->).)*+)?}\\s+)?(?P<void>\\/)?-->/s", self.document, matches_, PREG_OFFSET_CAPTURE, self.offset)
        #// if we get here we probably have catastrophic backtracking or out-of-memory in the PCRE.
        if False == has_match_:
            return Array("no-more-tokens", None, None, None, None)
        # end if
        #// we have no more tokens.
        if 0 == has_match_:
            return Array("no-more-tokens", None, None, None, None)
        # end if
        match_, started_at_ = matches_[0]
        length_ = php_strlen(match_)
        is_closer_ = (php_isset(lambda : matches_["closer"])) and -1 != matches_["closer"][1]
        is_void_ = (php_isset(lambda : matches_["void"])) and -1 != matches_["void"][1]
        namespace_ = matches_["namespace"]
        namespace_ = namespace_[0] if (php_isset(lambda : namespace_)) and -1 != namespace_[1] else "core/"
        name_ = namespace_ + matches_["name"][0]
        has_attrs_ = (php_isset(lambda : matches_["attrs"])) and -1 != matches_["attrs"][1]
        #// 
        #// Fun fact! It's not trivial in PHP to create "an empty associative array" since all arrays
        #// are associative arrays. If we use `array()` we get a JSON `[]`
        #//
        attrs_ = php_json_decode(matches_["attrs"][0], True) if has_attrs_ else self.empty_attrs
        #// 
        #// This state isn't allowed
        #// This is an error
        #//
        if is_closer_ and is_void_ or has_attrs_:
            pass
        # end if
        if is_void_:
            return Array("void-block", name_, attrs_, started_at_, length_)
        # end if
        if is_closer_:
            return Array("block-closer", name_, None, started_at_, length_)
        # end if
        return Array("block-opener", name_, attrs_, started_at_, length_)
    # end def next_token
    #// 
    #// Returns a new block object for freeform HTML
    #// 
    #// @internal
    #// @since 3.9.0
    #// 
    #// @param string $innerHTML HTML content of block.
    #// @return WP_Block_Parser_Block freeform block object.
    #//
    def freeform(self, innerHTML_=None):
        
        
        return php_new_class("WP_Block_Parser_Block", lambda : WP_Block_Parser_Block(None, self.empty_attrs, Array(), innerHTML_, Array(innerHTML_)))
    # end def freeform
    #// 
    #// Pushes a length of text from the input document
    #// to the output list as a freeform block.
    #// 
    #// @internal
    #// @since 3.8.0
    #// @param null $length how many bytes of document text to output.
    #//
    def add_freeform(self, length_=None):
        if length_ is None:
            length_ = None
        # end if
        
        length_ = length_ if length_ else php_strlen(self.document) - self.offset
        if 0 == length_:
            return
        # end if
        self.output[-1] = self.freeform(php_substr(self.document, self.offset, length_))
    # end def add_freeform
    #// 
    #// Given a block structure from memory pushes
    #// a new block to the output list.
    #// 
    #// @internal
    #// @since 3.8.0
    #// @param WP_Block_Parser_Block $block        The block to add to the output.
    #// @param int                   $token_start  Byte offset into the document where the first token for the block starts.
    #// @param int                   $token_length Byte length of entire block from start of opening token to end of closing token.
    #// @param int|null              $last_offset  Last byte offset into document if continuing form earlier output.
    #//
    def add_inner_block(self, block_=None, token_start_=None, token_length_=None, last_offset_=None):
        if last_offset_ is None:
            last_offset_ = None
        # end if
        
        parent_ = self.stack[php_count(self.stack) - 1]
        parent_.block.innerBlocks[-1] = block_
        html_ = php_substr(self.document, parent_.prev_offset, token_start_ - parent_.prev_offset)
        if (not php_empty(lambda : html_)):
            parent_.block.innerHTML += html_
            parent_.block.innerContent[-1] = html_
        # end if
        parent_.block.innerContent[-1] = None
        parent_.prev_offset = last_offset_ if last_offset_ else token_start_ + token_length_
    # end def add_inner_block
    #// 
    #// Pushes the top block from the parsing stack to the output list.
    #// 
    #// @internal
    #// @since 3.8.0
    #// @param int|null $end_offset byte offset into document for where we should stop sending text output as HTML.
    #//
    def add_block_from_stack(self, end_offset_=None):
        if end_offset_ is None:
            end_offset_ = None
        # end if
        
        stack_top_ = php_array_pop(self.stack)
        prev_offset_ = stack_top_.prev_offset
        html_ = php_substr(self.document, prev_offset_, end_offset_ - prev_offset_) if (php_isset(lambda : end_offset_)) else php_substr(self.document, prev_offset_)
        if (not php_empty(lambda : html_)):
            stack_top_.block.innerHTML += html_
            stack_top_.block.innerContent[-1] = html_
        # end if
        if (php_isset(lambda : stack_top_.leading_html_start)):
            self.output[-1] = self.freeform(php_substr(self.document, stack_top_.leading_html_start, stack_top_.token_start - stack_top_.leading_html_start))
        # end if
        self.output[-1] = stack_top_.block
    # end def add_block_from_stack
# end class WP_Block_Parser
