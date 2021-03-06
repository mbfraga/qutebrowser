# vim: ft=python fileencoding=utf-8 sts=4 sw=4 et:

# Copyright 2016-2017 Florian Bruhin (The Compiler) <mail@qutebrowser.org>
#
# This file is part of qutebrowser.
#
# qutebrowser is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# qutebrowser is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with qutebrowser.  If not, see <http://www.gnu.org/licenses/>.

import pytest

from qutebrowser.browser import downloads, qtnetworkdownloads


def test_download_model(qapp, qtmodeltester, config_stub, cookiejar_and_cache):
    """Simple check for download model internals."""
    manager = qtnetworkdownloads.DownloadManager(win_id=0)
    model = downloads.DownloadModel(manager)
    qtmodeltester.check(model)


@pytest.mark.parametrize('url, title, out', [
    ('http://qutebrowser.org/INSTALL.html',
     'Installing qutebrowser | qutebrowser',
     'Installing qutebrowser _ qutebrowser.html'),
    ('http://qutebrowser.org/INSTALL.html',
     'Installing qutebrowser | qutebrowser.html',
     'Installing qutebrowser _ qutebrowser.html'),
    ('http://qutebrowser.org/INSTALL.HTML',
     'Installing qutebrowser | qutebrowser',
     'Installing qutebrowser _ qutebrowser.html'),
    ('http://qutebrowser.org/INSTALL.html',
     'Installing qutebrowser | qutebrowser.HTML',
     'Installing qutebrowser _ qutebrowser.HTML'),
    ('http://qutebrowser.org/',
     'qutebrowser | qutebrowser',
     'qutebrowser _ qutebrowser.html'),
    ('https://github.com/qutebrowser/qutebrowser/releases',
     'Releases · qutebrowser/qutebrowser',
     'Releases · qutebrowser_qutebrowser.html'),
    ('http://qutebrowser.org/index.php',
     'qutebrowser | qutebrowser',
     'qutebrowser _ qutebrowser.html'),
    ('http://qutebrowser.org/index.php',
     'qutebrowser | qutebrowser - index.php',
     'qutebrowser _ qutebrowser - index.php.html'),
    ('https://qutebrowser.org/img/cheatsheet-big.png',
     'cheatsheet-big.png (3342×2060)',
     None),
    ('http://qutebrowser.org/page-with-no-title.html',
     '',
     None),
])
def test_page_titles(url, title, out):
    assert downloads.suggested_fn_from_title(url, title) == out


class TestDownloadTarget:

    def test_base(self):
        with pytest.raises(NotImplementedError):
            downloads._DownloadTarget()

    def test_filename(self):
        target = downloads.FileDownloadTarget("/foo/bar")
        assert target.filename == "/foo/bar"

    def test_fileobj(self):
        fobj = object()
        target = downloads.FileObjDownloadTarget(fobj)
        assert target.fileobj is fobj

    def test_openfile(self):
        target = downloads.OpenFileDownloadTarget()
        assert target.cmdline is None

    def test_openfile_custom_command(self):
        target = downloads.OpenFileDownloadTarget('echo')
        assert target.cmdline == 'echo'

    @pytest.mark.parametrize('obj', [
        downloads.FileDownloadTarget('foobar'),
        downloads.FileObjDownloadTarget(None),
        downloads.OpenFileDownloadTarget(),
    ])
    def test_class_hierarchy(self, obj):
        assert isinstance(obj, downloads._DownloadTarget)
