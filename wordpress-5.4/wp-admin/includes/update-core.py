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
#// WordPress core upgrade functionality.
#// 
#// @package WordPress
#// @subpackage Administration
#// @since 2.7.0
#// 
#// 
#// Stores files to be deleted.
#// 
#// @since 2.7.0
#// @global array $_old_files
#// @var array
#// @name $_old_files
#//
global _old_files_
php_check_if_defined("_old_files_")
_old_files_ = Array("wp-admin/import-b2.php", "wp-admin/import-blogger.php", "wp-admin/import-greymatter.php", "wp-admin/import-livejournal.php", "wp-admin/import-mt.php", "wp-admin/import-rss.php", "wp-admin/import-textpattern.php", "wp-admin/quicktags.js", "wp-images/fade-butt.png", "wp-images/get-firefox.png", "wp-images/header-shadow.png", "wp-images/smilies", "wp-images/wp-small.png", "wp-images/wpminilogo.png", "wp.php", "wp-includes/js/tinymce/plugins/inlinepopups/readme.txt", "wp-admin/edit-form-ajax-cat.php", "wp-admin/execute-pings.php", "wp-admin/inline-uploading.php", "wp-admin/link-categories.php", "wp-admin/list-manipulation.js", "wp-admin/list-manipulation.php", "wp-includes/comment-functions.php", "wp-includes/feed-functions.php", "wp-includes/functions-compat.php", "wp-includes/functions-formatting.php", "wp-includes/functions-post.php", "wp-includes/js/dbx-key.js", "wp-includes/js/tinymce/plugins/autosave/langs/cs.js", "wp-includes/js/tinymce/plugins/autosave/langs/sv.js", "wp-includes/links.php", "wp-includes/pluggable-functions.php", "wp-includes/template-functions-author.php", "wp-includes/template-functions-category.php", "wp-includes/template-functions-general.php", "wp-includes/template-functions-links.php", "wp-includes/template-functions-post.php", "wp-includes/wp-l10n.php", "wp-admin/cat-js.php", "wp-admin/import/b2.php", "wp-includes/js/autosave-js.php", "wp-includes/js/list-manipulation-js.php", "wp-includes/js/wp-ajax-js.php", "wp-admin/admin-db.php", "wp-admin/cat.js", "wp-admin/categories.js", "wp-admin/custom-fields.js", "wp-admin/dbx-admin-key.js", "wp-admin/edit-comments.js", "wp-admin/install-rtl.css", "wp-admin/install.css", "wp-admin/upgrade-schema.php", "wp-admin/upload-functions.php", "wp-admin/upload-rtl.css", "wp-admin/upload.css", "wp-admin/upload.js", "wp-admin/users.js", "wp-admin/widgets-rtl.css", "wp-admin/widgets.css", "wp-admin/xfn.js", "wp-includes/js/tinymce/license.html", "wp-admin/css/upload.css", "wp-admin/images/box-bg-left.gif", "wp-admin/images/box-bg-right.gif", "wp-admin/images/box-bg.gif", "wp-admin/images/box-butt-left.gif", "wp-admin/images/box-butt-right.gif", "wp-admin/images/box-butt.gif", "wp-admin/images/box-head-left.gif", "wp-admin/images/box-head-right.gif", "wp-admin/images/box-head.gif", "wp-admin/images/heading-bg.gif", "wp-admin/images/login-bkg-bottom.gif", "wp-admin/images/login-bkg-tile.gif", "wp-admin/images/notice.gif", "wp-admin/images/toggle.gif", "wp-admin/includes/upload.php", "wp-admin/js/dbx-admin-key.js", "wp-admin/js/link-cat.js", "wp-admin/profile-update.php", "wp-admin/templates.php", "wp-includes/images/wlw/WpComments.png", "wp-includes/images/wlw/WpIcon.png", "wp-includes/images/wlw/WpWatermark.png", "wp-includes/js/dbx.js", "wp-includes/js/fat.js", "wp-includes/js/list-manipulation.js", "wp-includes/js/tinymce/langs/en.js", "wp-includes/js/tinymce/plugins/autosave/editor_plugin_src.js", "wp-includes/js/tinymce/plugins/autosave/langs", "wp-includes/js/tinymce/plugins/directionality/images", "wp-includes/js/tinymce/plugins/directionality/langs", "wp-includes/js/tinymce/plugins/inlinepopups/css", "wp-includes/js/tinymce/plugins/inlinepopups/images", "wp-includes/js/tinymce/plugins/inlinepopups/jscripts", "wp-includes/js/tinymce/plugins/paste/images", "wp-includes/js/tinymce/plugins/paste/jscripts", "wp-includes/js/tinymce/plugins/paste/langs", "wp-includes/js/tinymce/plugins/spellchecker/classes/HttpClient.class.php", "wp-includes/js/tinymce/plugins/spellchecker/classes/TinyGoogleSpell.class.php", "wp-includes/js/tinymce/plugins/spellchecker/classes/TinyPspell.class.php", "wp-includes/js/tinymce/plugins/spellchecker/classes/TinyPspellShell.class.php", "wp-includes/js/tinymce/plugins/spellchecker/css/spellchecker.css", "wp-includes/js/tinymce/plugins/spellchecker/images", "wp-includes/js/tinymce/plugins/spellchecker/langs", "wp-includes/js/tinymce/plugins/spellchecker/tinyspell.php", "wp-includes/js/tinymce/plugins/wordpress/images", "wp-includes/js/tinymce/plugins/wordpress/langs", "wp-includes/js/tinymce/plugins/wordpress/wordpress.css", "wp-includes/js/tinymce/plugins/wphelp", "wp-includes/js/tinymce/themes/advanced/css", "wp-includes/js/tinymce/themes/advanced/images", "wp-includes/js/tinymce/themes/advanced/jscripts", "wp-includes/js/tinymce/themes/advanced/langs", "wp-includes/js/tinymce/tiny_mce_gzip.php", "wp-admin/bookmarklet.php", "wp-includes/js/jquery/jquery.dimensions.min.js", "wp-includes/js/tinymce/plugins/wordpress/popups.css", "wp-includes/js/wp-ajax.js", "wp-admin/css/press-this-ie-rtl.css", "wp-admin/css/press-this-ie.css", "wp-admin/css/upload-rtl.css", "wp-admin/edit-form.php", "wp-admin/images/comment-pill.gif", "wp-admin/images/comment-stalk-classic.gif", "wp-admin/images/comment-stalk-fresh.gif", "wp-admin/images/comment-stalk-rtl.gif", "wp-admin/images/del.png", "wp-admin/images/gear.png", "wp-admin/images/media-button-gallery.gif", "wp-admin/images/media-buttons.gif", "wp-admin/images/postbox-bg.gif", "wp-admin/images/tab.png", "wp-admin/images/tail.gif", "wp-admin/js/forms.js", "wp-admin/js/upload.js", "wp-admin/link-import.php", "wp-includes/images/audio.png", "wp-includes/images/css.png", "wp-includes/images/default.png", "wp-includes/images/doc.png", "wp-includes/images/exe.png", "wp-includes/images/html.png", "wp-includes/images/js.png", "wp-includes/images/pdf.png", "wp-includes/images/swf.png", "wp-includes/images/tar.png", "wp-includes/images/text.png", "wp-includes/images/video.png", "wp-includes/images/zip.png", "wp-includes/js/tinymce/tiny_mce_config.php", "wp-includes/js/tinymce/tiny_mce_ext.js", "wp-admin/js/users.js", "wp-includes/js/swfupload/plugins/swfupload.documentready.js", "wp-includes/js/swfupload/plugins/swfupload.graceful_degradation.js", "wp-includes/js/swfupload/swfupload_f9.swf", "wp-includes/js/tinymce/plugins/autosave", "wp-includes/js/tinymce/plugins/paste/css", "wp-includes/js/tinymce/utils/mclayer.js", "wp-includes/js/tinymce/wordpress.css", "wp-admin/import/btt.php", "wp-admin/import/jkw.php", "wp-admin/js/page.dev.js", "wp-admin/js/page.js", "wp-admin/js/set-post-thumbnail-handler.dev.js", "wp-admin/js/set-post-thumbnail-handler.js", "wp-admin/js/slug.dev.js", "wp-admin/js/slug.js", "wp-includes/gettext.php", "wp-includes/js/tinymce/plugins/wordpress/js", "wp-includes/streams.php", "README.txt", "htaccess.dist", "index-install.php", "wp-admin/css/mu-rtl.css", "wp-admin/css/mu.css", "wp-admin/images/site-admin.png", "wp-admin/includes/mu.php", "wp-admin/wpmu-admin.php", "wp-admin/wpmu-blogs.php", "wp-admin/wpmu-edit.php", "wp-admin/wpmu-options.php", "wp-admin/wpmu-themes.php", "wp-admin/wpmu-upgrade-site.php", "wp-admin/wpmu-users.php", "wp-includes/images/wordpress-mu.png", "wp-includes/wpmu-default-filters.php", "wp-includes/wpmu-functions.php", "wpmu-settings.php", "wp-admin/categories.php", "wp-admin/edit-category-form.php", "wp-admin/edit-page-form.php", "wp-admin/edit-pages.php", "wp-admin/images/admin-header-footer.png", "wp-admin/images/browse-happy.gif", "wp-admin/images/ico-add.png", "wp-admin/images/ico-close.png", "wp-admin/images/ico-edit.png", "wp-admin/images/ico-viewpage.png", "wp-admin/images/fav-top.png", "wp-admin/images/screen-options-left.gif", "wp-admin/images/wp-logo-vs.gif", "wp-admin/images/wp-logo.gif", "wp-admin/import", "wp-admin/js/wp-gears.dev.js", "wp-admin/js/wp-gears.js", "wp-admin/options-misc.php", "wp-admin/page-new.php", "wp-admin/page.php", "wp-admin/rtl.css", "wp-admin/rtl.dev.css", "wp-admin/update-links.php", "wp-admin/wp-admin.css", "wp-admin/wp-admin.dev.css", "wp-includes/js/codepress", "wp-includes/js/codepress/engines/khtml.js", "wp-includes/js/codepress/engines/older.js", "wp-includes/js/jquery/autocomplete.dev.js", "wp-includes/js/jquery/autocomplete.js", "wp-includes/js/jquery/interface.js", "wp-includes/js/scriptaculous/prototype.js", "wp-admin/edit-attachment-rows.php", "wp-admin/edit-link-categories.php", "wp-admin/edit-link-category-form.php", "wp-admin/edit-post-rows.php", "wp-admin/images/button-grad-active-vs.png", "wp-admin/images/button-grad-vs.png", "wp-admin/images/fav-arrow-vs-rtl.gif", "wp-admin/images/fav-arrow-vs.gif", "wp-admin/images/fav-top-vs.gif", "wp-admin/images/list-vs.png", "wp-admin/images/screen-options-right-up.gif", "wp-admin/images/screen-options-right.gif", "wp-admin/images/visit-site-button-grad-vs.gif", "wp-admin/images/visit-site-button-grad.gif", "wp-admin/link-category.php", "wp-admin/sidebar.php", "wp-includes/classes.php", "wp-includes/js/tinymce/blank.htm", "wp-includes/js/tinymce/plugins/media/css/content.css", "wp-includes/js/tinymce/plugins/media/img", "wp-includes/js/tinymce/plugins/safari", "wp-admin/images/logo-login.gif", "wp-admin/images/star.gif", "wp-admin/js/list-table.dev.js", "wp-admin/js/list-table.js", "wp-includes/default-embeds.php", "wp-includes/js/tinymce/plugins/wordpress/img/help.gif", "wp-includes/js/tinymce/plugins/wordpress/img/more.gif", "wp-includes/js/tinymce/plugins/wordpress/img/toolbars.gif", "wp-includes/js/tinymce/themes/advanced/img/fm.gif", "wp-includes/js/tinymce/themes/advanced/img/sflogo.png", "wp-admin/css/colors-classic-rtl.css", "wp-admin/css/colors-classic-rtl.dev.css", "wp-admin/css/colors-fresh-rtl.css", "wp-admin/css/colors-fresh-rtl.dev.css", "wp-admin/css/dashboard-rtl.dev.css", "wp-admin/css/dashboard.dev.css", "wp-admin/css/global-rtl.css", "wp-admin/css/global-rtl.dev.css", "wp-admin/css/global.css", "wp-admin/css/global.dev.css", "wp-admin/css/install-rtl.dev.css", "wp-admin/css/login-rtl.dev.css", "wp-admin/css/login.dev.css", "wp-admin/css/ms.css", "wp-admin/css/ms.dev.css", "wp-admin/css/nav-menu-rtl.css", "wp-admin/css/nav-menu-rtl.dev.css", "wp-admin/css/nav-menu.css", "wp-admin/css/nav-menu.dev.css", "wp-admin/css/plugin-install-rtl.css", "wp-admin/css/plugin-install-rtl.dev.css", "wp-admin/css/plugin-install.css", "wp-admin/css/plugin-install.dev.css", "wp-admin/css/press-this-rtl.dev.css", "wp-admin/css/press-this.dev.css", "wp-admin/css/theme-editor-rtl.css", "wp-admin/css/theme-editor-rtl.dev.css", "wp-admin/css/theme-editor.css", "wp-admin/css/theme-editor.dev.css", "wp-admin/css/theme-install-rtl.css", "wp-admin/css/theme-install-rtl.dev.css", "wp-admin/css/theme-install.css", "wp-admin/css/theme-install.dev.css", "wp-admin/css/widgets-rtl.dev.css", "wp-admin/css/widgets.dev.css", "wp-admin/includes/internal-linking.php", "wp-includes/images/admin-bar-sprite-rtl.png", "wp-includes/js/jquery/ui.button.js", "wp-includes/js/jquery/ui.core.js", "wp-includes/js/jquery/ui.dialog.js", "wp-includes/js/jquery/ui.draggable.js", "wp-includes/js/jquery/ui.droppable.js", "wp-includes/js/jquery/ui.mouse.js", "wp-includes/js/jquery/ui.position.js", "wp-includes/js/jquery/ui.resizable.js", "wp-includes/js/jquery/ui.selectable.js", "wp-includes/js/jquery/ui.sortable.js", "wp-includes/js/jquery/ui.tabs.js", "wp-includes/js/jquery/ui.widget.js", "wp-includes/js/l10n.dev.js", "wp-includes/js/l10n.js", "wp-includes/js/tinymce/plugins/wplink/css", "wp-includes/js/tinymce/plugins/wplink/img", "wp-includes/js/tinymce/plugins/wplink/js", "wp-includes/js/tinymce/themes/advanced/img/wpicons.png", "wp-includes/js/tinymce/themes/advanced/skins/wp_theme/img/butt2.png", "wp-includes/js/tinymce/themes/advanced/skins/wp_theme/img/button_bg.png", "wp-includes/js/tinymce/themes/advanced/skins/wp_theme/img/down_arrow.gif", "wp-includes/js/tinymce/themes/advanced/skins/wp_theme/img/fade-butt.png", "wp-includes/js/tinymce/themes/advanced/skins/wp_theme/img/separator.gif", "wp-admin/images/gray-star.png", "wp-admin/images/logo-login.png", "wp-admin/images/star.png", "wp-admin/index-extra.php", "wp-admin/network/index-extra.php", "wp-admin/user/index-extra.php", "wp-admin/images/screenshots/admin-flyouts.png", "wp-admin/images/screenshots/coediting.png", "wp-admin/images/screenshots/drag-and-drop.png", "wp-admin/images/screenshots/help-screen.png", "wp-admin/images/screenshots/media-icon.png", "wp-admin/images/screenshots/new-feature-pointer.png", "wp-admin/images/screenshots/welcome-screen.png", "wp-includes/css/editor-buttons.css", "wp-includes/css/editor-buttons.dev.css", "wp-includes/js/tinymce/plugins/paste/blank.htm", "wp-includes/js/tinymce/plugins/wordpress/css", "wp-includes/js/tinymce/plugins/wordpress/editor_plugin.dev.js", "wp-includes/js/tinymce/plugins/wordpress/img/embedded.png", "wp-includes/js/tinymce/plugins/wordpress/img/more_bug.gif", "wp-includes/js/tinymce/plugins/wordpress/img/page_bug.gif", "wp-includes/js/tinymce/plugins/wpdialogs/editor_plugin.dev.js", "wp-includes/js/tinymce/plugins/wpeditimage/css/editimage-rtl.css", "wp-includes/js/tinymce/plugins/wpeditimage/editor_plugin.dev.js", "wp-includes/js/tinymce/plugins/wpfullscreen/editor_plugin.dev.js", "wp-includes/js/tinymce/plugins/wpgallery/editor_plugin.dev.js", "wp-includes/js/tinymce/plugins/wpgallery/img/gallery.png", "wp-includes/js/tinymce/plugins/wplink/editor_plugin.dev.js", "wp-admin/gears-manifest.php", "wp-admin/includes/manifest.php", "wp-admin/images/archive-link.png", "wp-admin/images/blue-grad.png", "wp-admin/images/button-grad-active.png", "wp-admin/images/button-grad.png", "wp-admin/images/ed-bg-vs.gif", "wp-admin/images/ed-bg.gif", "wp-admin/images/fade-butt.png", "wp-admin/images/fav-arrow-rtl.gif", "wp-admin/images/fav-arrow.gif", "wp-admin/images/fav-vs.png", "wp-admin/images/fav.png", "wp-admin/images/gray-grad.png", "wp-admin/images/loading-publish.gif", "wp-admin/images/logo-ghost.png", "wp-admin/images/logo.gif", "wp-admin/images/menu-arrow-frame-rtl.png", "wp-admin/images/menu-arrow-frame.png", "wp-admin/images/menu-arrows.gif", "wp-admin/images/menu-bits-rtl-vs.gif", "wp-admin/images/menu-bits-rtl.gif", "wp-admin/images/menu-bits-vs.gif", "wp-admin/images/menu-bits.gif", "wp-admin/images/menu-dark-rtl-vs.gif", "wp-admin/images/menu-dark-rtl.gif", "wp-admin/images/menu-dark-vs.gif", "wp-admin/images/menu-dark.gif", "wp-admin/images/required.gif", "wp-admin/images/screen-options-toggle-vs.gif", "wp-admin/images/screen-options-toggle.gif", "wp-admin/images/toggle-arrow-rtl.gif", "wp-admin/images/toggle-arrow.gif", "wp-admin/images/upload-classic.png", "wp-admin/images/upload-fresh.png", "wp-admin/images/white-grad-active.png", "wp-admin/images/white-grad.png", "wp-admin/images/widgets-arrow-vs.gif", "wp-admin/images/widgets-arrow.gif", "wp-admin/images/wpspin_dark.gif", "wp-includes/images/upload.png", "wp-includes/js/prototype.js", "wp-includes/js/scriptaculous", "wp-admin/css/wp-admin-rtl.dev.css", "wp-admin/css/wp-admin.dev.css", "wp-admin/css/media-rtl.dev.css", "wp-admin/css/media.dev.css", "wp-admin/css/colors-classic.dev.css", "wp-admin/css/customize-controls-rtl.dev.css", "wp-admin/css/customize-controls.dev.css", "wp-admin/css/ie-rtl.dev.css", "wp-admin/css/ie.dev.css", "wp-admin/css/install.dev.css", "wp-admin/css/colors-fresh.dev.css", "wp-includes/js/customize-base.dev.js", "wp-includes/js/json2.dev.js", "wp-includes/js/comment-reply.dev.js", "wp-includes/js/customize-preview.dev.js", "wp-includes/js/wplink.dev.js", "wp-includes/js/tw-sack.dev.js", "wp-includes/js/wp-list-revisions.dev.js", "wp-includes/js/autosave.dev.js", "wp-includes/js/admin-bar.dev.js", "wp-includes/js/quicktags.dev.js", "wp-includes/js/wp-ajax-response.dev.js", "wp-includes/js/wp-pointer.dev.js", "wp-includes/js/hoverIntent.dev.js", "wp-includes/js/colorpicker.dev.js", "wp-includes/js/wp-lists.dev.js", "wp-includes/js/customize-loader.dev.js", "wp-includes/js/jquery/jquery.table-hotkeys.dev.js", "wp-includes/js/jquery/jquery.color.dev.js", "wp-includes/js/jquery/jquery.color.js", "wp-includes/js/jquery/jquery.hotkeys.dev.js", "wp-includes/js/jquery/jquery.form.dev.js", "wp-includes/js/jquery/suggest.dev.js", "wp-admin/js/xfn.dev.js", "wp-admin/js/set-post-thumbnail.dev.js", "wp-admin/js/comment.dev.js", "wp-admin/js/theme.dev.js", "wp-admin/js/cat.dev.js", "wp-admin/js/password-strength-meter.dev.js", "wp-admin/js/user-profile.dev.js", "wp-admin/js/theme-preview.dev.js", "wp-admin/js/post.dev.js", "wp-admin/js/media-upload.dev.js", "wp-admin/js/word-count.dev.js", "wp-admin/js/plugin-install.dev.js", "wp-admin/js/edit-comments.dev.js", "wp-admin/js/media-gallery.dev.js", "wp-admin/js/custom-fields.dev.js", "wp-admin/js/custom-background.dev.js", "wp-admin/js/common.dev.js", "wp-admin/js/inline-edit-tax.dev.js", "wp-admin/js/gallery.dev.js", "wp-admin/js/utils.dev.js", "wp-admin/js/widgets.dev.js", "wp-admin/js/wp-fullscreen.dev.js", "wp-admin/js/nav-menu.dev.js", "wp-admin/js/dashboard.dev.js", "wp-admin/js/link.dev.js", "wp-admin/js/user-suggest.dev.js", "wp-admin/js/postbox.dev.js", "wp-admin/js/tags.dev.js", "wp-admin/js/image-edit.dev.js", "wp-admin/js/media.dev.js", "wp-admin/js/customize-controls.dev.js", "wp-admin/js/inline-edit-post.dev.js", "wp-admin/js/categories.dev.js", "wp-admin/js/editor.dev.js", "wp-includes/js/tinymce/plugins/wpeditimage/js/editimage.dev.js", "wp-includes/js/tinymce/plugins/wpdialogs/js/popup.dev.js", "wp-includes/js/tinymce/plugins/wpdialogs/js/wpdialog.dev.js", "wp-includes/js/plupload/handlers.dev.js", "wp-includes/js/plupload/wp-plupload.dev.js", "wp-includes/js/swfupload/handlers.dev.js", "wp-includes/js/jcrop/jquery.Jcrop.dev.js", "wp-includes/js/jcrop/jquery.Jcrop.js", "wp-includes/js/jcrop/jquery.Jcrop.css", "wp-includes/js/imgareaselect/jquery.imgareaselect.dev.js", "wp-includes/css/wp-pointer.dev.css", "wp-includes/css/editor.dev.css", "wp-includes/css/jquery-ui-dialog.dev.css", "wp-includes/css/admin-bar-rtl.dev.css", "wp-includes/css/admin-bar.dev.css", "wp-includes/js/jquery/ui/jquery.effects.clip.min.js", "wp-includes/js/jquery/ui/jquery.effects.scale.min.js", "wp-includes/js/jquery/ui/jquery.effects.blind.min.js", "wp-includes/js/jquery/ui/jquery.effects.core.min.js", "wp-includes/js/jquery/ui/jquery.effects.shake.min.js", "wp-includes/js/jquery/ui/jquery.effects.fade.min.js", "wp-includes/js/jquery/ui/jquery.effects.explode.min.js", "wp-includes/js/jquery/ui/jquery.effects.slide.min.js", "wp-includes/js/jquery/ui/jquery.effects.drop.min.js", "wp-includes/js/jquery/ui/jquery.effects.highlight.min.js", "wp-includes/js/jquery/ui/jquery.effects.bounce.min.js", "wp-includes/js/jquery/ui/jquery.effects.pulsate.min.js", "wp-includes/js/jquery/ui/jquery.effects.transfer.min.js", "wp-includes/js/jquery/ui/jquery.effects.fold.min.js", "wp-admin/images/screenshots/captions-1.png", "wp-admin/images/screenshots/captions-2.png", "wp-admin/images/screenshots/flex-header-1.png", "wp-admin/images/screenshots/flex-header-2.png", "wp-admin/images/screenshots/flex-header-3.png", "wp-admin/images/screenshots/flex-header-media-library.png", "wp-admin/images/screenshots/theme-customizer.png", "wp-admin/images/screenshots/twitter-embed-1.png", "wp-admin/images/screenshots/twitter-embed-2.png", "wp-admin/js/utils.js", "wp-app.php", "wp-includes/class-wp-atom-server.php", "wp-includes/js/tinymce/themes/advanced/skins/wp_theme/ui.css", "wp-includes/js/swfupload/swfupload-all.js", "wp-admin/js/revisions-js.php", "wp-admin/images/screenshots", "wp-admin/js/categories.js", "wp-admin/js/categories.min.js", "wp-admin/js/custom-fields.js", "wp-admin/js/custom-fields.min.js", "wp-admin/js/cat.js", "wp-admin/js/cat.min.js", "wp-includes/js/tinymce/plugins/wpeditimage/js/editimage.min.js", "wp-includes/js/tinymce/themes/advanced/skins/wp_theme/img/page_bug.gif", "wp-includes/js/tinymce/themes/advanced/skins/wp_theme/img/more_bug.gif", "wp-includes/js/thickbox/tb-close-2x.png", "wp-includes/js/thickbox/tb-close.png", "wp-includes/images/wpmini-blue-2x.png", "wp-includes/images/wpmini-blue.png", "wp-admin/css/colors-fresh.css", "wp-admin/css/colors-classic.css", "wp-admin/css/colors-fresh.min.css", "wp-admin/css/colors-classic.min.css", "wp-admin/js/about.min.js", "wp-admin/js/about.js", "wp-admin/images/arrows-dark-vs-2x.png", "wp-admin/images/wp-logo-vs.png", "wp-admin/images/arrows-dark-vs.png", "wp-admin/images/wp-logo.png", "wp-admin/images/arrows-pr.png", "wp-admin/images/arrows-dark.png", "wp-admin/images/press-this.png", "wp-admin/images/press-this-2x.png", "wp-admin/images/arrows-vs-2x.png", "wp-admin/images/welcome-icons.png", "wp-admin/images/wp-logo-2x.png", "wp-admin/images/stars-rtl-2x.png", "wp-admin/images/arrows-dark-2x.png", "wp-admin/images/arrows-pr-2x.png", "wp-admin/images/menu-shadow-rtl.png", "wp-admin/images/arrows-vs.png", "wp-admin/images/about-search-2x.png", "wp-admin/images/bubble_bg-rtl-2x.gif", "wp-admin/images/wp-badge-2x.png", "wp-admin/images/wordpress-logo-2x.png", "wp-admin/images/bubble_bg-rtl.gif", "wp-admin/images/wp-badge.png", "wp-admin/images/menu-shadow.png", "wp-admin/images/about-globe-2x.png", "wp-admin/images/welcome-icons-2x.png", "wp-admin/images/stars-rtl.png", "wp-admin/images/wp-logo-vs-2x.png", "wp-admin/images/about-updates-2x.png", "wp-admin/css/colors.css", "wp-admin/css/colors.min.css", "wp-admin/css/colors-rtl.css", "wp-admin/css/colors-rtl.min.css", "wp-admin/images/lock-2x.png", "wp-admin/images/lock.png", "wp-admin/js/theme-preview.js", "wp-admin/js/theme-install.min.js", "wp-admin/js/theme-install.js", "wp-admin/js/theme-preview.min.js", "wp-includes/js/plupload/plupload.html4.js", "wp-includes/js/plupload/plupload.html5.js", "wp-includes/js/plupload/changelog.txt", "wp-includes/js/plupload/plupload.silverlight.js", "wp-includes/js/plupload/plupload.flash.js", "wp-includes/js/tinymce/plugins/spellchecker", "wp-includes/js/tinymce/plugins/inlinepopups", "wp-includes/js/tinymce/plugins/media/js", "wp-includes/js/tinymce/plugins/media/css", "wp-includes/js/tinymce/plugins/wordpress/img", "wp-includes/js/tinymce/plugins/wpdialogs/js", "wp-includes/js/tinymce/plugins/wpeditimage/img", "wp-includes/js/tinymce/plugins/wpeditimage/js", "wp-includes/js/tinymce/plugins/wpeditimage/css", "wp-includes/js/tinymce/plugins/wpgallery/img", "wp-includes/js/tinymce/plugins/wpfullscreen/css", "wp-includes/js/tinymce/plugins/paste/js", "wp-includes/js/tinymce/themes/advanced", "wp-includes/js/tinymce/tiny_mce.js", "wp-includes/js/tinymce/mark_loaded_src.js", "wp-includes/js/tinymce/wp-tinymce-schema.js", "wp-includes/js/tinymce/plugins/media/editor_plugin.js", "wp-includes/js/tinymce/plugins/media/editor_plugin_src.js", "wp-includes/js/tinymce/plugins/media/media.htm", "wp-includes/js/tinymce/plugins/wpview/editor_plugin_src.js", "wp-includes/js/tinymce/plugins/wpview/editor_plugin.js", "wp-includes/js/tinymce/plugins/directionality/editor_plugin.js", "wp-includes/js/tinymce/plugins/directionality/editor_plugin_src.js", "wp-includes/js/tinymce/plugins/wordpress/editor_plugin.js", "wp-includes/js/tinymce/plugins/wordpress/editor_plugin_src.js", "wp-includes/js/tinymce/plugins/wpdialogs/editor_plugin_src.js", "wp-includes/js/tinymce/plugins/wpdialogs/editor_plugin.js", "wp-includes/js/tinymce/plugins/wpeditimage/editimage.html", "wp-includes/js/tinymce/plugins/wpeditimage/editor_plugin.js", "wp-includes/js/tinymce/plugins/wpeditimage/editor_plugin_src.js", "wp-includes/js/tinymce/plugins/fullscreen/editor_plugin_src.js", "wp-includes/js/tinymce/plugins/fullscreen/fullscreen.htm", "wp-includes/js/tinymce/plugins/fullscreen/editor_plugin.js", "wp-includes/js/tinymce/plugins/wplink/editor_plugin_src.js", "wp-includes/js/tinymce/plugins/wplink/editor_plugin.js", "wp-includes/js/tinymce/plugins/wpgallery/editor_plugin_src.js", "wp-includes/js/tinymce/plugins/wpgallery/editor_plugin.js", "wp-includes/js/tinymce/plugins/tabfocus/editor_plugin.js", "wp-includes/js/tinymce/plugins/tabfocus/editor_plugin_src.js", "wp-includes/js/tinymce/plugins/wpfullscreen/editor_plugin.js", "wp-includes/js/tinymce/plugins/wpfullscreen/editor_plugin_src.js", "wp-includes/js/tinymce/plugins/paste/editor_plugin.js", "wp-includes/js/tinymce/plugins/paste/pasteword.htm", "wp-includes/js/tinymce/plugins/paste/editor_plugin_src.js", "wp-includes/js/tinymce/plugins/paste/pastetext.htm", "wp-includes/js/tinymce/langs/wp-langs.php", "wp-includes/js/jquery/ui/jquery.ui.accordion.min.js", "wp-includes/js/jquery/ui/jquery.ui.autocomplete.min.js", "wp-includes/js/jquery/ui/jquery.ui.button.min.js", "wp-includes/js/jquery/ui/jquery.ui.core.min.js", "wp-includes/js/jquery/ui/jquery.ui.datepicker.min.js", "wp-includes/js/jquery/ui/jquery.ui.dialog.min.js", "wp-includes/js/jquery/ui/jquery.ui.draggable.min.js", "wp-includes/js/jquery/ui/jquery.ui.droppable.min.js", "wp-includes/js/jquery/ui/jquery.ui.effect-blind.min.js", "wp-includes/js/jquery/ui/jquery.ui.effect-bounce.min.js", "wp-includes/js/jquery/ui/jquery.ui.effect-clip.min.js", "wp-includes/js/jquery/ui/jquery.ui.effect-drop.min.js", "wp-includes/js/jquery/ui/jquery.ui.effect-explode.min.js", "wp-includes/js/jquery/ui/jquery.ui.effect-fade.min.js", "wp-includes/js/jquery/ui/jquery.ui.effect-fold.min.js", "wp-includes/js/jquery/ui/jquery.ui.effect-highlight.min.js", "wp-includes/js/jquery/ui/jquery.ui.effect-pulsate.min.js", "wp-includes/js/jquery/ui/jquery.ui.effect-scale.min.js", "wp-includes/js/jquery/ui/jquery.ui.effect-shake.min.js", "wp-includes/js/jquery/ui/jquery.ui.effect-slide.min.js", "wp-includes/js/jquery/ui/jquery.ui.effect-transfer.min.js", "wp-includes/js/jquery/ui/jquery.ui.effect.min.js", "wp-includes/js/jquery/ui/jquery.ui.menu.min.js", "wp-includes/js/jquery/ui/jquery.ui.mouse.min.js", "wp-includes/js/jquery/ui/jquery.ui.position.min.js", "wp-includes/js/jquery/ui/jquery.ui.progressbar.min.js", "wp-includes/js/jquery/ui/jquery.ui.resizable.min.js", "wp-includes/js/jquery/ui/jquery.ui.selectable.min.js", "wp-includes/js/jquery/ui/jquery.ui.slider.min.js", "wp-includes/js/jquery/ui/jquery.ui.sortable.min.js", "wp-includes/js/jquery/ui/jquery.ui.spinner.min.js", "wp-includes/js/jquery/ui/jquery.ui.tabs.min.js", "wp-includes/js/jquery/ui/jquery.ui.tooltip.min.js", "wp-includes/js/jquery/ui/jquery.ui.widget.min.js", "wp-includes/js/tinymce/skins/wordpress/images/dashicon-no-alt.png", "wp-admin/js/wp-fullscreen.js", "wp-admin/js/wp-fullscreen.min.js", "wp-includes/js/tinymce/wp-mce-help.php", "wp-includes/js/tinymce/plugins/wpfullscreen", "wp-includes/theme-compat/comments-popup.php", "wp-admin/includes/class-wp-automatic-upgrader.php", "wp-includes/js/tinymce/plugins/wpembed", "wp-includes/js/tinymce/plugins/media/moxieplayer.swf", "wp-includes/js/tinymce/skins/lightgray/fonts/readme.md", "wp-includes/js/tinymce/skins/lightgray/fonts/tinymce-small.json", "wp-includes/js/tinymce/skins/lightgray/fonts/tinymce.json", "wp-includes/js/tinymce/skins/lightgray/skin.ie7.min.css", "wp-admin/css/press-this-editor-rtl.css", "wp-admin/css/press-this-editor-rtl.min.css", "wp-admin/css/press-this-editor.css", "wp-admin/css/press-this-editor.min.css", "wp-admin/css/press-this-rtl.css", "wp-admin/css/press-this-rtl.min.css", "wp-admin/css/press-this.css", "wp-admin/css/press-this.min.css", "wp-admin/includes/class-wp-press-this.php", "wp-admin/js/bookmarklet.js", "wp-admin/js/bookmarklet.min.js", "wp-admin/js/press-this.js", "wp-admin/js/press-this.min.js", "wp-includes/js/mediaelement/background.png", "wp-includes/js/mediaelement/bigplay.png", "wp-includes/js/mediaelement/bigplay.svg", "wp-includes/js/mediaelement/controls.png", "wp-includes/js/mediaelement/controls.svg", "wp-includes/js/mediaelement/flashmediaelement.swf", "wp-includes/js/mediaelement/froogaloop.min.js", "wp-includes/js/mediaelement/jumpforward.png", "wp-includes/js/mediaelement/loading.gif", "wp-includes/js/mediaelement/silverlightmediaelement.xap", "wp-includes/js/mediaelement/skipback.png", "wp-includes/js/plupload/plupload.flash.swf", "wp-includes/js/plupload/plupload.full.min.js", "wp-includes/js/plupload/plupload.silverlight.xap", "wp-includes/js/swfupload/plugins", "wp-includes/js/swfupload/swfupload.swf", "wp-includes/js/mediaelement/lang", "wp-includes/js/mediaelement/lang/ca.js", "wp-includes/js/mediaelement/lang/cs.js", "wp-includes/js/mediaelement/lang/de.js", "wp-includes/js/mediaelement/lang/es.js", "wp-includes/js/mediaelement/lang/fa.js", "wp-includes/js/mediaelement/lang/fr.js", "wp-includes/js/mediaelement/lang/hr.js", "wp-includes/js/mediaelement/lang/hu.js", "wp-includes/js/mediaelement/lang/it.js", "wp-includes/js/mediaelement/lang/ja.js", "wp-includes/js/mediaelement/lang/ko.js", "wp-includes/js/mediaelement/lang/nl.js", "wp-includes/js/mediaelement/lang/pl.js", "wp-includes/js/mediaelement/lang/pt.js", "wp-includes/js/mediaelement/lang/ro.js", "wp-includes/js/mediaelement/lang/ru.js", "wp-includes/js/mediaelement/lang/sk.js", "wp-includes/js/mediaelement/lang/sv.js", "wp-includes/js/mediaelement/lang/uk.js", "wp-includes/js/mediaelement/lang/zh-cn.js", "wp-includes/js/mediaelement/lang/zh.js", "wp-includes/js/mediaelement/mediaelement-flash-audio-ogg.swf", "wp-includes/js/mediaelement/mediaelement-flash-audio.swf", "wp-includes/js/mediaelement/mediaelement-flash-video-hls.swf", "wp-includes/js/mediaelement/mediaelement-flash-video-mdash.swf", "wp-includes/js/mediaelement/mediaelement-flash-video.swf", "wp-includes/js/mediaelement/renderers/dailymotion.js", "wp-includes/js/mediaelement/renderers/dailymotion.min.js", "wp-includes/js/mediaelement/renderers/facebook.js", "wp-includes/js/mediaelement/renderers/facebook.min.js", "wp-includes/js/mediaelement/renderers/soundcloud.js", "wp-includes/js/mediaelement/renderers/soundcloud.min.js", "wp-includes/js/mediaelement/renderers/twitch.js", "wp-includes/js/mediaelement/renderers/twitch.min.js", "wp-includes/js/codemirror/jshint.js", "wp-includes/random_compat/random_bytes_openssl.php", "wp-includes/js/tinymce/wp-tinymce.js.gz", "wp-includes/js/wp-a11y.js", "wp-includes/js/wp-a11y.min.js", "wp-admin/js/wp-fullscreen-stub.js", "wp-admin/js/wp-fullscreen-stub.min.js")
#// 
#// Stores new files in wp-content to copy
#// 
#// The contents of this array indicate any new bundled plugins/themes which
#// should be installed with the WordPress Upgrade. These items will not be
#// re-installed in future upgrades, this behaviour is controlled by the
#// introduced version present here being older than the current installed version.
#// 
#// The content of this array should follow the following format:
#// Filename (relative to wp-content) => Introduced version
#// Directories should be noted by suffixing it with a trailing slash (/)
#// 
#// @since 3.2.0
#// @since 4.7.0 New themes were not automatically installed for 4.4-4.6 on
#// upgrade. New themes are now installed again. To disable new
#// themes from being installed on upgrade, explicitly define
#// CORE_UPGRADE_SKIP_NEW_BUNDLED as true.
#// @global array $_new_bundled_files
#// @var array
#// @name $_new_bundled_files
#//
global _new_bundled_files_
php_check_if_defined("_new_bundled_files_")
_new_bundled_files_ = Array({"plugins/akismet/": "2.0", "themes/twentyten/": "3.0", "themes/twentyeleven/": "3.2", "themes/twentytwelve/": "3.5", "themes/twentythirteen/": "3.6", "themes/twentyfourteen/": "3.8", "themes/twentyfifteen/": "4.1", "themes/twentysixteen/": "4.4", "themes/twentyseventeen/": "4.7", "themes/twentynineteen/": "5.0", "themes/twentytwenty/": "5.3"})
#// 
#// Upgrades the core of WordPress.
#// 
#// This will create a .maintenance file at the base of the WordPress directory
#// to ensure that people can not access the web site, when the files are being
#// copied to their locations.
#// 
#// The files in the `$_old_files` list will be removed and the new files
#// copied from the zip file after the database is upgraded.
#// 
#// The files in the `$_new_bundled_files` list will be added to the installation
#// if the version is greater than or equal to the old version being upgraded.
#// 
#// The steps for the upgrader for after the new release is downloaded and
#// unzipped is:
#// 1. Test unzipped location for select files to ensure that unzipped worked.
#// 2. Create the .maintenance file in current WordPress base.
#// 3. Copy new WordPress directory over old WordPress files.
#// 4. Upgrade WordPress to new version.
#// 4.1. Copy all files/folders other than wp-content
#// 4.2. Copy any language files to WP_LANG_DIR (which may differ from WP_CONTENT_DIR
#// 4.3. Copy any new bundled themes/plugins to their respective locations
#// 5. Delete new WordPress directory path.
#// 6. Delete .maintenance file.
#// 7. Remove old files.
#// 8. Delete 'update_core' option.
#// 
#// There are several areas of failure. For instance if PHP times out before step
#// 6, then you will not be able to access any portion of your site. Also, since
#// the upgrade will not continue where it left off, you will not be able to
#// automatically remove old files and remove the 'update_core' option. This
#// isn't that bad.
#// 
#// If the copy of the new WordPress over the old fails, then the worse is that
#// the new WordPress directory will remain.
#// 
#// If it is assumed that every file will be copied over, including plugins and
#// themes, then if you edit the default theme, you should rename it, so that
#// your changes remain.
#// 
#// @since 2.7.0
#// 
#// @global WP_Filesystem_Base $wp_filesystem          WordPress filesystem subclass.
#// @global array              $_old_files
#// @global array              $_new_bundled_files
#// @global wpdb               $wpdb                   WordPress database abstraction object.
#// @global string             $wp_version
#// @global string             $required_php_version
#// @global string             $required_mysql_version
#// 
#// @param string $from New release unzipped path.
#// @param string $to   Path to old WordPress installation.
#// @return string|WP_Error New WordPress version on success, WP_Error on failure.
#//
def update_core(from_=None, to_=None, *_args_):
    
    
    global wp_filesystem_
    global _old_files_
    global _new_bundled_files_
    global wpdb_
    php_check_if_defined("wp_filesystem_","_old_files_","_new_bundled_files_","wpdb_")
    set_time_limit(300)
    #// 
    #// Filters feedback messages displayed during the core update process.
    #// 
    #// The filter is first evaluated after the zip file for the latest version
    #// has been downloaded and unzipped. It is evaluated five more times during
    #// the process:
    #// 
    #// 1. Before WordPress begins the core upgrade process.
    #// 2. Before Maintenance Mode is enabled.
    #// 3. Before WordPress begins copying over the necessary files.
    #// 4. Before Maintenance Mode is disabled.
    #// 5. Before the database is upgraded.
    #// 
    #// @since 2.5.0
    #// 
    #// @param string $feedback The core update feedback messages.
    #//
    apply_filters("update_feedback", __("Verifying the unpacked files&#8230;"))
    #// Sanity check the unzipped distribution.
    distro_ = ""
    roots_ = Array("/wordpress/", "/wordpress-mu/")
    for root_ in roots_:
        if wp_filesystem_.exists(from_ + root_ + "readme.html") and wp_filesystem_.exists(from_ + root_ + "wp-includes/version.php"):
            distro_ = root_
            break
        # end if
    # end for
    if (not distro_):
        wp_filesystem_.delete(from_, True)
        return php_new_class("WP_Error", lambda : WP_Error("insane_distro", __("The update could not be unpacked")))
    # end if
    #// 
    #// Import $wp_version, $required_php_version, and $required_mysql_version from the new version.
    #// DO NOT globalise any variables imported from `version-current.php` in this function.
    #// 
    #// BC Note: $wp_filesystem->wp_content_dir() returned unslashed pre-2.8
    #//
    versions_file_ = trailingslashit(wp_filesystem_.wp_content_dir()) + "upgrade/version-current.php"
    if (not wp_filesystem_.copy(from_ + distro_ + "wp-includes/version.php", versions_file_)):
        wp_filesystem_.delete(from_, True)
        return php_new_class("WP_Error", lambda : WP_Error("copy_failed_for_version_file", __("The update cannot be installed because we will be unable to copy some files. This is usually due to inconsistent file permissions."), "wp-includes/version.php"))
    # end if
    wp_filesystem_.chmod(versions_file_, FS_CHMOD_FILE)
    php_include_file(WP_CONTENT_DIR + "/upgrade/version-current.php", once=False)
    wp_filesystem_.delete(versions_file_)
    php_version_ = php_phpversion()
    mysql_version_ = wpdb_.db_version()
    old_wp_version_ = PHP_GLOBALS["wp_version"]
    #// The version of WordPress we're updating from.
    development_build_ = False != php_strpos(old_wp_version_ + wp_version_, "-")
    #// A dash in the version indicates a development release.
    php_compat_ = php_version_compare(php_version_, required_php_version_, ">=")
    if php_file_exists(WP_CONTENT_DIR + "/db.php") and php_empty(lambda : wpdb_.is_mysql):
        mysql_compat_ = True
    else:
        mysql_compat_ = php_version_compare(mysql_version_, required_mysql_version_, ">=")
    # end if
    if (not mysql_compat_) or (not php_compat_):
        wp_filesystem_.delete(from_, True)
    # end if
    php_update_message_ = ""
    if php_function_exists("wp_get_update_php_url"):
        #// translators: %s: URL to Update PHP page.
        php_update_message_ = "</p><p>" + php_sprintf(__("<a href=\"%s\">Learn more about updating PHP</a>."), esc_url(wp_get_update_php_url()))
        if php_function_exists("wp_get_update_php_annotation"):
            annotation_ = wp_get_update_php_annotation()
            if annotation_:
                php_update_message_ += "</p><p><em>" + annotation_ + "</em>"
            # end if
        # end if
    # end if
    if (not mysql_compat_) and (not php_compat_):
        return php_new_class("WP_Error", lambda : WP_Error("php_mysql_not_compatible", php_sprintf(__("The update cannot be installed because WordPress %1$s requires PHP version %2$s or higher and MySQL version %3$s or higher. You are running PHP version %4$s and MySQL version %5$s."), wp_version_, required_php_version_, required_mysql_version_, php_version_, mysql_version_) + php_update_message_))
    elif (not php_compat_):
        return php_new_class("WP_Error", lambda : WP_Error("php_not_compatible", php_sprintf(__("The update cannot be installed because WordPress %1$s requires PHP version %2$s or higher. You are running version %3$s."), wp_version_, required_php_version_, php_version_) + php_update_message_))
    elif (not mysql_compat_):
        return php_new_class("WP_Error", lambda : WP_Error("mysql_not_compatible", php_sprintf(__("The update cannot be installed because WordPress %1$s requires MySQL version %2$s or higher. You are running version %3$s."), wp_version_, required_mysql_version_, mysql_version_)))
    # end if
    #// Add a warning when the JSON PHP extension is missing.
    if (not php_extension_loaded("json")):
        return php_new_class("WP_Error", lambda : WP_Error("php_not_compatible_json", php_sprintf(__("The update cannot be installed because WordPress %1$s requires the %2$s PHP extension."), wp_version_, "JSON")))
    # end if
    #// This filter is documented in wp-admin/includes/update-core.php
    apply_filters("update_feedback", __("Preparing to install the latest version&#8230;"))
    #// Don't copy wp-content, we'll deal with that below.
    #// We also copy version.php last so failed updates report their old version.
    skip_ = Array("wp-content", "wp-includes/version.php")
    check_is_writable_ = Array()
    #// Check to see which files don't really need updating - only available for 3.7 and higher.
    if php_function_exists("get_core_checksums"):
        #// Find the local version of the working directory.
        working_dir_local_ = WP_CONTENT_DIR + "/upgrade/" + php_basename(from_) + distro_
        checksums_ = get_core_checksums(wp_version_, wp_local_package_ if (php_isset(lambda : wp_local_package_)) else "en_US")
        if php_is_array(checksums_) and (php_isset(lambda : checksums_[wp_version_])):
            checksums_ = checksums_[wp_version_]
            pass
        # end if
        if php_is_array(checksums_):
            for file_,checksum_ in checksums_.items():
                if "wp-content" == php_substr(file_, 0, 10):
                    continue
                # end if
                if (not php_file_exists(ABSPATH + file_)):
                    continue
                # end if
                if (not php_file_exists(working_dir_local_ + file_)):
                    continue
                # end if
                if "." == php_dirname(file_) and php_in_array(pathinfo(file_, PATHINFO_EXTENSION), Array("html", "txt")):
                    continue
                # end if
                if php_md5_file(ABSPATH + file_) == checksum_:
                    skip_[-1] = file_
                else:
                    check_is_writable_[file_] = ABSPATH + file_
                # end if
            # end for
        # end if
    # end if
    #// If we're using the direct method, we can predict write failures that are due to permissions.
    if check_is_writable_ and "direct" == wp_filesystem_.method:
        files_writable_ = php_array_filter(check_is_writable_, Array(wp_filesystem_, "is_writable"))
        if files_writable_ != check_is_writable_:
            files_not_writable_ = php_array_diff_key(check_is_writable_, files_writable_)
            for relative_file_not_writable_,file_not_writable_ in files_not_writable_.items():
                #// If the writable check failed, chmod file to 0644 and try again, same as copy_dir().
                wp_filesystem_.chmod(file_not_writable_, FS_CHMOD_FILE)
                if wp_filesystem_.is_writable(file_not_writable_):
                    files_not_writable_[relative_file_not_writable_] = None
                # end if
            # end for
            #// Store package-relative paths (the key) of non-writable files in the WP_Error object.
            error_data_ = php_array_keys(files_not_writable_) if php_version_compare(old_wp_version_, "3.7-beta2", ">") else ""
            if files_not_writable_:
                return php_new_class("WP_Error", lambda : WP_Error("files_not_writable", __("The update cannot be installed because we will be unable to copy some files. This is usually due to inconsistent file permissions."), php_implode(", ", error_data_)))
            # end if
        # end if
    # end if
    #// This filter is documented in wp-admin/includes/update-core.php
    apply_filters("update_feedback", __("Enabling Maintenance mode&#8230;"))
    #// Create maintenance file to signal that we are upgrading.
    maintenance_string_ = "<?php $upgrading = " + time() + "; ?>"
    maintenance_file_ = to_ + ".maintenance"
    wp_filesystem_.delete(maintenance_file_)
    wp_filesystem_.put_contents(maintenance_file_, maintenance_string_, FS_CHMOD_FILE)
    #// This filter is documented in wp-admin/includes/update-core.php
    apply_filters("update_feedback", __("Copying the required files&#8230;"))
    #// Copy new versions of WP files into place.
    result_ = _copy_dir(from_ + distro_, to_, skip_)
    if is_wp_error(result_):
        result_ = php_new_class("WP_Error", lambda : WP_Error(result_.get_error_code(), result_.get_error_message(), php_substr(result_.get_error_data(), php_strlen(to_))))
    # end if
    #// Since we know the core files have copied over, we can now copy the version file.
    if (not is_wp_error(result_)):
        if (not wp_filesystem_.copy(from_ + distro_ + "wp-includes/version.php", to_ + "wp-includes/version.php", True)):
            wp_filesystem_.delete(from_, True)
            result_ = php_new_class("WP_Error", lambda : WP_Error("copy_failed_for_version_file", __("The update cannot be installed because we will be unable to copy some files. This is usually due to inconsistent file permissions."), "wp-includes/version.php"))
        # end if
        wp_filesystem_.chmod(to_ + "wp-includes/version.php", FS_CHMOD_FILE)
    # end if
    #// Check to make sure everything copied correctly, ignoring the contents of wp-content.
    skip_ = Array("wp-content")
    failed_ = Array()
    if (php_isset(lambda : checksums_)) and php_is_array(checksums_):
        for file_,checksum_ in checksums_.items():
            if "wp-content" == php_substr(file_, 0, 10):
                continue
            # end if
            if (not php_file_exists(working_dir_local_ + file_)):
                continue
            # end if
            if "." == php_dirname(file_) and php_in_array(pathinfo(file_, PATHINFO_EXTENSION), Array("html", "txt")):
                skip_[-1] = file_
                continue
            # end if
            if php_file_exists(ABSPATH + file_) and php_md5_file(ABSPATH + file_) == checksum_:
                skip_[-1] = file_
            else:
                failed_[-1] = file_
            # end if
        # end for
    # end if
    #// Some files didn't copy properly.
    if (not php_empty(lambda : failed_)):
        total_size_ = 0
        for file_ in failed_:
            if php_file_exists(working_dir_local_ + file_):
                total_size_ += filesize(working_dir_local_ + file_)
            # end if
        # end for
        #// If we don't have enough free space, it isn't worth trying again.
        #// Unlikely to be hit due to the check in unzip_file().
        available_space_ = php_no_error(lambda: disk_free_space(ABSPATH))
        if available_space_ and total_size_ >= available_space_:
            result_ = php_new_class("WP_Error", lambda : WP_Error("disk_full", __("There is not enough free disk space to complete the update.")))
        else:
            result_ = _copy_dir(from_ + distro_, to_, skip_)
            if is_wp_error(result_):
                result_ = php_new_class("WP_Error", lambda : WP_Error(result_.get_error_code() + "_retry", result_.get_error_message(), php_substr(result_.get_error_data(), php_strlen(to_))))
            # end if
        # end if
    # end if
    #// Custom content directory needs updating now.
    #// Copy languages.
    if (not is_wp_error(result_)) and wp_filesystem_.is_dir(from_ + distro_ + "wp-content/languages"):
        if WP_LANG_DIR != ABSPATH + WPINC + "/languages" or php_no_error(lambda: php_is_dir(WP_LANG_DIR)):
            lang_dir_ = WP_LANG_DIR
        else:
            lang_dir_ = WP_CONTENT_DIR + "/languages"
        # end if
        #// Check if the language directory exists first.
        if (not php_no_error(lambda: php_is_dir(lang_dir_))) and 0 == php_strpos(lang_dir_, ABSPATH):
            #// If it's within the ABSPATH we can handle it here, otherwise they're out of luck.
            wp_filesystem_.mkdir(to_ + php_str_replace(ABSPATH, "", lang_dir_), FS_CHMOD_DIR)
            clearstatcache()
            pass
        # end if
        if php_no_error(lambda: php_is_dir(lang_dir_)):
            wp_lang_dir_ = wp_filesystem_.find_folder(lang_dir_)
            if wp_lang_dir_:
                result_ = copy_dir(from_ + distro_ + "wp-content/languages/", wp_lang_dir_)
                if is_wp_error(result_):
                    result_ = php_new_class("WP_Error", lambda : WP_Error(result_.get_error_code() + "_languages", result_.get_error_message(), php_substr(result_.get_error_data(), php_strlen(wp_lang_dir_))))
                # end if
            # end if
        # end if
    # end if
    #// This filter is documented in wp-admin/includes/update-core.php
    apply_filters("update_feedback", __("Disabling Maintenance mode&#8230;"))
    #// Remove maintenance file, we're done with potential site-breaking changes.
    wp_filesystem_.delete(maintenance_file_)
    #// 3.5 -> 3.5+ - an empty twentytwelve directory was created upon upgrade to 3.5 for some users, preventing installation of Twenty Twelve.
    if "3.5" == old_wp_version_:
        if php_is_dir(WP_CONTENT_DIR + "/themes/twentytwelve") and (not php_file_exists(WP_CONTENT_DIR + "/themes/twentytwelve/style.css")):
            wp_filesystem_.delete(wp_filesystem_.wp_themes_dir() + "twentytwelve/")
        # end if
    # end if
    #// 
    #// Copy new bundled plugins & themes.
    #// This gives us the ability to install new plugins & themes bundled with
    #// future versions of WordPress whilst avoiding the re-install upon upgrade issue.
    #// $development_build controls us overwriting bundled themes and plugins when a non-stable release is being updated.
    #//
    if (not is_wp_error(result_)) and (not php_defined("CORE_UPGRADE_SKIP_NEW_BUNDLED")) or (not CORE_UPGRADE_SKIP_NEW_BUNDLED):
        for file_,introduced_version_ in _new_bundled_files_.items():
            #// If a $development_build or if $introduced version is greater than what the site was previously running.
            if development_build_ or php_version_compare(introduced_version_, old_wp_version_, ">"):
                directory_ = "/" == file_[php_strlen(file_) - 1]
                type_, filename_ = php_explode("/", file_, 2)
                #// Check to see if the bundled items exist before attempting to copy them.
                if (not wp_filesystem_.exists(from_ + distro_ + "wp-content/" + file_)):
                    continue
                # end if
                if "plugins" == type_:
                    dest_ = wp_filesystem_.wp_plugins_dir()
                elif "themes" == type_:
                    #// Back-compat, ::wp_themes_dir() did not return trailingslash'd pre-3.2.
                    dest_ = trailingslashit(wp_filesystem_.wp_themes_dir())
                else:
                    continue
                # end if
                if (not directory_):
                    if (not development_build_) and wp_filesystem_.exists(dest_ + filename_):
                        continue
                    # end if
                    if (not wp_filesystem_.copy(from_ + distro_ + "wp-content/" + file_, dest_ + filename_, FS_CHMOD_FILE)):
                        result_ = php_new_class("WP_Error", lambda : WP_Error(str("copy_failed_for_new_bundled_") + str(type_), __("Could not copy file."), dest_ + filename_))
                    # end if
                else:
                    if (not development_build_) and wp_filesystem_.is_dir(dest_ + filename_):
                        continue
                    # end if
                    wp_filesystem_.mkdir(dest_ + filename_, FS_CHMOD_DIR)
                    _result_ = copy_dir(from_ + distro_ + "wp-content/" + file_, dest_ + filename_)
                    #// If a error occurs partway through this final step, keep the error flowing through, but keep process going.
                    if is_wp_error(_result_):
                        if (not is_wp_error(result_)):
                            result_ = php_new_class("WP_Error", lambda : WP_Error())
                        # end if
                        result_.add(_result_.get_error_code() + str("_") + str(type_), _result_.get_error_message(), php_substr(_result_.get_error_data(), php_strlen(dest_)))
                    # end if
                # end if
            # end if
        # end for
        pass
    # end if
    #// Handle $result error from the above blocks.
    if is_wp_error(result_):
        wp_filesystem_.delete(from_, True)
        return result_
    # end if
    #// Remove old files.
    for old_file_ in _old_files_:
        old_file_ = to_ + old_file_
        if (not wp_filesystem_.exists(old_file_)):
            continue
        # end if
        #// If the file isn't deleted, try writing an empty string to the file instead.
        if (not wp_filesystem_.delete(old_file_, True)) and wp_filesystem_.is_file(old_file_):
            wp_filesystem_.put_contents(old_file_, "")
        # end if
    # end for
    #// Remove any Genericons example.html's from the filesystem.
    _upgrade_422_remove_genericons()
    #// Remove the REST API plugin if its version is Beta 4 or lower.
    _upgrade_440_force_deactivate_incompatible_plugins()
    #// Upgrade DB with separate request.
    #// This filter is documented in wp-admin/includes/update-core.php
    apply_filters("update_feedback", __("Upgrading database&#8230;"))
    db_upgrade_url_ = admin_url("upgrade.php?step=upgrade_db")
    wp_remote_post(db_upgrade_url_, Array({"timeout": 60}))
    #// Clear the cache to prevent an update_option() from saving a stale db_version to the cache.
    wp_cache_flush()
    #// Not all cache back ends listen to 'flush'.
    wp_cache_delete("alloptions", "options")
    #// Remove working directory.
    wp_filesystem_.delete(from_, True)
    #// Force refresh of update information.
    if php_function_exists("delete_site_transient"):
        delete_site_transient("update_core")
    else:
        delete_option("update_core")
    # end if
    #// 
    #// Fires after WordPress core has been successfully updated.
    #// 
    #// @since 3.3.0
    #// 
    #// @param string $wp_version The current WordPress version.
    #//
    do_action("_core_updated_successfully", wp_version_)
    #// Clear the option that blocks auto updates after failures, now that we've been successful.
    if php_function_exists("delete_site_option"):
        delete_site_option("auto_core_update_failed")
    # end if
    return wp_version_
