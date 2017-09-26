# -*- coding: utf-8 -*-

from ExtractAPI import get_desciption
from ExtractAPI import get_error_classes
import selenium

if __name__ == '__main__':
    error_url = 'http://help.eclipse.org/oxygen/topic/org.eclipse.jdt.doc.isv/reference/api/org/eclipse/jdt/launching/sourcelookup/ArchiveSourceLocation.html'
    print(get_desciption(error_url))