# 
# This file is part of the Lampadas Documentation System.
# 
# Copyright (c) 2000, 2001, 2002 David Merrill <david@lupercalia.net>.
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
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA
# 

from Globals import *
from Log import log
from BaseClasses import *
from Languages import languages
from DataLayer import lampadas, Doc, User
from SourceFiles import sourcefiles
from WebLayer import lampadasweb
from Widgets import widgets
from Sessions import sessions
from Lintadas import lintadas
import os

EDIT_ICON     = '<img src="|uri.base|images/edit.png" alt="Edit" height="20" width="20" '\
                'border="0" hspace="3" vspace="0" align="top">'
EDIT_ICON_MED = '<img src="|uri.base|images/edit.png" alt="Edit" height="28" width="28" '\
                'border="0" hspace="0" vspace="0" align="top">'
EDIT_ICON_BIG = '<img src="|uri.base|images/edit.png" alt="Edit" height="36" width="36" '\
                'border="0" hspace="0" vspace="0" align="top">'
TEXT_ICON     = '<img src="|uri.base|images/ascii.png" alt="Text" height="20" width="20" '\
                'border="0" hspace="3" vspace="0" align="top">'
TEXT_ICON_MED = '<img src="|uri.base|images/ascii.png" alt="Text" height="28" width="28" '\
                'border="0" hspace="0" vspace="0" align="top">'
TEXT_ICON_BIG = '<img src="|uri.base|images/ascii.png" alt="Text" height="36" width="36" '\
                'border="0" hspace="0" vspace="0" align="top">'
DL_ICON       = '<img src="|uri.base|images/package.png" alt="D/L" height="20" width="20" '\
                'border="0" hspace="3" vspace="0" align="top">'
DL_ICON_MED   = '<img src="|uri.base|images/package.png" alt="D/L" height="28" width="28" '\
                'border="0" hspace="0" vspace="0" align="top">'
DL_ICON_BIG   = '<img src="|uri.base|images/package.png" alt="D/L" height="36" width="36" '\
                'border="0" hspace="0" vspace="0" align="top">'