# end def update_core
#// 
#// Copies a directory from one location to another via the WordPress Filesystem Abstraction.
#// Assumes that WP_Filesystem() has already been called and setup.
#// 
#// This is a temporary function for the 3.1 -> 3.2 upgrade, as well as for those upgrading to
#// 3.7+
#// 
#// @ignore
#// @since 3.2.0
#// @since 3.7.0 Updated not to use a regular expression for the skip list
#// @see copy_dir()
#// 
#// @global WP_Filesystem_Base $wp_filesystem
#// 
#// @param string   $from      Source directory.
#// @param string   $to        Destination directory.
#// @param string[] $skip_list Array of files/folders to skip copying.
#// @return true|WP_Error True on success, WP_Error on failure.
#//
def _copy_dir(from_=None, to_=None, skip_list_=None, *_args_):
    if skip_list_ is None:
        skip_list_ = Array()
    # end if
    
    global wp_filesystem_
    php_check_if_defined("wp_filesystem_")
    dirlist_ = wp_filesystem_.dirlist(from_)
    from_ = trailingslashit(from_)
    to_ = trailingslashit(to_)
    for filename_,fileinfo_ in dirlist_.items():
        if php_in_array(filename_, skip_list_, True):
            continue
        # end if
        if "f" == fileinfo_["type"]:
            if (not wp_filesystem_.copy(from_ + filename_, to_ + filename_, True, FS_CHMOD_FILE)):
                #// If copy failed, chmod file to 0644 and try again.
                wp_filesystem_.chmod(to_ + filename_, FS_CHMOD_FILE)
                if (not wp_filesystem_.copy(from_ + filename_, to_ + filename_, True, FS_CHMOD_FILE)):
                    return php_new_class("WP_Error", lambda : WP_Error("copy_failed__copy_dir", __("Could not copy file."), to_ + filename_))
                # end if
            # end if
        elif "d" == fileinfo_["type"]:
            if (not wp_filesystem_.is_dir(to_ + filename_)):
                if (not wp_filesystem_.mkdir(to_ + filename_, FS_CHMOD_DIR)):
                    return php_new_class("WP_Error", lambda : WP_Error("mkdir_failed__copy_dir", __("Could not create directory."), to_ + filename_))
                # end if
            # end if
            #// 
            #// Generate the $sub_skip_list for the subdirectory as a sub-set
            #// of the existing $skip_list.
            #//
            sub_skip_list_ = Array()
            for skip_item_ in skip_list_:
                if 0 == php_strpos(skip_item_, filename_ + "/"):
                    sub_skip_list_[-1] = php_preg_replace("!^" + preg_quote(filename_, "!") + "/!i", "", skip_item_)
                # end if
            # end for
            result_ = _copy_dir(from_ + filename_, to_ + filename_, sub_skip_list_)
            if is_wp_error(result_):
                return result_
            # end if
        # end if
    # end for
    return True
