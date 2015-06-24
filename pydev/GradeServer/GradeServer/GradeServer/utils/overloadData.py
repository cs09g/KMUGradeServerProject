# -*- coding: utf-8 -*-
"""
    GradeSever.util.OverloadData
    ~~~~~~~~~~~~~~~~~~~~~~~~~

   Data Base Overload Data Inserting

    :author: seulgi choi
    :copyright: (c) 2015 by KookminUniv

"""

from datetime import datetime
from werkzeug.security import generate_password_hash

from GradeServer.py3Des.pyDes import *

from GradeServer.database import dao

from GradeServer.model.members import Members
from GradeServer.model.departmentsDetailsOfMembers import DepartmentsDetailsOfMembers
from GradeServer.model.registeredCourses import RegisteredCourses
from GradeServer.model.registrations import Registrations
from GradeServer.model.articlesOnBoard import ArticlesOnBoard
from GradeServer.model.languagesOfCourses import LanguagesOfCourses
from GradeServer.model.registeredProblems import RegisteredProblems
from GradeServer.model.submittedRecordsOfProblems import SubmittedRecordsOfProblems
from GradeServer.model.submittedFiles import SubmittedFiles
from GradeServer.model.submissions import Submissions


from GradeServer.resource.setResources import SETResources
from GradeServer.resource.otherResources import OtherResources


def insert_overload_data():
    
    #Generate Password
    tripleDes = triple_des(OtherResources().const.TRIPLE_DES_KEY,
                           mode = ECB,
                           IV = "\0\0\0\0\0\0\0\0",
                           pad = None,
                           padmode = PAD_PKCS5)
    try:
        # Course Input
        dao.add(RegisteredCourses(courseId = '2015100101',
                                  courseName = '전산학실습',
                                  startDateOfCourse = datetime.now(),
                                  endDateOfCourse = '2015-07-30 00:00:00',
                                  courseAdministratorId = 'admin'))
        dao.commit()
        dao.add(LanguagesOfCourses(courseId = '2015100101',
                                   languageIndex = 1))
        dao.add(LanguagesOfCourses(courseId = '2015100101',
                                   languageIndex = 2))
        dao.add(LanguagesOfCourses(courseId = '2015100101',
                                   languageIndex = 3))
        dao.add(LanguagesOfCourses(courseId = '2015100101',
                                   languageIndex = 4))
        dao.add(LanguagesOfCourses(courseId = '2015100101',
                                   languageIndex = 5))
        
        dao.commit()
    except Exception:
        dao.rollback()
    
    try:
        # Problem Input
        for i in range(10001, 10060):
            dao.add(RegisteredProblems(problemId = i,
                                       courseId = '2015100101',
                                       openDate = datetime.now(),
                                       closeDate = '2015-07-30 00:00:00',
                                       startDateOfSubmission = datetime.now(),
                                       endDateOfSubmission = '2015-07-30 00:00:00'))
            dao.commit()
            # Problem Record Input
            dao.add(SubmittedRecordsOfProblems(problemId = i,
                                               courseId = '2015100101',
                                               sumOfSubmissionCount = 2500,
                                               sumOfSolvedCount = 40 + (i - 10000),
                                               sumOfWrongCount = 600,
                                               sumOfRuntimeErrorCount = 750,
                                               sumOfCompileErrorCount = 1000,
                                               sumOfTimeOverCount = 150))
            dao.commit()
    except Exception:
        dao.rollback()
    
    # Board Input
    import socket
    try:
        for i in range(0, 100):
            dao.add(ArticlesOnBoard(isNotice = 'TRUE',
                                    writerId = 'master',
                                    title = 'Many Input Data Test' +str(i),
                                    content = 'astroluj',
                                    writerIp = socket.gethostbyname(socket.gethostname()),
                                    writtenDate = datetime.now()))
            dao.commit()
            # User Input
            for i in range(1, 101):
                id = 'user' + str(i)
                try:
                    dao.add(Members(memberId = id,
                                   password = generate_password_hash(tripleDes.encrypt(str(id))),
                                   memberName = id,
                                   authority = SETResources().const.USER,
                                   signedInDate = datetime.now()))
                    dao.commit()
                    dao.add(DepartmentsDetailsOfMembers(memberId = id,
                                                        collegeIndex = 1,
                                                        departmentIndex = 1))
                    dao.add(Registrations(memberId = id,
                                          courseId = '2015100101')) 
                except Exception:
                    dao.rollback()   
                dao.add(ArticlesOnBoard(writerId = id,
                                        courseId = '2015100101',
                                        title = 'Many Input Data Test' +str(i),
                                        content = 'astroluj',
                                        writerIp = socket.gethostbyname(socket.gethostname()),
                                        writtenDate = datetime.now()))
                dao.commit()
    except Exception:
        dao.rollback()