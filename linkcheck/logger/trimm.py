# -*- coding: iso-8859-1 -*-
# Copyright (C) 2000-2014 Bastian Kleineidam
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License along
# with this program; if not, write to the Free Software Foundation, Inc.,
# 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA.
"""
A HTML logger with TRIMM styling.
"""
import time
import cgi
import os
from . import _Logger
from .. import strformat, configuration


# ss=1 enables show source
validate_html = "http://validator.w3.org/check?ss=1&amp;uri=%(uri)s"
# options are the default
validate_css = "http://jigsaw.w3.org/css-validator/validator?" \
               "uri=%(uri)s&amp;warning=1&amp;profile=css2&amp;usermedium=all"

HTML_HEADER = """<!DOCTYPE HTML>
<html>
<head>
<meta http-equiv="Content-Type" content="text/html; charset=%(encoding)s"/>
<title>%(title)s</title>
<style type="text/css">
<!--
 h2 { font-family: gotham-book, Helvetica, Arial, sans-serif; font-size: 22px; font-weight: bold; }
 body { font-family: gotham-book, Helvetica, Arial, sans-serif; font-size: 16px; background-color: %(body)s; color: %(colorfont)s; line-height: 1.6 }
 td { font-family: gotham-book, Helvetica, Arial, sans-serif; font-size: 11pt; }
 code { font-family: consolas, Courier; }
 a:link {color: %(link)s;}
 a:visited {color: %(vlink)s;}
 a:active {color: %(alink)s;}
 a:hover { color: %(colorhover)s; }
 table { border-collapse:collapse; border: 1px solid %(url)s; }
 th, td { border: 0px; padding: 2px; }
 td.url { background-color: %(url)s; color: %(colorlight)s; }
 td.valid { background-color: %(valid)s }
 td.error { background-color: %(error)s; color: %(colorlight)s; }
 td.warning { background-color: %(warning)s; color: %(colorlight)s; }
-->
</style>
</head>
<body>
<svg version="1.1" id="TRIMM_WORDMARK__x2B__TAGLINE" xmlns="http://www.w3.org/2000/svg" x="0" y="0" viewBox="0 0 819 236.5" xml:space="preserve" height="100px"><style type="text/css">.st0{fill:#46413c}.st1,.st2{display:none;fill:#f69227}.st2{fill:#46413c}.st3,.st4,.st5{display:none;fill:#d51d4d}.st4,.st5{fill:#f6cd2c}.st5{fill:#bbcc32}.st6{fill:#0d709a}.st7{fill:#fff}</style><g id="WORDMARK"><path id="M_2_" class="st0" d="M640.4 40.7h42.4l26.1 42.8L735 40.7h42.4v121.7h-40.5V102l-28 43.3h-.7l-28-43.3v60.3h-39.8V40.7z"/><path id="M" class="st0" d="M488.8 40.7h42.4l26.1 42.8 26.1-42.8h42.4v121.7h-40.5V102l-28 43.3h-.7l-28-43.3v60.3h-39.8V40.7z"/><path id="I" class="st0" d="M433.6 40.7h40.7v121.7h-40.7V40.7z"/><path id="R" class="st0" d="M304.7 40.7h59.5c19.9 0 34.5 4.6 43.8 13.9 7.4 7.4 11.1 17 11.1 28.9v.3c0 17-8 29.4-24 37.2l28.3 41.4H377l-22.9-34.8h-8.7v34.8h-40.7V40.7zM363 98.6c10.4 0 15.6-3.9 15.6-11.8v-.3c0-7.8-5.2-11.6-15.5-11.6h-17.7v23.8H363z"/><path id="T" class="st0" d="M213.7 75.1h-35.8V40.7h112.3v34.4h-35.8v87.3h-40.7V75.1z"/></g><path id="f69227" class="st1" d="M41.7 40.7h121.7v121.7H41.7z"/><path id="_x34_6413c" class="st2" d="M41.7 40.7h121.7v121.7H41.7z"/><path id="d71c4c" class="st3" d="M41.7 40.7h121.7v121.7H41.7z"/><path id="f7ce2b" class="st4" d="M41.7 40.7h121.7v121.7H41.7z"/><path id="becd00" class="st5" d="M41.7 40.7h121.7v121.7H41.7z"/><path id="_x30_d709a" class="st6" d="M41.7 40.7h121.7v121.7H41.7z"/><path class="st7" d="M122.3 85c-5.1 0-9.6 5.7-12.9 11.9-4.3-11.3-10.1-22.7-19.4-22.7-18.1.4-30.9 47.9-32.4 54.5h34.8c10.7-.1 13.1-8.4 13.1-8.4l-2.4-7.9s-3.2 8.2-10.7 8.2H68.8c2.2-6.9 11.9-37.8 21.3-37.8 8.6 0 15.8 27.5 18.1 33.7 2.3 6.2 7.3 12.2 15.9 12.2h23.4c-7-22.9-15.6-43.7-25.2-43.7zm0 8.3c5.6 0 14.5 27.4 14.5 27.4h-11c-5 0-8.4-1.2-10.9-8.3l-2.4-6.7c3.5-6.4 7.4-12.4 9.8-12.4z"/><path class="st0" d="M41.7 182.1h6.6c6.2 0 10.5 4.3 10.5 9.8v.1c0 5.6-4.3 9.9-10.5 9.9h-6.6v-19.8zm1.4 1.4v17.1h5.1c5.5 0 9-3.8 9-8.5v-.1c0-4.7-3.5-8.5-9-8.5h-5.1zM82.7 182.1h1.5v19.8h-1.5v-19.8zM108.7 192.1c0-5.2 3.7-9.9 9.5-9.9 3.1 0 5.1.9 7 2.5l-.9 1.1c-1.5-1.3-3.3-2.3-6.1-2.3-4.6 0-7.9 3.9-7.9 8.5v.1c0 4.9 3.1 8.6 8.2 8.6 2.4 0 4.7-1 6.1-2.2V193H118v-1.3h7.8v7.4c-1.7 1.5-4.4 2.9-7.5 2.9-6-.1-9.6-4.5-9.6-9.9zM150.4 182.1h1.5v19.8h-1.5v-19.8zM182.5 183.5h-6.9v-1.4h15.3v1.4H184v18.4h-1.5v-18.4zM219.1 182.1h1.4l9.1 19.8H228l-2.5-5.5H214l-2.5 5.5H210l9.1-19.8zm5.8 13l-5.2-11.4-5.2 11.4h10.4zM252.8 182.1h1.5v18.4h11.6v1.4h-13.1v-19.8zM304.7 192.1c0-5.5 4-9.9 9.6-9.9 3.4 0 5.5 1.3 7.4 3.1l-1 1c-1.7-1.6-3.6-2.8-6.4-2.8-4.6 0-8.1 3.7-8.1 8.5v.1c0 4.8 3.5 8.6 8.1 8.6 2.8 0 4.6-1.1 6.6-3l1 .9c-2 2-4.2 3.3-7.6 3.3-5.5 0-9.6-4.3-9.6-9.8zM345 182.1h8.3c2.4 0 4.4.8 5.6 1.9.9.9 1.5 2.3 1.5 3.7v.1c0 3.3-2.5 5.2-5.8 5.6l6.5 8.4h-1.9l-6.3-8.2h-6.5v8.2H345v-19.7zm8.1 10.3c3.3 0 5.8-1.7 5.8-4.5v-.1c0-2.7-2.1-4.3-5.7-4.3h-6.8v8.9h6.7zM391.4 182.2h1.4l9.1 19.7h-1.6l-2.5-5.5h-11.6l-2.5 5.5h-1.5l9.2-19.7zm5.9 12.9l-5.2-11.3-5.2 11.3h10.4zM424.8 182.1h13.9v1.4h-12.5v8.1h11.2v1.4h-11.2v9h-1.5v-19.9zM467.4 183.5h-6.9v-1.4h15.3v1.4h-6.9v18.4h-1.5v-18.4zM497.3 198.8l.9-1.1c2.1 2 4.1 2.9 6.9 2.9 2.9 0 4.9-1.6 4.9-3.8v-.1c0-2-1.1-3.2-5.4-4.1-4.6-.9-6.5-2.5-6.5-5.4v-.1c0-2.9 2.6-5.1 6.2-5.1 2.8 0 4.6.8 6.6 2.3l-.9 1.1c-1.8-1.6-3.6-2.2-5.7-2.2-2.8 0-4.7 1.6-4.7 3.6v.1c0 2 1 3.3 5.6 4.2 4.4.9 6.3 2.5 6.3 5.3v.1c0 3.1-2.7 5.2-6.4 5.2-3.1.2-5.5-.8-7.8-2.9zM535 182.1h1.4l7.9 11.7 7.9-11.7h1.4v19.8h-1.5v-17.2l-7.8 11.4h-.1l-7.8-11.4v17.2H535v-19.8zM585.5 182.2h1.4l9.1 19.7h-1.6l-2.5-5.5h-11.6l-2.5 5.5h-1.5l9.2-19.7zm5.8 12.9l-5.2-11.3-5.2 11.3h10.4zM618.9 182.1h1.4l13.6 17.2v-17.2h1.4v19.8h-1.1l-13.9-17.6v17.6h-1.4v-19.8zM658.7 198.8l.9-1.1c2.1 2 4.1 2.9 6.9 2.9 2.9 0 4.9-1.6 4.9-3.8v-.1c0-2-1.1-3.2-5.4-4.1-4.6-.9-6.5-2.5-6.5-5.4v-.1c0-2.9 2.6-5.1 6.2-5.1 2.8 0 4.6.8 6.6 2.3l-.9 1.1c-1.8-1.6-3.6-2.2-5.7-2.2-2.8 0-4.7 1.6-4.7 3.6v.1c0 2 1 3.3 5.6 4.2 4.4.9 6.3 2.5 6.3 5.3v.1c0 3.1-2.7 5.2-6.4 5.2-3.1.2-5.5-.8-7.8-2.9zM696.4 182.1h1.5v9.2h12.7v-9.2h1.5v19.8h-1.5v-9.3h-12.7v9.3h-1.5v-19.8zM736.6 182.1h1.5v19.8h-1.5v-19.8zM762.8 182.1h7.2c4.4 0 7.3 2.2 7.3 6v.1c0 4.2-3.6 6.3-7.7 6.3h-5.3v7.4h-1.5v-19.8zm6.9 11.1c3.7 0 6.2-1.9 6.2-4.9v-.1c0-3.1-2.4-4.8-6-4.8h-5.6v9.7h5.4z"/></svg>
"""