# end def _copy_dir
#// 
#// Redirect to the About WordPress page after a successful upgrade.
#// 
#// This function is only needed when the existing installation is older than 3.4.0.
#// 
#// @since 3.3.0
#// 
#// @global string $wp_version The WordPress version string.
#// @global string $pagenow
#// @global string $action
#// 
#// @param string $new_version
#//
def _redirect_to_about_wordpress(new_version_=None, *_args_):
    
    
    global wp_version_
    global pagenow_
    global action_
    php_check_if_defined("wp_version_","pagenow_","action_")
    if php_version_compare(wp_version_, "3.4-RC1", ">="):
        return
    # end if
    #// Ensure we only run this on the update-core.php page. The Core_Upgrader may be used in other contexts.
    if "update-core.php" != pagenow_:
        return
    # end if
    if "do-core-upgrade" != action_ and "do-core-reinstall" != action_:
        return
    # end if
    #// Load the updated default text localization domain for new strings.
    load_default_textdomain()
    #// See do_core_upgrade().
    show_message(__("WordPress updated successfully"))
    #// self_admin_url() won't exist when upgrading from <= 3.0, so relative URLs are intentional.
    show_message("<span class=\"hide-if-no-js\">" + php_sprintf(__("Welcome to WordPress %1$s. You will be redirected to the About WordPress screen. If not, click <a href=\"%2$s\">here</a>."), new_version_, "about.php?updated") + "</span>")
    show_message("<span class=\"hide-if-js\">" + php_sprintf(__("Welcome to WordPress %1$s. <a href=\"%2$s\">Learn more</a>."), new_version_, "about.php?updated") + "</span>")
    php_print("</div>")
    php_print("""<script type=\"text/javascript\">
    window.location = 'about.php?updated';
    </script>
    """)
    #// Include admin-footer.php and exit.
    php_include_file(ABSPATH + "wp-admin/admin-footer.php", once=True)
    php_exit(0)
