# -*- coding: utf-8 -*-
"""
    GradeSever.controller.download
    ~~~~~~~~~~~~~~~~~~~~~~~~~

    과목별 파일 다운로드

    :copyright: (c) 2015 by KookminUniv

"""

from flask.helpers import send_from_directory, session

from GradeServer.utils.loginRequired import login_required
from GradeServer.utils.checkInvalidAccess import check_invalid_access

from GradeServer.resource.sessionResources import SessionResources

from GradeServer.GradeServer_logger import Log
from GradeServer.GradeServer_blueprint import GradeServer


@GradeServer.route('/download_file/<courseId>_<courseName>')
@check_invalid_access
@login_required
def download_file(courseId, courseName):
    try:
        directory = '/mnt/shared/Problems/10004_HelloWorld/'
        filename = '10004_HelloWorld.zip'
        
        Log.info(session[SessionResources().const.MEMBER_ID] \
                 + ' download '\
                 + courseId + '_' + courseName)
        
        return send_from_directory(directory = directory, filename = filename)
    except Exception as e:
       Log.info(e)