class TRIMMLogger (_Logger):
    """Logger with TRIMM styled HTML output."""

    LoggerName = 'trimm'

    LoggerArgs =  {
        "filename":        "trimm-linkchecker-out.html",
        'colorbackground': '#ffffff',
        'colorfont':       '#322E2A',
        'colorurl':        '#46413C',
        'colorhover':      '#0D709A',
        'colorborder':     '#000000',
        'colorlink':       '#337AB7',
        'colorwarning':    '#3BA557',
        'colorerror':      '#D61C4B',
        'colorok':         '#0D709A',
        'colorlight':      '#EEF2F4',
    }

    def __init__ (self, **kwargs):
        """Initialize default HTML color values."""
        args = self.get_args(kwargs)
        super(TRIMMLogger, self).__init__(**args)
        self.init_fileoutput(args)
        self.colorbackground = args['colorbackground']
        self.colorurl = args['colorurl']
        self.colorborder = args['colorborder']
        self.colorlink = args['colorlink']
        self.colorwarning = args['colorwarning']
        self.colorerror = args['colorerror']
        self.colorok = args['colorok']
        self.colorfont = args['colorfont']
        self.colorlight = args['colorlight']
        self.colorhover = args['colorhover']

    def part (self, name):
        """Return non-space-breakable part name."""
        return super(TRIMMLogger, self).part(name).replace(" ", "&nbsp;")

    def comment (self, s, **args):
        """Write HTML comment."""
        self.write(u"<!-- ")
        self.write(s, **args)
        self.write(u" -->")

    def start_output (self):
        """Write start of checking info."""
        super(TRIMMLogger, self).start_output()
        header = {
            "encoding": self.get_charset_encoding(),
            "title": "TRIMM " + configuration.App,
            "body": self.colorbackground,
            "link": self.colorlink,
            "vlink": self.colorlink,
            "alink": self.colorlink,
            "url": self.colorurl,
            "error": self.colorerror,
            "valid": self.colorok,
            "warning": self.colorwarning,
            "colorfont": self.colorfont,
            "colorlight": self.colorlight,
            "colorhover": self.colorhover,
        }
        self.write(HTML_HEADER % header)
        self.comment("Generated by TRIMM %s" % configuration.App)
        if self.has_part('intro'):
            self.write(u"<blockquote><h2> TRIMM "+configuration.App+
                       "</h2><br/>"+
                       (_("Start checking at %s") %
                       strformat.strtime(self.starttime))+
                       os.linesep+"<br/><br/>")
            self.check_date()
        self.flush()

    def log_url (self, url_data):
        """Write url checking info as HTML."""
        self.write_table_start()
        if self.has_part("url"):
            self.write_url(url_data)
        if url_data.name and self.has_part("name"):
            self.write_name(url_data)
        if url_data.parent_url and self.has_part("parenturl"):
            self.write_parent(url_data)
        if url_data.base_ref and self.has_part("base"):
            self.write_base(url_data)
        if url_data.url and self.has_part("realurl"):
            self.write_real(url_data)
        if url_data.dltime >= 0 and self.has_part("dltime"):
            self.write_dltime(url_data)
        if url_data.size >= 0 and self.has_part("dlsize"):
            self.write_size(url_data)
        if url_data.checktime and self.has_part("checktime"):
            self.write_checktime(url_data)
        if url_data.info and self.has_part("info"):
            self.write_info(url_data)
        if url_data.modified and self.has_part("modified"):
            self.write_modified(url_data)
        if url_data.warnings and self.has_part("warning"):
            self.write_warning(url_data)
        if self.has_part("result"):
            self.write_result(url_data)
        self.write_table_end()
        self.flush()

    def write_table_start (self):
        """Start html table."""
        self.writeln(u'<br/><table>')

    def write_table_end (self):
        """End html table."""
        self.write(u'</table><br/>')

    def write_id (self):
        """Write ID for current URL."""
        self.writeln(u"<tr>")
        self.writeln(u'<td>%s</td>' % self.part("id"))
        self.write(u"<td>%d</td></tr>" % self.stats.number)

    def write_url (self, url_data):
        """Write url_data.base_url."""
        self.writeln(u"<tr>")
        self.writeln(u'<td class="url">%s</td>' % self.part("url"))
        self.write(u'<td class="url">')
        self.write(u"`%s'" % cgi.escape(url_data.base_url))
        self.writeln(u"</td></tr>")

    def write_name (self, url_data):
        """Write url_data.name."""
        args = (self.part("name"), cgi.escape(url_data.name))
        self.writeln(u"<tr><td>%s</td><td>`%s'</td></tr>" % args)

    def write_parent (self, url_data):
        """Write url_data.parent_url."""
        self.write(u"<tr><td>"+self.part("parenturl")+
                   u'</td><td><a target="top" href="'+
                   url_data.parent_url+u'">'+
                   cgi.escape(url_data.parent_url)+u"</a>")
        if url_data.line > 0:
            self.write(_(", line %d") % url_data.line)
        if url_data.column > 0:
            self.write(_(", col %d") % url_data.column)
        if url_data.page > 0:
            self.write(_(", page %d") % url_data.page)
        if not url_data.valid:
            # on errors show HTML and CSS validation for parent url
            vhtml = validate_html % {'uri': url_data.parent_url}
            vcss = validate_css % {'uri': url_data.parent_url}
            self.writeln()
            self.writeln(u'(<a href="'+vhtml+u'">HTML</a>)')
            self.write(u'(<a href="'+vcss+u'">CSS</a>)')
        self.writeln(u"</td></tr>")

    def write_base (self, url_data):
        """Write url_data.base_ref."""
        self.writeln(u"<tr><td>"+self.part("base")+u"</td><td>"+
                     cgi.escape(url_data.base_ref)+u"</td></tr>")

    def write_real (self, url_data):
        """Write url_data.url."""
        self.writeln("<tr><td>"+self.part("realurl")+u"</td><td>"+
                     u'<a target="top" href="'+url_data.url+
                     u'">'+cgi.escape(url_data.url)+u"</a></td></tr>")

    def write_dltime (self, url_data):
        """Write url_data.dltime."""
        self.writeln(u"<tr><td>"+self.part("dltime")+u"</td><td>"+
                     (_("%.3f seconds") % url_data.dltime)+
                     u"</td></tr>")

    def write_size (self, url_data):
        """Write url_data.size."""
        self.writeln(u"<tr><td>"+self.part("dlsize")+u"</td><td>"+
                     strformat.strsize(url_data.size)+
                     u"</td></tr>")

    def write_checktime (self, url_data):
        """Write url_data.checktime."""
        self.writeln(u"<tr><td>"+self.part("checktime")+u"</td><td>"+
                     (_("%.3f seconds") % url_data.checktime)+u"</td></tr>")

    def write_info (self, url_data):
        """Write url_data.info."""
        sep = u"<br/>"+os.linesep
        text = sep.join(cgi.escape(x) for x in url_data.info)
        self.writeln(u'<tr><td valign="top">' + self.part("info")+
               u"</td><td>"+text+u"</td></tr>")

    def write_modified(self, url_data):
        """Write url_data.modified."""
        text = cgi.escape(self.format_modified(url_data.modified))
        self.writeln(u'<tr><td valign="top">' + self.part("modified") +
            u"</td><td>"+text+u"</td></tr>")

    def write_warning (self, url_data):
        """Write url_data.warnings."""
        sep = u"<br/>"+os.linesep
        text = sep.join(cgi.escape(x[1]) for x in url_data.warnings)
        self.writeln(u'<tr><td class="warning" '+
                     u'valign="top">' + self.part("warning") +
                     u'</td><td class="warning">' + text + u"</td></tr>")

    def write_result (self, url_data):
        """Write url_data.result."""
        if url_data.valid:
            self.write(u'<tr><td class="valid">')
            self.write(self.part("result"))
            self.write(u'</td><td class="valid">')
            self.write(cgi.escape(_("Valid")))
        else:
            self.write(u'<tr><td class="error">')
            self.write(self.part("result"))
            self.write(u'</td><td class="error">')
            self.write(cgi.escape(_("Error")))
        if url_data.result:
            self.write(u": "+cgi.escape(url_data.result))
        self.writeln(u"</td></tr>")

    def write_stats (self):
        """Write check statistic infos."""
        self.writeln(u'<br/><i>%s</i><br/>' % _("Statistics"))
        if self.stats.number > 0:
            self.writeln(_(
              "Content types: %(image)d image, %(text)d text, %(video)d video, "
              "%(audio)d audio, %(application)d application, %(mail)d mail"
              " and %(other)d other.") % self.stats.link_types)
            self.writeln(u"<br/>")
            self.writeln(_("URL lengths: min=%(min)d, max=%(max)d, avg=%(avg)d.") %
                         dict(min=self.stats.min_url_length,
                         max=self.stats.max_url_length,
                         avg=self.stats.avg_url_length))
        else:
            self.writeln(_("No statistics available since no URLs were checked."))
        self.writeln(u"<br/>")

    def write_outro (self):
        """Write end of check message."""
        self.writeln(u"<br/>")
        self.write(_("That's it.")+" ")
        if self.stats.number >= 0:
            self.write(_n("%d link checked.", "%d links checked.",
                       self.stats.number) % self.stats.number)
            self.write(u" ")
        self.write(_n("%d warning found", "%d warnings found",
             self.stats.warnings_printed) % self.stats.warnings_printed)
        if self.stats.warnings != self.stats.warnings_printed:
            self.write(_(" (%d ignored or duplicates not printed)") %
                (self.stats.warnings - self.stats.warnings_printed))
        self.write(u". ")
        self.write(_n("%d error found", "%d errors found",
             self.stats.errors_printed) % self.stats.errors_printed)
        if self.stats.errors != self.stats.errors_printed:
            self.write(_(" (%d duplicates not printed)") %
                (self.stats.errors - self.stats.errors_printed))
        self.writeln(u".")
        self.writeln(u"<br/>")
        num = self.stats.internal_errors
        if num:
            self.write(_n("There was %(num)d internal error.",
                "There were %(num)d internal errors.", num) % {"num": num})
            self.writeln(u"<br/>")
        self.stoptime = time.time()
        duration = self.stoptime - self.starttime
        self.writeln(_("Stopped checking at %(time)s (%(duration)s)") %
             {"time": strformat.strtime(self.stoptime),
              "duration": strformat.strduration_long(duration)})
        self.writeln(u'</blockquote><br/><hr><small><br/>')
        self.writeln(u'<a href="https://www.trimm.nl">TRIMM</a> Linkchecker<br/>')
        self.writeln(u'</small></body></html>')

    def end_output (self, **kwargs):
        """Write end of checking info as HTML."""
        if self.has_part("stats"):
            self.write_stats()
        if self.has_part("outro"):
            self.write_outro()
        self.close_fileoutput()