# end def _redirect_to_about_wordpress
#// 
#// Cleans up Genericons example files.
#// 
#// @since 4.2.2
#// 
#// @global array              $wp_theme_directories
#// @global WP_Filesystem_Base $wp_filesystem
#//
def _upgrade_422_remove_genericons(*_args_):
    
    
    global wp_theme_directories_
    global wp_filesystem_
    php_check_if_defined("wp_theme_directories_","wp_filesystem_")
    #// A list of the affected files using the filesystem absolute paths.
    affected_files_ = Array()
    #// Themes.
    for directory_ in wp_theme_directories_:
        affected_theme_files_ = _upgrade_422_find_genericons_files_in_folder(directory_)
        affected_files_ = php_array_merge(affected_files_, affected_theme_files_)
    # end for
    #// Plugins.
    affected_plugin_files_ = _upgrade_422_find_genericons_files_in_folder(WP_PLUGIN_DIR)
    affected_files_ = php_array_merge(affected_files_, affected_plugin_files_)
    for file_ in affected_files_:
        gen_dir_ = wp_filesystem_.find_folder(trailingslashit(php_dirname(file_)))
        if php_empty(lambda : gen_dir_):
            continue
        # end if
        #// The path when the file is accessed via WP_Filesystem may differ in the case of FTP.
        remote_file_ = gen_dir_ + php_basename(file_)
        if (not wp_filesystem_.exists(remote_file_)):
            continue
        # end if
        if (not wp_filesystem_.delete(remote_file_, False, "f")):
            wp_filesystem_.put_contents(remote_file_, "")
        # end if
    # end for
