<?php declare(strict_types=1);

require __DIR__ . '/vendor/autoload.php';

use PhpParser\Error;
use PhpParser\ParserFactory;

function utf8ize($d)
{
    if (is_array($d)) {
        foreach ($d as $k => $v) {
            unset($d[$k]);
            $d[utf8ize($k)] = utf8ize($v);
        }
    } else if (is_object($d)) {
        $objVars = get_object_vars($d);
        foreach ($objVars as $key => $value) {
            $d->$key = utf8ize($value);
        }
    } else if (is_string($d)) {
        return iconv('UTF-8', 'UTF-8//IGNORE', utf8_encode($d));
    }
    return $d;
}

function php2ast()
{
    global $argv;

    $fname = $argv[1];

    if (!is_readable($fname)) {
        echo "[-] Error reading file {$fname}.\n";
        exit(1);
    }

    $code = file_get_contents($fname);
    if ($code === FALSE) {
        echo "[-] Error reading file {$fname}\n";
        exit(2);
    }
    $parser = (new ParserFactory)->create(ParserFactory::PREFER_PHP7);
    try {
        $ast = $parser->parse($code);
        echo json_encode(utf8ize($ast));
    } catch (Error $error) {
        echo "[-] Error parsing {$fname}: {$error->getMessage()}\n";
        exit(3);
    }
}

php2ast();
