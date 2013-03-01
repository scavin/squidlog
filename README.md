squidlog
========

squidlog is a tool to analyzes your squid `access.log` file, display the usage information or send to a RADIUS server using `Accounting-Request` as defined in RFC 2866.

It may call squid to rotate your log file so that no lines will be counted more than once.

Forked from Jiehan Zheng's [squid2radius](https://github.com/jiehanzheng/squid2radius).

Installation
------------

### Clone Git repo

```bash
git clone git://github.com/billzhong/squidlog.git
```

Usage for Radius
----------------

```
usage: squid2radius.py [-h] [-p RADIUS_ACCT_PORT]
                       [--radius-nasid RADIUS_NASID] [--squid-path SQUID_PATH]
                       [--exclude-pattern EXCLUDE_PATTERN] [--no-rotation]
                       logfile_path radius_server radius_secret
```

For instance, run like this if you have access log file at `/var/log/squid/access.log`, RADIUS server running at `localhost` with secret set to `testing123`:

```bash
python squid2radius.py /var/log/squid/access.log localhost testing123
```

It is certainly a good idea to make a cron job for this.

You should also read [SquidFaq/SquidLogs](http://wiki.squid-cache.org/SquidFaq/SquidLogs#access.log) to make sure your log files are in reasonable sizes.

### --exclude-pattern

If for some reason you need to prevent usage information of certain user from being sent to the RADIUS server, there is an argument for that!  Use `--exclude-pattern="(girl|boy)friend"` and squid2radius.py won't send usage of either your `girlfriend` or `boyfriend` to the RADIUS server.

### --no-rotation

By default squid2radius.py calls `squid -k rotate` to make squid rotate your log files right after we are done counting usage data, in order to ensure usage data accuracy by not counting any log lines more than once next time you run it.  If this is troublesome in your setup, you can add `--no-rotation` argument to disable this behavior.

Usage for Display
-----------------

```
usage: squidlocal.py [-h] [--exclude-pattern EXCLUDE_PATTERN]
                     logfile_path
```

For example, you have an access log file at `/var/log/squid/access.log`:

```bash
python squidlocal.py /var/log/squid/access.log
```

### --exclude-pattern

If for some reason you need to prevent usage information of certain user from being sent to the RADIUS server, there is an argument for that!  Use `--exclude-pattern="(girl|boy)friend"` and squidlocal.py won't send usage of either your `girlfriend` or `boyfriend` to the RADIUS server.

Note
----

The script assumes that you are using the default [Squid native access.log format](http://wiki.squid-cache.org/Features/LogFormat#squid) on first ten columns of your log file.  If you need custom columns, add them after the default ones.
