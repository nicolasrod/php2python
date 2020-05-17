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
#// The base configuration for WordPress
#// 
#// The wp-config.php creation script uses this file during the
#// installation. You don't have to use the web site, you can
#// copy this file to "wp-config.php" and fill in the values.
#// 
#// This file contains the following configurations:
#// 
#// MySQL settings
#// Secret keys
#// Database table prefix
#// ABSPATH
#// 
#// @link https://wordpress.org/support/article/editing-wp-config-php/
#// 
#// @package WordPress
#// 
#// MySQL settings - You can get this info from your web host ** //
#// The name of the database for WordPress
php_define("DB_NAME", "wp")
#// MySQL database username
php_define("DB_USER", "root")
#// MySQL database password
php_define("DB_PASSWORD", "")
#// MySQL hostname
php_define("DB_HOST", "localhost")
#// Database Charset to use in creating database tables.
php_define("DB_CHARSET", "utf8")
#// The Database Collate type. Don't change this if in doubt.
php_define("DB_COLLATE", "")
#// #@+
#// Authentication Unique Keys and Salts.
#// 
#// Change these to different unique phrases!
#// You can generate these using the {@link https://api.wordpress.org/secret-key/1.1/salt/ WordPress.org secret-key service}
#// You can change these at any point in time to invalidate all existing cookies. This will force all users to have to log in again.
#// 
#// @since 2.6.0
#//
php_define("AUTH_KEY", "put your unique phrase here")
php_define("SECURE_AUTH_KEY", "put your unique phrase here")
php_define("LOGGED_IN_KEY", "put your unique phrase here")
php_define("NONCE_KEY", "put your unique phrase here")
php_define("AUTH_SALT", "put your unique phrase here")
php_define("SECURE_AUTH_SALT", "put your unique phrase here")
php_define("LOGGED_IN_SALT", "put your unique phrase here")
php_define("NONCE_SALT", "put your unique phrase here")
#// #@-
#// 
#// WordPress Database Table prefix.
#// 
#// You can have multiple installations in one database if you give each
#// a unique prefix. Only numbers, letters, and underscores please!
#//
table_prefix_ = "wp_power2017"
#// 
#// For developers: WordPress debugging mode.
#// 
#// Change this to true to enable the display of notices during development.
#// It is strongly recommended that plugin and theme developers use WP_DEBUG
#// in their development environments.
#// 
#// For information on other constants that can be used for debugging,
#// visit the documentation.
#// 
#// @link https://wordpress.org/support/article/debugging-in-wordpress/
#//
php_define("WP_DEBUG", False)
#// That's all, stop editing! Happy publishing.
#// Absolute path to the WordPress directory.
if (not php_defined("ABSPATH")):
    php_define("ABSPATH", __DIR__ + "/")
# end if
#// Sets up WordPress vars and included files.
php_include_file(ABSPATH + "wp-settings.php", once=True)
