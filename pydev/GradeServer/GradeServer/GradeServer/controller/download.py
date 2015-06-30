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
        # Absolute Path
        directory = '/mnt/shared/PastCourses/' + str(courseId) + '_' + courseName
        # File Name StudentId_MemberName.zip
        filename = session[SessionResources().const.MEMBER_ID] + '_'\
        + session[SessionResources().const.MEMBER_NAME] + '.zip'
        
        Log.info(session[SessionResources().const.MEMBER_ID] \
                 + ' download '\
                 + directory\
                 + '/'  + filename)
        
        return send_from_directory(directory = directory, filename = filename)
    except Exception as e:
       Log.info(str(e))
       
              # 메인 페이지로 옮기기
       from flask import redirect, url_for, flash
       from GradeServer.resource.routeResources import RouteResources
       flash('Not Found File')
       return redirect(url_for(RouteResources().const.SIGN_IN))