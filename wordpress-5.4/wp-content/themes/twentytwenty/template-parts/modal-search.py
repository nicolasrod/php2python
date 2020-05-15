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
pass
php_print("""<div class=\"search-modal cover-modal header-footer-group\" data-modal-target-string=\".search-modal\">
<div class=\"search-modal-inner modal-inner\">
<div class=\"section-inner\">
""")
get_search_form(Array({"label": __("Search for:", "twentytwenty")}))
php_print("\n           <button class=\"toggle search-untoggle close-search-toggle fill-children-current-color\" data-toggle-target=\".search-modal\" data-toggle-body-class=\"showing-search-modal\" data-set-focus=\".search-modal .search-field\" aria-expanded=\"false\">\n             <span class=\"screen-reader-text\">")
_e("Close search", "twentytwenty")
php_print("</span>\n                ")
twentytwenty_the_theme_svg("cross")
php_print("""           </button><!-- .search-toggle -->
</div><!-- .section-inner -->
</div><!-- .search-modal-inner -->
</div><!-- .menu-modal -->
""")