class Tables(LampadasCollection):

    def __init__(self):
        self.data = {}

    def bar_graph(self, value, max, lang):
        return str(value) + '/' + str(max)

    def doc(self, uri):
        if not sessions.session:
            return '|blknopermission|'
        elif sessions.session.user.can_edit(doc_id=uri.id)==0:
            return '|blknopermission|'

        box = WOStringIO('<table class="box" width="100%">')
        box.write('<tr><th colspan="6">|strdocdetails|</th></tr>')
        if uri.id > 0:
            lintadas.check_doc(uri.id)
            lintadas.import_doc_metadata(uri.id)
            doc = lampadas.docs[uri.id]
            box.write('<form method=GET action="/data/save/document" '\
                      'name="document">')
        else:

            # Create a new document
            doc = Doc()
            doc.lang = uri.lang
            doc.pub_status_code = 'P'
            doc.review_status_code = 'U'
            doc.tech_review_status_code = 'U'
            box.write('<form method=GET action="/data/save/newdocument" '\
                      'name="document">')
        box.write('''<input name="username" type="hidden" value="%s">
        <input name="doc_id" type="hidden" value="%s">
        ''' % (sessions.session.username, doc.id))
        box.write('''<tr><td class="label">|strtitle|</td>
        <td colspan="5">
        <input type="text" name="title" style="width:100%%" value="%s"></td>
        </tr>''' % doc.title)
        box.write('<tr>')
        box.write('<td class="label">|strstatus|</td><td>' + widgets.pub_status_code(doc.pub_status_code, uri.lang) + '</td>\n')
        box.write('<td class="label">|strtype|</td><td>' + widgets.type_code(doc.type_code, uri.lang) + '</td>\n')
        box.write('</tr>\n<tr>\n')
        box.write('<td class="label">|strversion|</td><td><input type=text name="version" value="' + doc.version + '"></td>\n')
        box.write('<td class="label">|strshort_title|</td><td><input type=text name="short_title" value="' + doc.short_title + '"></td>\n')
        box.write('</tr>\n<tr>\n')
        box.write('<td class="label">|strwriting|</td><td>' + widgets.review_status_code(doc.review_status_code, uri.lang) + '</td>\n')
        box.write('<td class="label">|straccuracy|</td><td>' + widgets.tech_review_status_code(doc.tech_review_status_code, uri.lang) + '</td>\n')
        box.write('</tr>\n<tr>\n')
        box.write('<td class="label">|strpub_date|</td><td><input type=text name="pub_date" maxlength="10" value="' + doc.pub_date + '"></td>\n')
        box.write('<td class="label">|strupdated|</td><td><input type=text name="last_update" value="' + doc.last_update + '"></td>\n')
        box.write('</tr>\n<tr>\n')
        box.write('<td class="label">|strpub_time|</td><td><input type=text name="pub_time" value="' + doc.pub_time + '"></td>\n')
        box.write('<td class="label">|strmirror_time|</td><td><input type=text name="mirror_time" value="' + doc.mirror_time + '"></td>\n')
        box.write('</tr>\n<tr>\n')
        box.write('<td class="label">|strtickle_date|</td><td><input type=text name="tickle_date" value="' + doc.tickle_date + '"></td>')
        box.write('<td class="label">|strisbn|</td><td><input type=text name="isbn" value="' + doc.isbn + '"></td>')
        box.write('</tr>\n<tr>\n')
        box.write('<td class="label">|strmaintained|</td><td>' + bool2yesno(doc.maintained) + '</td>\n')
        box.write('<td class="label">|strrating|</td><td>' + self.bar_graph(doc.rating, 10, uri.lang) + '</td>\n')
        box.write('</tr>\n<tr>\n')
        box.write('<td class="label">|strformat|</td>')
        if doc.format_code > '':
            box.write('<td>'  + lampadas.formats[doc.format_code].name[uri.lang] + '</td>\n')
        else:
            box.write('<td></td>\n')
        box.write('<td class="label">|strdtd|</td><td>%s %s</td>' % (doc.dtd_code, doc.dtd_version))
        box.write('</tr>\n<tr>\n')
        box.write('<td class="label">|strlanguage|</td><td>' + widgets.lang(doc.lang, uri.lang) + '</td>\n')
        box.write('<td class="label">|strmaint_wanted|</td><td>' + widgets.tf('maintainer_wanted', doc.maintainer_wanted, uri.lang) + '</td>\n')
        box.write('</tr>\n<tr>\n')
        box.write('<td class="label">|strlicense|</td><td>' + widgets.license_code(doc.license_code, uri.lang))
        box.write(' <input type=text name=license_version size="6" value="' + doc.license_version + '"></td>\n')
        box.write('<td class="label">|strcopyright_holder|</td><td><input type=text name=copyright_holder value="' + doc.copyright_holder + '"></td>\n')
        box.write('</tr>\n<tr>\n')
        box.write('<td class="label">|strtrans_master|</td><td colspan="3">' + widgets.sk_seriesid(doc.sk_seriesid) + '</td>\n')
        box.write('</tr>\n<tr>\n')
        box.write('<td class="label">|strreplacedby|</td><td colspan="3">' + widgets.replaced_by_id(doc.replaced_by_id) + '</td>\n')
        box.write('''
        </tr>
        <tr>
          <td class="label">|strabstract|</td>
          <td colspan="5"><textarea name="abstract" rows="6" cols="40" style="width:100%%" wrap>%s</textarea></td>
        </tr>
        <tr>
          <td class="label">|strshort_desc|</td>
          <td colspan="5"><input type=text name="short_desc" style="width:100%%" value="%s"></td>
        </tr>
        <tr>
          <td></td>
          <td><input type=submit name="save" value="|strsave|"></td>
        </tr>
        </table>
        </form>''' % (doc.abstract, doc.short_desc))
        return box.get_value()

    def docversions(self, uri):
        if not sessions.session:
            return '|blknopermission|'
        elif sessions.session.user.can_edit(doc_id=uri.id)==0:
            return '|blknopermission|'

        log(3, 'Creating docversions table')
        doc = lampadas.docs[uri.id]
        box = '''
        <table class="box" width="100%">
        <tr><th colspan="6">|strdocversions|</th></tr>
        <tr>
        <th class="collabel">|strversion|</th>
        <th class="collabel">|strdate|</th>
        <th class="collabel">|strinitials|</th>
        <th class="collabel">|strcomments|</th> 
        <th class="collabel" colspan="2">|straction|</th> 
        </tr>
        '''
        keys = doc.versions.sort_by('pub_date')
        for key in keys:
            version = doc.versions[key]
            box = box + '<form method=GET action="/data/save/document_version" name="document_version">'
            box = box + '<input name="rev_id" type=hidden value=' + str(version.id) + '>\n'
            box = box + '<input name="doc_id" type=hidden value=' + str(version.doc_id) + '>\n'
            box = box + '<tr>\n'
            box = box + '<td><input type=text name=version value="' + version.version + '"></td>\n'
            box = box + '<td><input type=text name=pub_date value="' + version.pub_date + '"></td>\n'
            box = box + '<td><input type=text name=initials size=3 maxlength=3 value="' + version.initials + '"></td>\n'
            box = box + '<td style="width:100%"><textarea name="notes" wrap=soft style="width:100%; height:100%">' + version.notes + '</textarea></td>\n'
            box = box + '<td><input type=checkbox name="delete">|strdel|</td>\n'
            box = box + '<td><input type=submit name="action" value="|strsave|"></td>\n'
            box = box + '</tr>\n'
            box = box + '</form>\n'
        box = box + '<form method=GET action="/data/save/newdocument_version" name="document_version">'
        box = box + '<input name="doc_id" type=hidden value=' + str(doc.id) + '>\n'
        box = box + '''
        <tr>
        <td><input type="text" name="version"></td>
        <td><input type="text" name="pub_date"></td>
        <td><input type="text" name="initials" size="3" maxlength="3"></td>
        <td style="width:100%"><textarea name="notes" wrap="soft" style="width:100%; height:100%"></textarea></td>
        <td></td><td><input type="submit" name="action" value="|stradd|"></td>
        </tr>
        </form>
        </table>
        '''
        return box
        

    def docfiles(self, uri):
        if not sessions.session:
            return '|blknopermission|'
        elif sessions.session.user.can_edit(doc_id=uri.id)==0:
            return '|blknopermission|'

        log(3, 'Creating docfiles table')
        doc = lampadas.docs[uri.id]
        
        box = WOStringIO('''<table class="box" width="100%%">
        <tr><th colspan="6">%s</th></tr>
        ''' % ('|strdocfiles|'))
        doc = lampadas.docs[uri.id]
        keys = doc.files.sort_by('filename')
        for key in keys:

            lintadas.check_file(key)
            docfile = doc.files[key]
            sourcefile = sourcefiles[key]
            box.write('<form method=GET action="/data/save/document_file" name="document_file">')
            box.write('<input type=hidden name="doc_id" value=' + str(doc.id) + '>\n')
            box.write('<input type=hidden name="filename" size=30 style="width:100%" value="' + docfile.filename + '">\n')
            box.write('<tr>\n')
            if sourcefile.errors.count() > 0:
                box.write('<td class="sectionlabel error" colspan="6"><a href="%ssourcefile/%s%s">%s</a></td>\n'
                    % (uri.base, docfile.filename, uri.lang_ext, docfile.filename))
            else:
                box.write('<td class="sectionlabel" colspan="6"><a href="%ssourcefile/%s%s">%s</a></td>\n'
                    % (uri.base, docfile.filename, uri.lang_ext, docfile.filename))
            box.write('</tr>\n')
            box.write('<tr>\n')
            box.write('<td class="label">|strprimary|</td>')
            box.write('<td>'  + widgets.tf('top', docfile.top, uri.lang) + '</td>\n')
            box.write('<td class="label">|strfilesize|</td>')
            box.write('<td>' + str(sourcefile.filesize) + '</td>\n')
            box.write('<td class="label">|strupdated|</td>')
            if sourcefile.modified > '':
                box.write('<td>' + sourcefile.modified + '</td>\n')
            else:
                box.write('<td>|strunknown|</td>\n')
            box.write('</tr>\n')
            box.write('<tr>\n')
            box.write('<td class="label">|strformat|</td>')
            if sourcefile.format_code > '':
                box.write('<td>'  + lampadas.formats[sourcefile.format_code].name[uri.lang] + '</td>\n')
            else:
                box.write('<td>|strunknown|</td>\n')
            box.write('<td class="label">|strfilemode|</td>')
            box.write('<td>' + widgets.filemode(sourcefile.filemode) + '</td>\n')
            box.write('''
            <td><input type="checkbox" name="delete">|strdelete|</td>
            <td><input type="submit" name="action" value="|strsave|"></td>
            </tr>
            ''')
            box.write('</form>')
        
        # Add a new docfile
        box.write('<tr>\n')
        box.write('<form method=GET action="/data/save/newdocument_file" name="document_file">')
        box.write('<input name="doc_id" type="hidden" value="' + str(doc.id) + '">\n')
        box.write('<td colspan="6"><input type="text" name="filename" size="30" style="width:100%"></td>\n')
        box.write('</tr>\n')
        box.write('<tr>\n')
        box.write('<td class="label">|strprimary|</td>')
        box.write('<td>'  + widgets.tf('top', 0, uri.lang) + '</td>\n')
        box.write('<td></td>\n')
        box.write('<td></td>\n')
        box.write('<td></td>\n')
        box.write('''
        <td><input type="submit" name="action" value="|stradd|"></td>
        </tr>
        </form>
        ''')
        box.write('</table>\n')
        return box.get_value()
        

    def docusers(self, uri):
        if not sessions.session:
            return '|blknopermission|'
        elif sessions.session.user.can_edit(doc_id=uri.id)==0:
            return '|blknopermission|'

        log(3, 'Creating docusers table')
        doc = lampadas.docs[uri.id]
        box = '''
        <table class="box" width="100%">
        <tr><th colspan="6">|strdocusers|</th></tr>
        <tr>
        <th class="collabel">|strusername|</th>
        <th class="collabel">|stractive|</th>
        <th class="collabel">|strrole|</th>
        <th class="collabel">|stremail|</th>
        <th class="collabel" colspan="2">|straction|</th>
        </tr>
        '''
        doc = lampadas.docs[uri.id]
        keys = doc.users.sort_by('username')
        odd_even = OddEven()
        for key in keys:
            docuser = doc.users[key]
            box = box + '<form method=GET action="/data/save/document_user" name="document_user">'
            box = box + '<input type=hidden name="doc_id" value=' + str(doc.id) + '>\n'
            box = box + '<input type=hidden name="username" value=' + docuser.username + '>\n'
            box = box + '<tr class="' + odd_even.get_next() + '">\n'
            if sessions.session:
                if sessions.session.user.admin==1 or sessions.session.user.sysadmin==1:
                    box = box + '<td><a href="|uri.base|user/' + docuser.username + '">' + docuser.username + '</a></td>\n'
                else:
                    box = box + '<td>' + docuser.username + '</td>\n'
            else:
                box = box + '<td>' + docuser.username + '</td>\n'
            box = box + '<td>' + widgets.tf('active', docuser.active, uri.lang) + '</td>\n'
            box = box + '<td>' + widgets.role_code(docuser.role_code, uri.lang) + '</td>\n'
            box = box + '<td><input type=text name=email size=15 value="' +docuser.email + '"></td>\n'
            box = box + '<td><input type=checkbox name="delete">|strdel|</td>\n'
            box = box + '<td><input type=submit name="action" value="|strsave|"></td>\n'
            box = box + '</tr>\n'
            box = box + '</form>\n'
        box = box + '<form method=GET action="/data/save/newdocument_user" name="document_user">'
        box = box + '<input name="doc_id" type=hidden value=' + str(doc.id) + '>\n'
        box = box + '<tr>\n'
        box = box + '<td>' + '<input type=text name="username"></td>\n'
        box = box + '<td>' + widgets.tf('active', 1, uri.lang) + '</td>\n'
        box = box + '<td>' + widgets.role_code('', uri.lang) + '</td>\n'
        box = box + '<td><input type=text name=email size=15></td>\n'
        box = box + '<td></td><td><input type=submit name="action" value="|stradd|"></td>'
        box = box + '</tr>\n'
        box = box + '</form>\n'
        box = box + '</table>\n'
        return box
        

    def doctopics(self, uri):
        if not sessions.session:
            return '|blknopermission|'
        elif sessions.session.user.can_edit(doc_id=uri.id)==0:
            return '|blknopermission|'

        log(3, 'Creating doctopics table')
        doc = lampadas.docs[uri.id]
        box = ''
        box = box + '<table class="box" width="100%">'
        box = box + '<tr><th colspan="2">|strdoctopics|</th></tr>\n'
        box = box + '<tr>\n'
        box = box + '<th class="collabel">|strtopic|</th>\n'
        box = box + '<th class="collabel">|straction|</th>\n'
        box = box + '</tr>\n'
        doc = lampadas.docs[uri.id]
        topic_codes = lampadas.topics.sort_by('sort_order')
        odd_even = OddEven()
        for topic_code in topic_codes:
            doctopic = doc.topics[topic_code]
            if doctopic:
                topic = lampadas.topics[topic_code]
                box = box + '<form method=GET action="/data/save/deldocument_topic" name="document_topic">'
                box = box + '<input type=hidden name="doc_id" value=' + str(doc.id) + '>\n'
                box = box + '<input type=hidden name="topic_code" value=' + topic_code + '>\n'
                box = box + '<tr class="' + odd_even.get_next() + '"><td><a href="|uri.base|topic/' + topic_code + '|uri.lang_ext|">' + topic.title[uri.lang] + '</a>'
                box = box + '</td>\n'
                box = box + '<td><input type=submit name="action" value="|strdelete|"></td>\n'
                box = box + '</tr>\n'
                box = box + '</form>\n'
        box = box + '<form method=GET action="/data/save/newdocument_topic" name="document_topic">'
        box = box + '<input name="doc_id" type=hidden value=' + str(doc.id) + '>\n'
        box = box + '<tr>\n'
        box = box + '<td>' + widgets.topic_code('', uri.lang) + '</td>\n'
        box = box + '<td><input type=submit name="action" value="|stradd|"></td>'
        box = box + '</tr>\n'
        box = box + '</form>\n'
        box = box + '</table>\n'
        return box


    def docnotes(self, uri):
        if not sessions.session:
            return '|blknopermission|'
        elif sessions.session.user.can_edit(doc_id=uri.id)==0:
            return '|blknopermission|'

        log(3, 'Creating docnotes table')
        doc = lampadas.docs[uri.id]
        box = ''
        box = box + '<table class="box" width="100%">'
        box = box + '<tr><th colspan="4">|strdocnotes|</th></tr>\n'
        box = box + '<tr>\n'
        box = box + '<th class="collabel">|strdate_time|</th>\n'
        box = box + '<th class="collabel">|strusername|</th>\n'
        box = box + '<th class="collabel">|strcomments|</th>\n'
        box = box + '<th class="collabel">|straction|</th>\n'
        box = box + '</tr>\n'
        doc = lampadas.docs[uri.id]
        note_ids = doc.notes.sort_by('date_entered')
        odd_even = OddEven()
        for note_id in note_ids:
            note = doc.notes[note_id]
            box = box + '<tr class="' + odd_even.get_next() + '">\n'
            box = box + '<td>' + note.date_entered + '</td>\n'
            box = box + '<td>' + note.creator + '</td>\n'
            box = box + '<td>' + note.notes + '</td>\n'
            box = box + '<td></td>\n'
            box = box + '</tr>\n'
        box = box + '<form method=GET action="/data/save/newdocument_note" name="document_note">'
        box = box + '<input name="doc_id" type=hidden value=' + str(doc.id) + '>\n'
        box = box + '<input name="creator" type=hidden value=' + sessions.session.username + '>\n'
        box = box + '<tr><td></td><td></td>\n'
        box = box + '<td><textarea name="notes" rows=5 cols=40 style="width:100%"></textarea></td>\n'
        box = box + '<td><input type=submit name="action" value="|stradd|"></td>'
        box = box + '</tr>\n'
        box = box + '</form>\n'
        box = box + '</table>\n'
        return box


    def doctranslations(self, uri):
        """
        Builds a table of all available translations of a document.
        Based on the DocTable.
        """
        log(3, 'Creating doctranslations table')
        doc = lampadas.docs[uri.id]
        return self.doctable(uri, sk_seriesid=doc.sk_seriesid,
                             columns={'|strlanguage|':  'lang',
                                      '|strversion|':   'version',
                                      '|strupdated|':   'last_update',
                                      '|strpub_date|':  'pub_date',
                                     })

    def errors(self, uri):
        """
        Builds a complete list of all errors reported by Lintadas.
        It uses docerrors() and docfileerrors(), and just concatenates
        all of their contents.
        """

        if not sessions.session:
            return '|blknopermission|'

        log(3, 'Creating errors table')
        doc_ids = lampadas.docs.sort_by('title')
        box = WOStringIO('')
        for doc_id in doc_ids:
            doc = lampadas.docs[doc_id]

            # Only display docs the user has rights to.
            if sessions.session.user.can_edit(doc_id=doc_id)==0:
                continue
            if doc.lang==uri.lang:
                uri.id = doc_id
                doctable = self.docerrors(uri)
                filestable = self.docfileerrors(uri)
                if doctable > '' or filestable > '':
                    box.write('<h1><a href="|uri.base|document_main/%s|uri.lang_ext|">%s</a>%s</h1>' % (str(doc.id), EDIT_ICON, doc.title))
                if doctable > '':
                    box.write('<p>' + doctable)
                if filestable > '':
                    box.write('<p>' + filestable)
        return box.get_value()

    def docerrors(self, uri):
        if not sessions.session:
            return '|blknopermission|'
        elif sessions.session.user.can_edit(doc_id=uri.id)==0:
            return '|blknopermission|'

        log(3, 'Creating docerrors table')
        doc = lampadas.docs[uri.id]
        
        if doc.errors.count()==0:
            return ''

        box = ''
        box = box + '<table class="box" width="100%">'
        box = box + '<tr><th colspan="2">|strdocerrs|</th></tr>\n'
        box = box + '<tr>\n'
        box = box + '<th class="collabel">|strid|</th>\n'
        box = box + '<th class="collabel">|strerror|</th>\n'
        box = box + '</tr>\n'
        err_ids = doc.errors.sort_by('date_entered')
        odd_even = OddEven()
        for err_id in err_ids:
            docerror = doc.errors[err_id]
            error = lampadas.errors[err_id]
            box = box + '<tr class="' + odd_even.get_next() + '">\n'
            box = box + '<td>' + str(docerror.err_id) + '</td>\n'
            box = box + '<td>' + error.name[uri.lang] + '</td>\n'
            box = box + '</tr>\n'
        box = box + '</table>\n'
        return box

    def filereports(self, uri):
        if not sessions.session:
            return '|blknopermission|'
        elif sessions.session.user.can_edit(doc_id=uri.id)==0:
            return '|blknopermission|'

        log(3, 'Creating filereports table')
        sourcefile = sourcefiles[uri.filename]

        box = ''
        box = box + '<table class="box" width="100%">'
        box = box + '<tr><th colspan="2">|strfilereports|</th></tr>\n'
        box = box + '<tr><th colspan="2" class="sectionlabel">|uri.filename|</th></tr>\n'
        report_codes = lampadasweb.file_reports.sort_by_lang('name', uri.lang)
        odd_even = OddEven()
        for report_code in report_codes:
            report = lampadasweb.file_reports[report_code]
            if report.only_cvs==0 or sourcefile.in_cvs==1:
                box = box + '<tr class="' + odd_even.get_next() + '">\n'
                box = box + '<td><a href="|uri.base|file_report/' + report.code + '/'
                box = box + uri.filename + uri.lang_ext + '">'
                box = box + report.name[uri.lang] + '</a></td>\n'
                box = box + '<td>' + report.description[uri.lang] + '</td>\n'
                box = box + '</tr>\n'
        box = box + '</table>\n'
        return box

    def filereport(self, uri):
        if not sessions.session:
            return '|blknopermission|'
        elif sessions.session.user.can_edit(doc_id=uri.id)==0:
            return '|blknopermission|'

        log(3, 'Creating filereport table')

        # Build and execute the command
        report = lampadasweb.file_reports[uri.code]
        command = report.command
        sourcefile = sourcefiles[uri.filename]

        # Write local filename in case script wants it.
        fh = open('/tmp/lampadas_localname.txt', 'w')
        fh.write(sourcefile.localname + '\n')
        fh.close()
        
        # Write CVS-relative filename in case script wants it.
        fh = open('/tmp/lampadas_filename.txt', 'w')
        fh.write(sourcefile.filename + '\n')
        fh.close()
        
        child_stdin, child_stdout, child_stderr  = os.popen3(command)
        stdout = child_stdout.read()
        stderr = child_stderr.read()
        child_stdin.close()
        child_stdout.close()
        child_stderr.close()

        box = ''
        box = box + '<table class="box" width="100%">'
        box = box + '<tr><th>' + report.name[uri.lang] + '</th></tr>\n'
        box = box + '<tr><td><h2>|stroutput|</h2><pre>' + stdout + '</pre></td></tr>\n'
        box = box + '<tr><td><h2>|strerrors|</h2><pre>' + stderr + '</pre></td></tr>\n'
        if sessions.session:
            if sessions.session.user.admin==1 or sessions.session.user.sysadmin==1:
                box = box + '<tr><td><h2>|strcommand|</h2><pre>' + command + '</pre></td></tr>\n'
        box = box + '</table>\n'
        return box

    def docfileerrors(self, uri):
        if not sessions.session:
            return '|blknopermission|'
        elif sessions.session.user.can_edit(doc_id=uri.id)==0:
            return '|blknopermission|'

        log(3, 'Creating docfileerrors table')
        doc = lampadas.docs[uri.id]

        if doc.files.error_count==0:
            return ''

        box = ''
        box = box + '<table class="box" width="100%">'
        box = box + '<tr><th colspan="3">|strfileerrs|</th></tr>\n'
        box = box + '<tr>\n'
        box = box + '<th class="collabel">|strid|</th>\n'
        box = box + '<th class="collabel">|strerror|</th>\n'
        box = box + '<th class="collabel">|strfilename|</th>\n'
        box = box + '</tr>\n'
        filenames = doc.files.sort_by('filename')
        odd_even = OddEven()
        for filename in filenames:
            sourcefile = sourcefiles[filename]
            err_ids = sourcefile.errors.sort_by('date_entered')
            for err_id in err_ids:
                fileerror = sourcefile.errors[err_id]
                error = lampadas.errors[err_id]
                box = box + '<tr class="' + odd_even.get_next() + '">\n'
                box = box + '<td>' + str(fileerror.err_id) + '</td>\n'
                box = box + '<td>' + error.name[uri.lang] + '</td>\n'
                box = box + '<td>' + sourcefile.filename + '</td>\n'
                box = box + '</tr>\n'
        box = box + '</table>\n'
        return box

    def letters(self, uri):
        log(3, 'Creating letter table')
        box = '<table class="tab"><tr>\n'
        for letter in string.uppercase:
            if letter==uri.letter:
                box = box + '<th>' + letter + '</th>\n'
            else:
                box = box + '<th><a href="|uri.base|' + uri.page_code + '/' + letter + '|uri.lang_ext|">' + letter + '</a></th>\n'
        box = box + '</tr></table>\n'
        return box
        
    def users(self, uri):
        if not sessions.session:
            return '|tabnopermission|'
        elif sessions.session.user.admin==0 and sessions.session.user.sysadmin==0:
            return '|tabnopermission|'
        elif uri.letter=='':
            return ''
        log(3, 'Creating users table')
        box = '<table class="box" width="100%"><tr><th colspan=2>|strusers|</th></tr>\n'
        box = box + '<tr>\n'
        box = box + '<th class="collabel">|strusername|</th>\n'
        box = box + '<th class="collabel">|strname|</th>\n'
        box = box + '</tr>\n';
        if uri.letter > '':
            usernames = lampadas.users.letter_keys(uri.letter)
            odd_even = OddEven()
            for username in usernames:
                user = lampadas.users[username]
                box = box + '<tr class="' + odd_even.get_next() + '">\n'
                box = box + '<td><a href="|uri.base|user/' + username + '|uri.lang_ext|">' + username + '</a></td>\n'
                box = box + '<td>' + user.name + '</a></td>\n'
                box = box + '</tr>\n'
        box = box + '</table>\n'
        return box

    def user(self, uri):
        if sessions.session==None:
            return '|blknopermission|'
        elif sessions.session.user.can_edit(username=uri.username)==0:
            return '|blknopermission|'

        if uri.username > '':
            user = lampadas.users[uri.username]
            if user==None:
                return '|blknotfound|'
            box = '<form method=GET action="/data/save/user" name="user">\n'
        else:
            user = User()
            box = '<form method=GET action="/data/save/newuser" name="user">\n'
        box = box + '<table class="box" width="100%">\n'
        box = box + '<tr><th colspan=2>|struserdetails|</th></tr>\n'
        box = box + '<tr><td class="label">|strusername|</td>'
        if user.username=='':
            box = box + '<td><input type=text name="username"></td>\n'
        else:
            box = box + '<td><input name="username" type=hidden value=' + user.username + '>' + user.username + '</td></tr>\n'
        box = box + '<tr><td class="label">|strfirst_name|</td><td><input type=text name=first_name size="15" value="' + user.first_name + '"></td></tr>\n'
        box = box + '<tr><td class="label">|strmiddle_name|</td><td><input type=text name=middle_name size="15" value="' + user.middle_name + '"></td></tr>\n'
        box = box + '<tr><td class="label">|strsurname|</td><td><input type=text name=surname size="15" value="' + user.surname + '"></td></tr>\n'
        box = box + '<tr><td class="label">|stremail|</td><td><input type=text name=email size="15" value="' + user.email + '"></td></tr>\n'
        box = box + '<tr><td class="label">|strstylesheet|</td><td><input type=text name=stylesheet size="12" value="' + user.stylesheet + '"></td></tr>\n'
        if user.username=='':
            box = box + '<tr><td class="label">|strpassword|</td><td><input type=text name=password size="12"></td></tr>\n'
        else:
            if sessions.session:
                if sessions.session.user.admin==1 or sessions.session.user.sysadmin==1:
                    box = box + '<tr><td class="label">|strpassword|</td><td>' + user.password + '</td></tr>\n'
            box = box + '<tr><td class="label">|strnewpassword|</td><td><input type=text name=password size="12"></td></tr>\n'
        if sessions.session.user and (sessions.session.user.admin > 0 or sessions.session.user.sysadmin > 0):
            box = box + '<tr><td class="label">|stradmin|</td><td>' + widgets.tf('admin', user.admin, uri.lang) + '</td></tr>\n'
        else:
            box = box + '<input name="admin" type="hidden" value="' + str(user.admin) + '">\n'
            box = box + '<tr><td class="label">|stradmin|</td><td>' + bool2yesno(user.admin) + '</td></tr>\n'
        if sessions.session.user and sessions.session.user.sysadmin > 0:
            box = box + '<tr><td class="label">|strsysadmin|</td><td>' + widgets.tf('sysadmin', user.sysadmin, uri.lang) + '</td></tr>\n'
        else:
            box = box + '<input name="sysadmin" type="hidden" value="' + str(user.sysadmin) + '">\n'
            box = box + '<tr><td class="label">|strsysadmin|</td><td>' + bool2yesno(user.sysadmin) + '</td></tr>\n'
        box = box + '<tr><td class="label">|strcomments|</td><td style="width:100%"><textarea rows=6 name="notes" wrap=soft style="width:100%;">' + user.notes + '</textarea></td></tr>\n'
        box = box + '<tr><td></td><td><input type=submit name=save value=|strsave|></td></tr>\n'
        box = box + '</table>\n'
        box = box + '</form>\n'
        return box
        
    def doctable(self, uri,
                 title=None,
                 pub_status_code=None,
                 type_code=None,
                 topic_code=None,
                 username=None,
                 maintained=None,
                 maintainer_wanted=None,
                 lang=None,
                 review_status_code=None,
                 tech_review_status_code=None,
                 pub_date=None,
                 last_update=None,
                 tickle_date=None,
                 isbn=None,
                 rating=None,
                 format_code=None,
                 dtd_code=None,
                 license_code=None,
                 copyright_holder=None,
                 sk_seriesid=None,
                 abstract=None,
                 short_desc=None,
                 columns={},
                 layout='compact',
                ):
        """
        Creates a listing of all documents which fit the parameters passed in.

        You can select a layout from "compact" or "block". Compact is onel line
        per document; block is a table per document. The block layout does
        not accept additional columns to be requested, and ignores the columns{}
        parameter.
        """

        log(3, "Creating doctable")
        colspan = 3 + len(columns)

        # Table header for compact layout
        if layout=='compact':
            box = WOStringIO('<table class="box" width="100%%"><tr><th colspan="%s">|strdoctable|</th></tr>\n'
                             % str(colspan))
            box.write('<tr><th class="collabel" colspan="3" align="center">|strtitle|</th>')
            for column in columns.keys():
                box.write('<th class="collabel">%s</td>' % column)
            box.write('</tr>\n')
        elif layout=='block':
            box = WOStringIO('')

        keys = lampadas.docs.sort_by("title")
        odd_even = OddEven()
        for key in keys:
            doc = lampadas.docs[key]

            # Don't include unpublished documents
            # except for admins and owners.
            if doc.pub_time=='' and (sessions.session==None or sessions.session.user.can_edit(doc_id=doc.id)==0):
                continue

            # Filter documents according to parameters passed in
            # by the calling routine.
            if not username==None:
                if doc.users[username]==None:
                    continue
            if not lang==None:
                if doc.lang <> lang:
                    continue
            if not pub_status_code==None:
                if doc.pub_status_code <> pub_status_code:
                    continue
            
            # If any other parameters were specified, limit the documents
            # to those which match the requirements.
            if not type_code==None:
                if doc.type_code <> type_code:
                    continue
            if not topic_code==None:
                topic = lampadas.topics[topic_code]
                if topic.docs[doc.id]==None:
                    continue
            if not maintained==None:
                if doc.maintained <> maintained:
                    continue
            if not maintainer_wanted==None:
                if doc.maintainer_wanted <> maintainer_wanted:
                    continue
            if not title==None:
                if doc.title.upper().find(title.upper())==-1:
                    continue
            if not review_status_code==None:
                if doc.review_status_code <> review_status_code:
                    continue
            if not review_status_code==None:
                if doc.review_status_code <> review_status_code:
                    continue
            if not tech_review_status_code==None:
                if doc.tech_review_status_code <> tech_review_status_code:
                    continue
            if not pub_date==None:
                if doc.pub_date <> pub_date:
                    continue
            if not last_update==None:
                if doc.last_update <> last_update:
                    continue
            if not tickle_date==None:
                if doc.tickle_date <> tickle_date:
                    continue
            if not isbn==None:
                if doc.isbn <> isbn:
                    continue
            if not rating==None:
                if doc.rating <> rating:
                    continue
            if not format_code==None:
                if doc.format_code <> format_code:
                    continue
            if not dtd_code==None:
                if doc.dtd_code <> dtd_code:
                    continue
            if not license_code==None:
                if doc.license_code <> license_code:
                    continue
            if not copyright_holder==None:
                if doc.copyright_holder.upper().find(copyright_holder.upper())==-1:
                    continue
            if not sk_seriesid==None:
                if doc.sk_seriesid.find(sk_seriesid)==-1:
                    continue
            if not abstract==None:
                if doc.abstract.upper().find(abstract.upper())==-1:
                    continue
            if not short_desc==None:
                if doc.short_desc.upper().find(short_desc.upper())==-1:
                    continue

            # Only show documents with errors if the user owns them
            if doc.errors.count() > 0 or doc.files.error_count > 0:
                if sessions.session==None:
                    continue
                elif sessions.session.user.can_edit(doc_id=doc.id)==0:
                    continue

            # Build the table for any documents that passed the filters
            topfile = doc.find_top_file()
            if topfile:
                sourcefile = sourcefiles[topfile.filename]
                txtfile = sourcefile.txtfile
            else:
                txtfile = ''
           
            if layout=='compact':
                box.write('<tr class="%s">\n<td>' % odd_even.get_next())
                if sessions.session and sessions.session.user.can_edit(doc_id=doc.id)==1:
                    box.write('<a href="|uri.base|document_main/%s|uri.lang_ext|">%s</a>' % (str(doc.id), EDIT_ICON))
                box.write('</td>\n<td>')
                if doc.pub_time > '':
                    box.write('<a href="|uri.base|docdownloads/%s/">%s</a>' % (str(doc.id), DL_ICON))
                box.write('</td>\n')

                # Format the title differently to flag its status
                if doc.pub_time > '':
                    box.write('<td style="width:100%%"><a href="|uri.base|doc/%s/index.html">%s</a></td>\n' % (str(doc.id), doc.title))
                elif sessions.session and sessions.session.user.can_edit(doc_id=doc.id)==1:
                    if doc.errors.count() > 0 or doc.files.error_count > 0:
                        box.write('<td style="width:100%%" class="error">%s</td>\n' % doc.title)
                    else:
                        box.write('<td style="width:100%%">%s</td>\n' % doc.title)

                for column in columns.keys():
                    box.write('<td>%s</td>\n' % getattr(doc, columns[column]))
                box.write('</tr>\n')

            # This is a blocky extended listing, fairly extended and with abstracts.
            elif layout=='block':
                if doc.errors.count() > 0 or doc.files.error_count > 0:
                    block_title = '<th colspan="4" class="error">' + doc.title + '</th>\n'
                else:
                    block_title = '<th colspan="4">' + doc.title + '</th>\n'

                if sessions.session and sessions.session.user.can_edit(doc_id=doc.id)==1:
                    block_editlink = '<td width="30" align="center"><a href="|uri.base|document_main/' + str(doc.id) + '|uri.lang_ext|">' + EDIT_ICON_MED + '</a></td>\n'
                else:
                    block_editlink = '<td width="30" align="center"></td>\n'

                if doc.pub_time > '':
                    block_viewlink = '<td width="30" align="center"><a href="|uri.base|doc/' + str(doc.id) + '/index.html">' + TEXT_ICON_MED + '</a></td>\n'
                else:
                    block_viewlink = '<td width="30" align="center"></td>\n'
                
                block_dllink = '<td width="30" align="center"><a href="|uri.base|docdownloads/' + str(doc.id) + '/">' + DL_ICON_MED + '</a></td>\n'
                block_abstract = '<td>' + doc.abstract + '</td>\n'
                
                box.write('<p><table class="box" width="100%%">\n' \
                          '<tr>%s</tr>' \
                          '<tr>%s%s%s%s</tr>' \
                          '</table>\n'
                          % (block_title,
                             block_editlink, block_viewlink, block_dllink, block_abstract))

        if layout=='compact':
            box.write('</table>\n')
        return box.get_value()

    def userdocs(self, uri, username=''):
        """
        Displays a DocTable containing documents linked to a user.
        The default is to display docs for the logged-on user.
        """
        if sessions.session==None:
            return '|nopermission|'
        if sessions.session.user.can_edit(username=username)==0:
            return '|nopermission|'
        if username > '':
            return self.doctable(uri, username=username)
        else:
            return self.doctable(uri, username=sessions.session.username)

    def section_menu(self, uri, section_code):
        log(3, "Creating section menu: " + section_code)
        section = lampadasweb.sections[section_code]
        box = WOStringIO('<table class="navbox"><tr><th>%s</th></tr>\n' \
                         '<tr><td>' % section.name[uri.lang])
        keys = lampadasweb.pages.sort_by('sort_order')
        for key in keys:
            page = lampadasweb.pages[key]
            if page.section_code==section.code:
                if lampadasweb.static and page.only_dynamic:
                    continue
                if page.only_registered and sessions.session==None:
                    continue
                if page.only_admin and (sessions.session==None or sessions.session.user.admin==0):
                    continue
                if page.only_sysadmin and (sessions.session==None or sessions.session.user.sysadmin==0):
                    continue
                box.write('<a href="|uri.base|%s|uri.lang_ext|">%s</a><br>\n' 
                    % (page.code, page.menu_name[uri.lang]))
        box.write('</td></tr></table>\n')
        return box.get_value()

    def section_menus(self, uri):
        log(3, "Creating all section menus")
        box = WOStringIO('')
        keys = lampadasweb.sections.sort_by('sort_order')
        menu_separator = ''
        for key in keys:
            section = lampadasweb.sections[key]
            if lampadasweb.static and section.static_count==0:
                continue
            if section.nonregistered_count==0 and (sessions.session==None):
                continue
            if section.nonadmin_count==0 and (sessions.session==None or sessions.session.user.admin==0):
                continue
            if section.nonsysadmin_count==0 and (sessions.session==None or sessions.session.user.sysadmin==0):
                continue
            box.write(menu_separator + self.section_menu(uri, section.code))
            menu_separator = '<p>'
        return box.get_value()

    def sitemap(self, uri):
        log(3, 'Creating sitemap')
        box = ''
        box = '<table class="box" width="100%"><tr><th>|strsitemap|</th></tr>\n'
        section_codes = lampadasweb.sections.sort_by('sort_order')
        page_codes = lampadasweb.pages.sort_by('sort_order')
        for section_code in section_codes:
            section = lampadasweb.sections[section_code]
            if section.static_count==0 and lampadasweb.static:
                continue
            if section.nonregistered_count==0 and sessions.session==None:
                continue
            if section.nonadmin_count==0 and (sessions.session==None or sessions.session.user.admin==0):
                continue
            if section.nonsysadmin_count==0 and (sessions.session==None or sessions.session.user.sysadmin==0):
                continue

            box = box + '<tr><th class="collabel">' +  section.name[uri.lang] + '</th></tr>\n'
            for page_code in page_codes:
                page = lampadasweb.pages[page_code]
                if page.section_code==section_code:
                    if page.only_dynamic and lampadasweb.static:
                        continue
                    if page.only_registered or page.only_admin or page.only_sysadmin > 0:
                        if sessions.session==None: continue
                    if page.only_admin > 0:
                        if sessions.session==None: continue
                        if sessions.session.user.admin==0 and sessions.session.user.sysadmin==0:
                            continue
                    if page.only_sysadmin > 0:
                        if sessions.session==None: continue
                        if sessions.session.user.sysadmin==0:
                            continue
                    box = box + '<tr><td><a href="|uri.base|' + page.code + '|uri.lang_ext|">' + page.menu_name[uri.lang] + '</a></td></tr>\n'
        box = box + '</table>\n'
        return box

