#!/usr/bin/python
import httplib
import optparse
import os
import sys
import threading
import urllib
import urlparse


__version__ = (0, 1, 0)

PASTEE_URL = "https://pastee.org"
DEFAULT_LEXER = "text"
DEFAULT_TTL = 30  # days


class Paste:
    """Class representing a paste that has been submitted."""

    def __init__(self, content, lexer, url):
        """Constructor.

        Args:
          content: paste content
          lexer: lexer used for this paste
          url: URL to access the paste
        """
        self.content = content
        self.lexer = lexer
        self.url = url

    def __unicode__(self):
        return self.url

    def __str__(self):
        return str(self.__unicode__)


class PasteClient:
    """Pasting client for a Pastee application.

    Instances of this class can be used to programmatically create new pastes on
    an installation of Pastee (https://pastee.org).

    This class is thread-safe.
    """

    def __init__(self, url=PASTEE_URL):
        """Constructor.

        Args:
          url: URL to Pastee installation (defaults to https://pastee.org)
        """
        parse = urlparse.urlsplit(url)
        self._scheme = parse[0]
        self._netloc = parse[1]
        self._lock = threading.Semaphore()

    def paste(self, content, lexer=None, ttl=None, key=None):
        """Create a new paste.

        Args:
          content: string of text to paste
          lexer: lexer to use (defaults to text)
          ttl: time-to-live in days (defaults to 30)
          key: encrypt paste with this key; if not specified, paste is not
               encrypted

        Returns:
          Paste object
        """
        if lexer is None:
            lexer = DEFAULT_LEXER
        if ttl is None:
            ttl = DEFAULT_TTL

        if self._scheme == "https":
            self._conn = httplib.HTTPSConnection(self._netloc)
        else:
            self._conn = httplib.HTTPConnection(self._netloc)

        headers = {"Content-type": "application/x-www-form-urlencoded",
                   "Accept": "text/plain"}
        params = {"lexer": lexer,
                  "content": content,
                  "ttl": int(ttl * 86400)}
        if key is not None:
            params["encrypt"] = "checked"
            params["key"] = key

        self._lock.acquire()
        self._conn.request("POST", "/submit", urllib.urlencode(params), headers)
        response = self._conn.getresponse()
        self._lock.release()
        return self._make_paste(response, content, lexer)

    def paste_file(self, filename, lexer=None, ttl=None, key=None):
        """Create a new paste from a file.

        Args:
          filename: path to file
          lexer: lexer to use (defaults to extension of the file or text)
          ttl: time-to-live in days (defaults to 30)
          key: encrypt paste with this key; if not specified, paste is not
               encrypted

        Returns:
          Paste object
        """
        _, ext = os.path.splitext(filename)
        if lexer is None and ext:
            lexer = ext[1:]  # remove leading period first
        # TODO(ms): need exception handling here
        fd = open(filename, "r")
        content = fd.read()
        fd.close()
        return self.paste(content, lexer=lexer, ttl=ttl, key=key)

    def _make_paste(self, response, content, lexer):
        for (key, value) in response.getheaders():
            if key.lower() == "location":
                return self._clean_url(value)
        return Paste(content, lexer, self._clean_url(value))

    @staticmethod
    def _clean_url(url):
        p = urlparse.urlsplit(url)
        scheme = p[0]
        netloc_split = p[1].split(":")
        hostname = netloc_split[0]
        if len(netloc_split) > 1:
            port = int(netloc_split[1])
        else:
            port = scheme == "https" and 443 or 80
        path = p[2]
        port_str = ""
        if port != 80 and scheme == "http":
            port_str = ":%d" % port
        elif port != 443 and scheme == "https":
            port_str = ":%d" % port
        return "%s://%s%s%s" % (scheme, hostname, port_str, path)


def die_with_error(message):
    """Print a message and exit with exit code 1.

    Args:
      message: message to print before exiting
    """
    print "error: %s" % message
    sys.exit(1)


def main():
    parser = optparse.OptionParser()
    parser.add_option("-l", "--lexer", dest="lexer", metavar="LEXERNAME",
                      help=("Force use of a particular lexer (i.e. c, py). "
                            "This defaults to the extension of the supplied "
                            "filenames, or 'text' if pasting from stdin."))
    parser.add_option("-t", "--ttl", dest="ttl", metavar="DAYS",
                      help="Number of days before the paste will expire.")
    parser.add_option("-k", "--key", dest="key", metavar="PASSPHRASE",
                      help="Encrypt pastes with this key.")
    (options, filenames) = parser.parse_args()
    lexer = options.lexer
    key = options.key
    try:
        ttl = float(options.ttl)
    except ValueError:
        die_with_error("floating point number must be passed for TTL")
    except TypeError:
        ttl = None

    client = PasteClient()

    if filenames:
        # paste from multiple files
        for filename in filenames:
            print client.paste_file(filename, lexer=lexer, ttl=ttl, key=key)
    else:
        # paste from stdin
        print client.paste(sys.stdin.read(), lexer=lexer, ttl=ttl, key=key)


if __name__ == "__main__":
    main()
