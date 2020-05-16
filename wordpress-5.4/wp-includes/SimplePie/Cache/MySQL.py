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
#// SimplePie
#// 
#// A PHP-Based RSS and Atom Feed Framework.
#// Takes the hard work out of managing a complete RSS/Atom solution.
#// 
#// Copyright (c) 2004-2012, Ryan Parman, Geoffrey Sneddon, Ryan McCue, and contributors
#// All rights reserved.
#// 
#// Redistribution and use in source and binary forms, with or without modification, are
#// permitted provided that the following conditions are met:
#// 
#// Redistributions of source code must retain the above copyright notice, this list of
#// conditions and the following disclaimer.
#// 
#// Redistributions in binary form must reproduce the above copyright notice, this list
#// of conditions and the following disclaimer in the documentation and/or other materials
#// provided with the distribution.
#// 
#// Neither the name of the SimplePie Team nor the names of its contributors may be used
#// to endorse or promote products derived from this software without specific prior
#// written permission.
#// 
#// THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND ANY EXPRESS
#// OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY
#// AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDERS
#// AND CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
#// CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
#// SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY
#// THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR
#// OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
#// POSSIBILITY OF SUCH DAMAGE.
#// 
#// @package SimplePie
#// @version 1.3.1
#// @copyright 2004-2012 Ryan Parman, Geoffrey Sneddon, Ryan McCue
#// @author Ryan Parman
#// @author Geoffrey Sneddon
#// @author Ryan McCue
#// @link http://simplepie.org/ SimplePie
#// @license http://www.opensource.org/licenses/bsd-license.php BSD License
#// 
#// 
#// Caches data to a MySQL database
#// 
#// Registered for URLs with the "mysql" protocol
#// 
#// For example, `mysql://root:password@localhost:3306/mydb?prefix=sp_` will
#// connect to the `mydb` database on `localhost` on port 3306, with the user
#// `root` and the password `password`. All tables will be prefixed with `sp_`
#// 
#// @package SimplePie
#// @subpackage Caching
#//
class SimplePie_Cache_MySQL(SimplePie_Cache_DB):
    mysql = Array()
    options = Array()
    id = Array()
    #// 
    #// Create a new cache object
    #// 
    #// @param string $location Location string (from SimplePie::$cache_location)
    #// @param string $name Unique ID for the cache
    #// @param string $type Either TYPE_FEED for SimplePie data, or TYPE_IMAGE for image data
    #//
    def __init__(self, location=None, name=None, type=None):
        
        self.options = Array({"user": None, "pass": None, "host": "127.0.0.1", "port": "3306", "path": "", "extras": Array({"prefix": ""})})
        self.options = php_array_merge_recursive(self.options, SimplePie_Cache.parse_url(location))
        #// Path is prefixed with a "/"
        self.options["dbname"] = php_substr(self.options["path"], 1)
        try: 
            self.mysql = php_new_class("PDO", lambda : PDO(str("mysql:dbname=") + str(self.options["dbname"]) + str(";host=") + str(self.options["host"]) + str(";port=") + str(self.options["port"]), self.options["user"], self.options["pass"], Array({PDO.MYSQL_ATTR_INIT_COMMAND: "SET NAMES utf8"})))
        except PDOException as e:
            self.mysql = None
            return
        # end try
        self.id = name + type
        query = self.mysql.query("SHOW TABLES")
        if (not query):
            self.mysql = None
            return
        # end if
        db = Array()
        while True:
            row = query.fetchcolumn()
            if not (row):
                break
            # end if
            db[-1] = row
        # end while
        if (not php_in_array(self.options["extras"]["prefix"] + "cache_data", db)):
            query = self.mysql.exec("CREATE TABLE `" + self.options["extras"]["prefix"] + "cache_data` (`id` TEXT CHARACTER SET utf8 NOT NULL, `items` SMALLINT NOT NULL DEFAULT 0, `data` BLOB NOT NULL, `mtime` INT UNSIGNED NOT NULL, UNIQUE (`id`(125)))")
            if query == False:
                self.mysql = None
            # end if
        # end if
        if (not php_in_array(self.options["extras"]["prefix"] + "items", db)):
            query = self.mysql.exec("CREATE TABLE `" + self.options["extras"]["prefix"] + "items` (`feed_id` TEXT CHARACTER SET utf8 NOT NULL, `id` TEXT CHARACTER SET utf8 NOT NULL, `data` TEXT CHARACTER SET utf8 NOT NULL, `posted` INT UNSIGNED NOT NULL, INDEX `feed_id` (`feed_id`(125)))")
            if query == False:
                self.mysql = None
            # end if
        # end if
    # end def __init__
    #// 
    #// Save data to the cache
    #// 
    #// @param array|SimplePie $data Data to store in the cache. If passed a SimplePie object, only cache the $data property
    #// @return bool Successfulness
    #//
    def save(self, data=None):
        
        if self.mysql == None:
            return False
        # end if
        if type(data).__name__ == "SimplePie":
            data = copy.deepcopy(data)
            prepared = self.prepare_simplepie_object_for_cache(data)
            query = self.mysql.prepare("SELECT COUNT(*) FROM `" + self.options["extras"]["prefix"] + "cache_data` WHERE `id` = :feed")
            query.bindvalue(":feed", self.id)
            if query.execute():
                if query.fetchcolumn() > 0:
                    items = php_count(prepared[1])
                    if items:
                        sql = "UPDATE `" + self.options["extras"]["prefix"] + "cache_data` SET `items` = :items, `data` = :data, `mtime` = :time WHERE `id` = :feed"
                        query = self.mysql.prepare(sql)
                        query.bindvalue(":items", items)
                    else:
                        sql = "UPDATE `" + self.options["extras"]["prefix"] + "cache_data` SET `data` = :data, `mtime` = :time WHERE `id` = :feed"
                        query = self.mysql.prepare(sql)
                    # end if
                    query.bindvalue(":data", prepared[0])
                    query.bindvalue(":time", time())
                    query.bindvalue(":feed", self.id)
                    if (not query.execute()):
                        return False
                    # end if
                else:
                    query = self.mysql.prepare("INSERT INTO `" + self.options["extras"]["prefix"] + "cache_data` (`id`, `items`, `data`, `mtime`) VALUES(:feed, :count, :data, :time)")
                    query.bindvalue(":feed", self.id)
                    query.bindvalue(":count", php_count(prepared[1]))
                    query.bindvalue(":data", prepared[0])
                    query.bindvalue(":time", time())
                    if (not query.execute()):
                        return False
                    # end if
                # end if
                ids = php_array_keys(prepared[1])
                if (not php_empty(lambda : ids)):
                    for id in ids:
                        database_ids[-1] = self.mysql.quote(id)
                    # end for
                    query = self.mysql.prepare("SELECT `id` FROM `" + self.options["extras"]["prefix"] + "items` WHERE `id` = " + php_implode(" OR `id` = ", database_ids) + " AND `feed_id` = :feed")
                    query.bindvalue(":feed", self.id)
                    if query.execute():
                        existing_ids = Array()
                        while True:
                            row = query.fetchcolumn()
                            if not (row):
                                break
                            # end if
                            existing_ids[-1] = row
                        # end while
                        new_ids = php_array_diff(ids, existing_ids)
                        for new_id in new_ids:
                            date = prepared[1][new_id].get_date("U")
                            if (not date):
                                date = time()
                            # end if
                            query = self.mysql.prepare("INSERT INTO `" + self.options["extras"]["prefix"] + "items` (`feed_id`, `id`, `data`, `posted`) VALUES(:feed, :id, :data, :date)")
                            query.bindvalue(":feed", self.id)
                            query.bindvalue(":id", new_id)
                            query.bindvalue(":data", serialize(prepared[1][new_id].data))
                            query.bindvalue(":date", date)
                            if (not query.execute()):
                                return False
                            # end if
                        # end for
                        return True
                    # end if
                else:
                    return True
                # end if
            # end if
        else:
            query = self.mysql.prepare("SELECT `id` FROM `" + self.options["extras"]["prefix"] + "cache_data` WHERE `id` = :feed")
            query.bindvalue(":feed", self.id)
            if query.execute():
                if query.rowcount() > 0:
                    query = self.mysql.prepare("UPDATE `" + self.options["extras"]["prefix"] + "cache_data` SET `items` = 0, `data` = :data, `mtime` = :time WHERE `id` = :feed")
                    query.bindvalue(":data", serialize(data))
                    query.bindvalue(":time", time())
                    query.bindvalue(":feed", self.id)
                    if self.execute():
                        return True
                    # end if
                else:
                    query = self.mysql.prepare("INSERT INTO `" + self.options["extras"]["prefix"] + "cache_data` (`id`, `items`, `data`, `mtime`) VALUES(:id, 0, :data, :time)")
                    query.bindvalue(":id", self.id)
                    query.bindvalue(":data", serialize(data))
                    query.bindvalue(":time", time())
                    if query.execute():
                        return True
                    # end if
                # end if
            # end if
        # end if
        return False
    # end def save
    #// 
    #// Retrieve the data saved to the cache
    #// 
    #// @return array Data for SimplePie::$data
    #//
    def load(self):
        
        if self.mysql == None:
            return False
        # end if
        query = self.mysql.prepare("SELECT `items`, `data` FROM `" + self.options["extras"]["prefix"] + "cache_data` WHERE `id` = :id")
        query.bindvalue(":id", self.id)
        row = query.fetch()
        if query.execute() and row:
            data = unserialize(row[1])
            if (php_isset(lambda : self.options["items"][0])):
                items = php_int(self.options["items"][0])
            else:
                items = php_int(row[0])
            # end if
            if items != 0:
                if (php_isset(lambda : data["child"][SIMPLEPIE_NAMESPACE_ATOM_10]["feed"][0])):
                    feed = data["child"][SIMPLEPIE_NAMESPACE_ATOM_10]["feed"][0]
                elif (php_isset(lambda : data["child"][SIMPLEPIE_NAMESPACE_ATOM_03]["feed"][0])):
                    feed = data["child"][SIMPLEPIE_NAMESPACE_ATOM_03]["feed"][0]
                elif (php_isset(lambda : data["child"][SIMPLEPIE_NAMESPACE_RDF]["RDF"][0])):
                    feed = data["child"][SIMPLEPIE_NAMESPACE_RDF]["RDF"][0]
                elif (php_isset(lambda : data["child"][SIMPLEPIE_NAMESPACE_RSS_20]["rss"][0])):
                    feed = data["child"][SIMPLEPIE_NAMESPACE_RSS_20]["rss"][0]
                else:
                    feed = None
                # end if
                if feed != None:
                    sql = "SELECT `data` FROM `" + self.options["extras"]["prefix"] + "items` WHERE `feed_id` = :feed ORDER BY `posted` DESC"
                    if items > 0:
                        sql += " LIMIT " + items
                    # end if
                    query = self.mysql.prepare(sql)
                    query.bindvalue(":feed", self.id)
                    if query.execute():
                        while True:
                            row = query.fetchcolumn()
                            if not (row):
                                break
                            # end if
                            feed["child"][SIMPLEPIE_NAMESPACE_ATOM_10]["entry"][-1] = unserialize(row)
                        # end while
                    else:
                        return False
                    # end if
                # end if
            # end if
            return data
        # end if
        return False
    # end def load
    #// 
    #// Retrieve the last modified time for the cache
    #// 
    #// @return int Timestamp
    #//
    def mtime(self):
        
        if self.mysql == None:
            return False
        # end if
        query = self.mysql.prepare("SELECT `mtime` FROM `" + self.options["extras"]["prefix"] + "cache_data` WHERE `id` = :id")
        query.bindvalue(":id", self.id)
        time = query.fetchcolumn()
        if query.execute() and time:
            return time
        else:
            return False
        # end if
    # end def mtime
    #// 
    #// Set the last modified time to the current time
    #// 
    #// @return bool Success status
    #//
    def touch(self):
        
        if self.mysql == None:
            return False
        # end if
        query = self.mysql.prepare("UPDATE `" + self.options["extras"]["prefix"] + "cache_data` SET `mtime` = :time WHERE `id` = :id")
        query.bindvalue(":time", time())
        query.bindvalue(":id", self.id)
        if query.execute() and query.rowcount() > 0:
            return True
        else:
            return False
        # end if
    # end def touch
    #// 
    #// Remove the cache
    #// 
    #// @return bool Success status
    #//
    def unlink(self):
        
        if self.mysql == None:
            return False
        # end if
        query = self.mysql.prepare("DELETE FROM `" + self.options["extras"]["prefix"] + "cache_data` WHERE `id` = :id")
        query.bindvalue(":id", self.id)
        query2 = self.mysql.prepare("DELETE FROM `" + self.options["extras"]["prefix"] + "items` WHERE `feed_id` = :id")
        query2.bindvalue(":id", self.id)
        if query.execute() and query2.execute():
            return True
        else:
            return False
        # end if
    # end def unlink
# end class SimplePie_Cache_MySQL