# FIXME WOStringIO implemented below --nico

    def recent_news(self, uri):
        log(3, 'Creating recent news')
        box = WOStringIO('''<table class="box" width="100%">
        <tr><th colspan="2">|strrecentnews|</th></tr>
        <tr><th class="collabel">|strdate|</th><th class="collabel">|strnews|</th></tr>\n''')
        keys = lampadasweb.news.sort_by_desc('pub_date')
        odd_even = OddEven()
        for key in keys:
            news = lampadasweb.news[key]
            if not news.news[uri.lang]==None:
                box.write('''<tr class="%s"><td>%s</td><td>%s</td></tr>\n'''
                          % (odd_even.get_next(), news.pub_date, news.news[uri.lang]))
        box.write('</table>\n')
        return box.get_value()

    def navtopics(self, uri):
        if self['navtopics']==None:
            self['navtopics'] = LampadasCollection()
            self['navtopics'].html = LampadasCollection()
        if self['navtopics'].html[uri.lang]==None:
            log(3, 'Creating navtopics menu')
            box = WOStringIO('''<table class="navbox">
            <tr><th>|strtopics|</th></tr>
            <tr><td>''')
            keys = lampadas.topics.sort_by('sort_order')
            for key in keys:
                topic = lampadas.topics[key]
                if topic.parent_code=='':
                    box.write('<a href="|uri.base|topic/%s|uri.lang_ext|">%s</a><br>\n'
                              % (topic.code, topic.name[uri.lang]))
            box.write('</td></tr></table>\n')
            self['navtopics'].html[uri.lang] = box.get_value()
        return self['navtopics'].html[uri.lang]

    def tabtopics(self, uri):
        log(3, 'Creating tabtopics table')
        topic = lampadas.topics[uri.code]
        box = WOStringIO('''<table class="box" width="100%%">
        <tr><th>%s</th></tr>
        <tr><th class="collabel">|topic.description|</th></tr>
        ''' % topic.title[uri.lang])
        keys = lampadas.topics.sort_by('sort_order') 
        odd_even = OddEven()
        for key in keys:
            topic = lampadas.topics[key]
            if topic.parent_code==uri.code:
                box.write('<tr class="%s"><td><a href="|uri.base|topic/%s|uri.lang_ext|">%s</a></td></tr>\n'
                          % (odd_even.get_next(), topic.code, topic.name[uri.lang]))
        box.write('</td></tr>\n</table>\n')
        return box.get_value()

    def tabtopic(self, uri):
        log(3, 'Creating tabtopic table')
        topic = lampadas.topics[uri.code]
        box = '''<table class="box" width="100%%">
        <tr><th>%s</th></tr>
        <tr><td>%s</td><tr>
        </table>
        ''' % (topic.title[uri.lang], topic.description[uri.lang])
        return box

    def types(self, uri):
        log(3, 'Creating types menu')
        box = WOStringIO('''<table class="navbox">
        <tr><th>|strtypes|</th></tr>
        <tr><td>''')
        keys = lampadas.types.sort_by('sort_order')
        for key in keys:
            type = lampadas.types[key]
            box.write('<a href="|uri.base|type/%s|uri.lang_ext|">%s</a><br>\n'
                      % (type.code, type.name[uri.lang]))
        box.write('</td></tr>\n</table>\n')
        return box.get_value()

    def login(self, uri):
        if lampadasweb.static==1:
            return ''
        if sessions.session:
            log(3, 'Creating active user box')
            box = '''<table class="navbox">
            <tr><th>|stractive_user|</th></tr>
            <form name="logout" action="/data/session/logout">
            <input name="username" type="hidden" value="%s">
            <tr><td align="center">
            <a href="|uri.base|user/|session_username||uri.lang_ext|">|session_name|</a>
            <p>
            <input type="submit" name="logout"
            value="|strlog_out|"></td></tr>
            </form>
            </table>
            ''' % sessions.session.username
        else:
            log(3, 'Creating login box')
            box = '''<table class="navbox">
            <tr><th colspan="2">|strlogin|</th></tr>
            <form name="login" action="/data/session/login" method="GET">
            <tr>
              <td class="label">|strusername|</td>
              <td><input type="text" name="username" size="12"></td>
            </tr>
            <tr>
              <td class="label">|strpassword|</td>
              <td><input type="password" name="password" size="12"></td>
            </tr>
            <tr>
              <td align="center" colspan="2">
              <input type=submit name="login" value="login"><br>
              <a href="|uri.base|mailpass|uri.lang_ext|">|strmail_passwd|</a><br>
              <a href="|uri.base|newuser|uri.lang_ext|">|strcreate_acct|</a></td>
            </tr>
            </form> 
            </table>
            '''
        return box

    def navsessions(self, uri):
        if sessions.session and sessions.session.user.admin > 0:
            log(3, 'Creating navsessions table')
            box = WOStringIO('''<table class="navbox">
            <tr><th>|strsessions|</th></tr>
            <tr><td>
            ''')
            keys = sessions.sort_by('username')
            for key in keys:
                session = sessions[key]
                box.write('<a href="|uri.base|user/%s|uri.lang_ext|">%s</a><br>\n'
                          % (session.username, session.username))
            box.write('</td></tr>\n</table>\n')
            return box.get_value()
        return ''

    def tabsessions(self, uri):
        if sessions.session.user and sessions.session.user.admin > 0:
            log(3, 'Creating sessions table')
            box = WOStringIO('''<table class="box" width="100%">
            <tr><th colspan="4">|strsessions|</th></tr>
            <tr>
            <th class="collabel">|strusername|</th>
            <th class="collabel">|strip_address|</th>
            <th class="collabel">|strurl|</th>
            <th class="collabel">|strtimestamp|</th>
            </tr>
            ''')
            keys = sessions.sort_by_desc('timestamp')
            odd_even = OddEven()
            for key in keys:
                session = sessions[key]
                box.write('''<tr class="%s">
                <td><a href="|uri.base|user/%s|uri.lang_ext|">%s</a></td>
                <td>%s</td>
                <td>%s</td>
                <td>%s</td>
                </tr>
                ''' % (odd_even.get_next(),
                       session.username, session.username,
                       session.ip_address,
                       session.uri,
                       session.timestamp))
            box.write('</table>\n')
            return box.get_value()
        return '|nopermission|'

    def languages(self, uri):
        log(3, 'Creating languages table')
        box = WOStringIO('''<table class="navbox">
        <tr><th>|strlanguages|</th></tr>
        <tr><td>
        ''')
        keys = languages.sort_by_lang('name', uri.lang)
        for key in keys:
            language = lampadas.languages[key]
            if language.supported > 0:
                if uri.data > '':
                    add_data = '/' + uri.data
                else:
                    add_data = ''
                add_data = string.join(uri.data,'/')
                if add_data > '':
                    add_data = '/' + add_data
                box.write('<a href="|uri.base|%s%s.%s.html">%s</a><br>\n'
                          % (uri.page_code,
                             add_data,
                             language.code.lower(),
                             language.name[uri.lang]))
        box.write('</td></tr>\n</table>\n')
        return box.get_value()

    def tabsearch(self, uri):
        log(3, 'Creating tabsearch table')
        box = WOStringIO()
        box.write('''
            <table class="box">\n
            <form name="search" action="/data/search/document">
            <tr><th colspan="2">|strsearch|</th></tr>\n
            <tr><td class="label">|strtitle|</td><td>%s</td></tr>
            <tr><td class="label">|strstatus|</td><td>%s</td></tr>
            <tr><td class="label">|strtype|</td><td>%s</td></tr>
            <tr><td class="label">|strtopic|</td><td>%s</td></tr>
            <tr><td class="label">|strmaintained|</td><td>%s</td></tr>
            <tr><td class="label">|strmaint_wanted|</td><td>%s</td></tr>
            <tr><td class="label">|strlanguage|</td><td>%s</td></tr>
            <tr><td class="label">|strwriting|</td><td>%s</td></tr>
            <tr><td class="label">|straccuracy|</td><td>%s</td></tr>
            <tr><td class="label">|strpub_date|</td><td>%s</td></tr>
            <tr><td class="label">|strupdated|</td><td>%s</td></tr>
            <tr><td class="label">|strtickle_date|</td><td>%s</td></tr>
            <tr><td class="label">|strisbn|</td><td>%s</td></tr>
            <tr><td class="label">|strrating|</td><td>%s</td></tr>
            <tr><td class="label">|strformat|</td><td>%s</td></tr>
            <tr><td class="label">|strdtd|</td><td>%s</td></tr>
            <tr><td class="label">|strlicense|</td><td>%s</td></tr>
            <tr><td class="label">|strcopyright_holder|</td><td>%s</td></tr>
            <tr><td class="label">|strtrans_master|</td><td>%s</td></tr>
            <tr><td class="label">|strabstract|</td><td>%s</td></tr>
            <tr><td class="label">|strshort_desc|</td><td>%s</td></tr>
            <tr><td></td><td><input type="submit" value="|strsearch|"></td></tr>
            </form>
            </table>
            '''
            % (widgets.title(''),
               widgets.pub_status_code('', uri.lang),
               widgets.type_code('', uri.lang),
               widgets.topic_code('', uri.lang),
               widgets.tf('maintained', '', uri.lang),
               widgets.tf('maintainer_wanted', '', uri.lang),
               widgets.doc_lang(uri.lang, uri.lang),
               widgets.review_status_code('', uri.lang),
               widgets.tech_review_status_code('', uri.lang),
               widgets.pub_date(''),
               widgets.last_update(''),
               widgets.tickle_date(''),
               widgets.isbn(''),
               widgets.rating(''),
               widgets.format_code('', uri.lang),
               widgets.dtd_code(''),
               widgets.license_code('', uri.lang),
               widgets.copyright_holder(''),
               widgets.sk_seriesid(''),
               widgets.abstract(''),
               widgets.short_desc('')
               ))
        return box.get_value()
        
    def tabmailpass(self, uri):
        log(3, 'Creating mailpass table')
        box = '''<form name="mailpass" action="/data/save/mailpass">
        <table class="box" width="100%">
        <tr><th colspan="2">|strmail_passwd|</th></tr>
        <tr>
        <td><input type="text" name="email"></td>
        <td align="center"><input type="submit" name="mailpass" value="|strmail_passwd|"></td></tr>
        </table>
        </form>
        '''
        return box

    def tabsplashlanguages(self, uri):
        """Creates a customizable splash page for selecting a language.
           Each element gets a unique identifier such as 'p1', so a css
           stylesheet can exercise fine control over placement."""
        log(3, 'Creating tabslashlanguages table')
        box = WOStringIO('<p class="hide"><div class="map">\n' \
                         '<h1 id="p1">|strproject|</h1>\n')
        id = 1
        for key in languages.supported_keys():
            id = id + 1
            language = languages[key]
            box.write('<p id="p%s"><a href="%s.%s.html">%s</a></p>\n'
                % (str(id), 'home', key.lower(), language.name[language.code]))
        box.write('</div>')
        return box.get_value()

tables = Tables()
