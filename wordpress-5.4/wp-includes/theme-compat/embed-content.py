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
php_print(" <div ")
post_class("wp-embed")
php_print(">\n      ")
thumbnail_id = 0
if has_post_thumbnail():
    thumbnail_id = get_post_thumbnail_id()
# end if
if "attachment" == get_post_type() and wp_attachment_is_image():
    thumbnail_id = get_the_ID()
# end if
#// 
#// Filters the thumbnail image ID for use in the embed template.
#// 
#// @since 4.9.0
#// 
#// @param int $thumbnail_id Attachment ID.
#//
thumbnail_id = apply_filters("embed_thumbnail_id", thumbnail_id)
if thumbnail_id:
    aspect_ratio = 1
    measurements = Array(1, 1)
    image_size = "full"
    #// Fallback.
    meta = wp_get_attachment_metadata(thumbnail_id)
    if (not php_empty(lambda : meta["sizes"])):
        for size,data in meta["sizes"]:
            if data["height"] > 0 and data["width"] / data["height"] > aspect_ratio:
                aspect_ratio = data["width"] / data["height"]
                measurements = Array(data["width"], data["height"])
                image_size = size
            # end if
        # end for
    # end if
    #// 
    #// Filters the thumbnail image size for use in the embed template.
    #// 
    #// @since 4.4.0
    #// @since 4.5.0 Added `$thumbnail_id` parameter.
    #// 
    #// @param string $image_size   Thumbnail image size.
    #// @param int    $thumbnail_id Attachment ID.
    #//
    image_size = apply_filters("embed_thumbnail_image_size", image_size, thumbnail_id)
    shape = "rectangular" if measurements[0] / measurements[1] >= 1.75 else "square"
    #// 
    #// Filters the thumbnail shape for use in the embed template.
    #// 
    #// Rectangular images are shown above the title while square images
    #// are shown next to the content.
    #// 
    #// @since 4.4.0
    #// @since 4.5.0 Added `$thumbnail_id` parameter.
    #// 
    #// @param string $shape        Thumbnail image shape. Either 'rectangular' or 'square'.
    #// @param int    $thumbnail_id Attachment ID.
    #//
    shape = apply_filters("embed_thumbnail_image_shape", shape, thumbnail_id)
# end if
if thumbnail_id and "rectangular" == shape:
    php_print("         <div class=\"wp-embed-featured-image rectangular\">\n               <a href=\"")
    the_permalink()
    php_print("\" target=\"_top\">\n                    ")
    php_print(wp_get_attachment_image(thumbnail_id, image_size))
    php_print("             </a>\n          </div>\n        ")
# end if
php_print("\n       <p class=\"wp-embed-heading\">\n            <a href=\"")
the_permalink()
php_print("\" target=\"_top\">\n                ")
the_title()
php_print("""           </a>
</p>
""")
if thumbnail_id and "square" == shape:
    php_print("         <div class=\"wp-embed-featured-image square\">\n                <a href=\"")
    the_permalink()
    php_print("\" target=\"_top\">\n                    ")
    php_print(wp_get_attachment_image(thumbnail_id, image_size))
    php_print("             </a>\n          </div>\n        ")
# end if
php_print("\n       <div class=\"wp-embed-excerpt\">")
the_excerpt_embed()
php_print("</div>\n\n       ")
#// 
#// Prints additional content after the embed excerpt.
#// 
#// @since 4.4.0
#//
do_action("embed_content")
php_print("\n       <div class=\"wp-embed-footer\">\n           ")
the_embed_site_title()
php_print("\n           <div class=\"wp-embed-meta\">\n             ")
#// 
#// Prints additional meta content in the embed template.
#// 
#// @since 4.4.0
#//
do_action("embed_content_meta")
php_print("""           </div>
</div>
</div>
""")
