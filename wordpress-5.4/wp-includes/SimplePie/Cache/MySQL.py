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
    #// 
    #// PDO instance
    #// 
    #// @var PDO
    #//
    mysql = Array()
    #// 
    #// Options
    #// 
    #// @var array
    #//
    options = Array()
    #// 
    #// Cache ID
    #// 
    #// @var string
    #//
    id = Array()
    #// 
    #// Create a new cache object
    #// 
    #// @param string $location Location string (from SimplePie::$cache_location)
    #// @param string $name Unique ID for the cache
    #// @param string $type Either TYPE_FEED for SimplePie data, or TYPE_IMAGE for image data
    #//
    def __init__(self, location_=None, name_=None, type_=None):
        
        
        self.options = Array({"user": None, "pass": None, "host": "127.0.0.1", "port": "3306", "path": "", "extras": Array({"prefix": ""})})
        self.options = php_array_merge_recursive(self.options, SimplePie_Cache.parse_url(location_))
        #// Path is prefixed with a "/"
        self.options["dbname"] = php_substr(self.options["path"], 1)
        try: 
            self.mysql = php_new_class("PDO", lambda : PDO(str("mysql:dbname=") + str(self.options["dbname"]) + str(";host=") + str(self.options["host"]) + str(";port=") + str(self.options["port"]), self.options["user"], self.options["pass"], Array({PDO.MYSQL_ATTR_INIT_COMMAND: "SET NAMES utf8"})))
        except PDOException as e_:
            self.mysql = None
            return
        # end try
        self.id = name_ + type_
        query_ = self.mysql.query("SHOW TABLES")
        if (not query_):
            self.mysql = None
            return
        # end if
        db_ = Array()
        while True:
            row_ = query_.fetchcolumn()
            if not (row_):
                break
            # end if
            db_[-1] = row_
        # end while
        if (not php_in_array(self.options["extras"]["prefix"] + "cache_data", db_)):
            query_ = self.mysql.exec("CREATE TABLE `" + self.options["extras"]["prefix"] + "cache_data` (`id` TEXT CHARACTER SET utf8 NOT NULL, `items` SMALLINT NOT NULL DEFAULT 0, `data` BLOB NOT NULL, `mtime` INT UNSIGNED NOT NULL, UNIQUE (`id`(125)))")
            if query_ == False:
                self.mysql = None
            # end if
        # end if
        if (not php_in_array(self.options["extras"]["prefix"] + "items", db_)):
            query_ = self.mysql.exec("CREATE TABLE `" + self.options["extras"]["prefix"] + "items` (`feed_id` TEXT CHARACTER SET utf8 NOT NULL, `id` TEXT CHARACTER SET utf8 NOT NULL, `data` TEXT CHARACTER SET utf8 NOT NULL, `posted` INT UNSIGNED NOT NULL, INDEX `feed_id` (`feed_id`(125)))")
            if query_ == False:
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
    def save(self, data_=None):
        
        
        if self.mysql == None:
            return False
        # end if
        if type(data_).__name__ == "SimplePie":
            data_ = copy.deepcopy(data_)
            prepared_ = self.prepare_simplepie_object_for_cache(data_)
            query_ = self.mysql.prepare("SELECT COUNT(*) FROM `" + self.options["extras"]["prefix"] + "cache_data` WHERE `id` = :feed")
            query_.bindvalue(":feed", self.id)
            if query_.execute():
                if query_.fetchcolumn() > 0:
                    items_ = php_count(prepared_[1])
                    if items_:
                        sql_ = "UPDATE `" + self.options["extras"]["prefix"] + "cache_data` SET `items` = :items, `data` = :data, `mtime` = :time WHERE `id` = :feed"
                        query_ = self.mysql.prepare(sql_)
                        query_.bindvalue(":items", items_)
                    else:
                        sql_ = "UPDATE `" + self.options["extras"]["prefix"] + "cache_data` SET `data` = :data, `mtime` = :time WHERE `id` = :feed"
                        query_ = self.mysql.prepare(sql_)
                    # end if
                    query_.bindvalue(":data", prepared_[0])
                    query_.bindvalue(":time", time())
                    query_.bindvalue(":feed", self.id)
                    if (not query_.execute()):
                        return False
                    # end if
                else:
                    query_ = self.mysql.prepare("INSERT INTO `" + self.options["extras"]["prefix"] + "cache_data` (`id`, `items`, `data`, `mtime`) VALUES(:feed, :count, :data, :time)")
                    query_.bindvalue(":feed", self.id)
                    query_.bindvalue(":count", php_count(prepared_[1]))
                    query_.bindvalue(":data", prepared_[0])
                    query_.bindvalue(":time", time())
                    if (not query_.execute()):
                        return False
                    # end if
                # end if
                ids_ = php_array_keys(prepared_[1])
                if (not php_empty(lambda : ids_)):
                    for id_ in ids_:
                        database_ids_[-1] = self.mysql.quote(id_)
                    # end for
                    query_ = self.mysql.prepare("SELECT `id` FROM `" + self.options["extras"]["prefix"] + "items` WHERE `id` = " + php_implode(" OR `id` = ", database_ids_) + " AND `feed_id` = :feed")
                    query_.bindvalue(":feed", self.id)
                    if query_.execute():
                        existing_ids_ = Array()
                        while True:
                            row_ = query_.fetchcolumn()
                            if not (row_):
                                break
                            # end if
                            existing_ids_[-1] = row_
                        # end while
                        new_ids_ = php_array_diff(ids_, existing_ids_)
                        for new_id_ in new_ids_:
                            date_ = prepared_[1][new_id_].get_date("U")
                            if (not date_):
                                date_ = time()
                            # end if
                            query_ = self.mysql.prepare("INSERT INTO `" + self.options["extras"]["prefix"] + "items` (`feed_id`, `id`, `data`, `posted`) VALUES(:feed, :id, :data, :date)")
                            query_.bindvalue(":feed", self.id)
                            query_.bindvalue(":id", new_id_)
                            query_.bindvalue(":data", serialize(prepared_[1][new_id_].data))
                            query_.bindvalue(":date", date_)
                            if (not query_.execute()):
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
            query_ = self.mysql.prepare("SELECT `id` FROM `" + self.options["extras"]["prefix"] + "cache_data` WHERE `id` = :feed")
            query_.bindvalue(":feed", self.id)
            if query_.execute():
                if query_.rowcount() > 0:
                    query_ = self.mysql.prepare("UPDATE `" + self.options["extras"]["prefix"] + "cache_data` SET `items` = 0, `data` = :data, `mtime` = :time WHERE `id` = :feed")
                    query_.bindvalue(":data", serialize(data_))
                    query_.bindvalue(":time", time())
                    query_.bindvalue(":feed", self.id)
                    if self.execute():
                        return True
                    # end if
                else:
                    query_ = self.mysql.prepare("INSERT INTO `" + self.options["extras"]["prefix"] + "cache_data` (`id`, `items`, `data`, `mtime`) VALUES(:id, 0, :data, :time)")
                    query_.bindvalue(":id", self.id)
                    query_.bindvalue(":data", serialize(data_))
                    query_.bindvalue(":time", time())
                    if query_.execute():
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
        query_ = self.mysql.prepare("SELECT `items`, `data` FROM `" + self.options["extras"]["prefix"] + "cache_data` WHERE `id` = :id")
        query_.bindvalue(":id", self.id)
        row_ = query_.fetch()
        if query_.execute() and row_:
            data_ = unserialize(row_[1])
            if (php_isset(lambda : self.options["items"][0])):
                items_ = php_int(self.options["items"][0])
            else:
                items_ = php_int(row_[0])
            # end if
            if items_ != 0:
                if (php_isset(lambda : data_["child"][SIMPLEPIE_NAMESPACE_ATOM_10]["feed"][0])):
                    feed_ = data_["child"][SIMPLEPIE_NAMESPACE_ATOM_10]["feed"][0]
                elif (php_isset(lambda : data_["child"][SIMPLEPIE_NAMESPACE_ATOM_03]["feed"][0])):
                    feed_ = data_["child"][SIMPLEPIE_NAMESPACE_ATOM_03]["feed"][0]
                elif (php_isset(lambda : data_["child"][SIMPLEPIE_NAMESPACE_RDF]["RDF"][0])):
                    feed_ = data_["child"][SIMPLEPIE_NAMESPACE_RDF]["RDF"][0]
                elif (php_isset(lambda : data_["child"][SIMPLEPIE_NAMESPACE_RSS_20]["rss"][0])):
                    feed_ = data_["child"][SIMPLEPIE_NAMESPACE_RSS_20]["rss"][0]
                else:
                    feed_ = None
                # end if
                if feed_ != None:
                    sql_ = "SELECT `data` FROM `" + self.options["extras"]["prefix"] + "items` WHERE `feed_id` = :feed ORDER BY `posted` DESC"
                    if items_ > 0:
                        sql_ += " LIMIT " + items_
                    # end if
                    query_ = self.mysql.prepare(sql_)
                    query_.bindvalue(":feed", self.id)
                    if query_.execute():
                        while True:
                            row_ = query_.fetchcolumn()
                            if not (row_):
                                break
                            # end if
                            feed_["child"][SIMPLEPIE_NAMESPACE_ATOM_10]["entry"][-1] = unserialize(row_)
                        # end while
                    else:
                        return False
                    # end if
                # end if
            # end if
            return data_
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
        query_ = self.mysql.prepare("SELECT `mtime` FROM `" + self.options["extras"]["prefix"] + "cache_data` WHERE `id` = :id")
        query_.bindvalue(":id", self.id)
        time_ = query_.fetchcolumn()
        if query_.execute() and time_:
            return time_
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
        query_ = self.mysql.prepare("UPDATE `" + self.options["extras"]["prefix"] + "cache_data` SET `mtime` = :time WHERE `id` = :id")
        query_.bindvalue(":time", time())
        query_.bindvalue(":id", self.id)
        if query_.execute() and query_.rowcount() > 0:
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
        query_ = self.mysql.prepare("DELETE FROM `" + self.options["extras"]["prefix"] + "cache_data` WHERE `id` = :id")
        query_.bindvalue(":id", self.id)
        query2_ = self.mysql.prepare("DELETE FROM `" + self.options["extras"]["prefix"] + "items` WHERE `feed_id` = :id")
        query2_.bindvalue(":id", self.id)
        if query_.execute() and query2_.execute():
            return True
        else:
            return False
        # end if
    # end def unlink
# end class SimplePie_Cache_MySQL