# end def _upgrade_422_remove_genericons
#// 
#// Recursively find Genericons example files in a given folder.
#// 
#// @ignore
#// @since 4.2.2
#// 
#// @param string $directory Directory path. Expects trailingslashed.
#// @return array
#//
def _upgrade_422_find_genericons_files_in_folder(directory_=None, *_args_):
    
    
    directory_ = trailingslashit(directory_)
    files_ = Array()
    if php_file_exists(str(directory_) + str("example.html")) and False != php_strpos(php_file_get_contents(str(directory_) + str("example.html")), "<title>Genericons</title>"):
        files_[-1] = str(directory_) + str("example.html")
    # end if
    dirs_ = glob(directory_ + "*", GLOB_ONLYDIR)
    if dirs_:
        for dir_ in dirs_:
            files_ = php_array_merge(files_, _upgrade_422_find_genericons_files_in_folder(dir_))
        # end for
    # end if
    return files_
# end def _upgrade_422_find_genericons_files_in_folder
#// 
#// @ignore
#// @since 4.4.0
#//
def _upgrade_440_force_deactivate_incompatible_plugins(*_args_):
    
    
    if php_defined("REST_API_VERSION") and php_version_compare(REST_API_VERSION, "2.0-beta4", "<="):
        deactivate_plugins(Array("rest-api/plugin.php"), True)
    # end if
# end def _upgrade_440_force_deactivate_incompatible_plugins
