import sys
from DBManager import db_session
from DB.submissions import Submissions
from DB.submittedRecordsOfProblems import SubmittedRecordsOfProblems

STATUS = ['grading status', 'NeverSubmitted', 'Judging', 'Solved', 'TimeOver',
          'WrongAnswer', 'CompileError', 'RunTimeError', 'ServerError']

class DBUpdate(object):
    def __init__(self, stdNum, problemNum, courseNum, submitCount):
        self.stdNum = stdNum
        self.problemNum = problemNum
        self.courseNum = courseNum
        self.submitCount = submitCount
        
    def UpdateSubmissions(self, result, score, runTime, usingMem):
        try:
            db_session.query(Submissions).\
                filter_by(memberId = self.stdNum,
                          problemId = self.problemNum,
                          courseId = self.courseNum,
                          submissionCount = self.submitCount).\
                update(dict(status = STATUS.index(result),
                            score = score,
                            runTime = runTime,
                            usedMemory = usingMem,
                            solutionCheckCount = Submissions.solutionCheckCount+1))
            
        except Exception as e:
            db_session.rollback()
            self.UpdateServerError(self.stdNum, self.problemNum, self.courseNum, self.submitCount)
        
    def SubmittedRecordsOfProblems_CompileError(self):
        try:
            db_session.query(SubmittedRecordsOfProblems).\
                filter_by(problemId = self.problemNum,
                          courseId = self.courseNum).\
                          update(dict(sumOfSubmissionCount = SubmittedRecordsOfProblems.sumOfSubmissionCount + 1,
                                      sumOfCompileErrorCount = SubmittedRecordsOfProblems.sumOfCompileErrorCount + 1))
        
            db_session.commit()
        except Exception as e:
            db_session.rollback()
            self.UpdateServerError(self.stdNum, self.problemNum, self.courseNum, self.submitCount)
            
    def SubmittedRecordsOfProblems_Solved(self):
        try:
            db_session.query(SubmittedRecordsOfProblems).\
                    filter_by(problemId = self.problemNum,
                              courseId = self.courseNum).\
                    update(dict(sumOfSubmissionCount = SubmittedRecordsOfProblems.sumOfSubmissionCount + 1,
                                sumOfSolvedCount = SubmittedRecordsOfProblems.sumOfSolvedCount + 1))
        
            db_session.commit()
        except Exception as e:
            db_session.rollback()
            self.UpdateServerError(self.stdNum, self.problemNum, self.courseNum, self.submitCount)
            
    def SubmittedRecordsOfProblems_WrongAnswer(self):
        try:
            db_session.query(SubmittedRecordsOfProblems).\
                    filter_by(problemId = self.problemNum,
                              courseId = self.courseNum).\
                    update(dict(sumOfSubmissionCount = SubmittedRecordsOfProblems.sumOfSubmissionCount + 1,
                                sumOfWrongCount = SubmittedRecordsOfProblems.sumOfWrongCount + 1))
        
            db_session.commit()
        except Exception as e:
            db_session.rollback()
            self.UpdateServerError(self.stdNum, self.problemNum, self.courseNum, self.submitCount)
            
    def SubmittedRecordsOfProblems_TimbeOver(self):
        try:
            db_session.query(SubmittedRecordsOfProblems).\
                    filter_by(problemId = self.problemNum,
                              courseId = self.courseNum).\
                    update(dict(sumOfSubmissionCount = SubmittedRecordsOfProblems.sumOfSubmissionCount + 1,
                                sumOfTimeOverCount = SubmittedRecordsOfProblems.sumOfTimeOverCount + 1))
        
            db_session.commit()
        except Exception as e:
            db_session.rollback()
            self.UpdateServerError(self.stdNum, self.problemNum, self.courseNum, self.submitCount)
            
    def SubmittedRecordsOfProblems_RunTimeError(self):
        try:
            db_session.query(SubmittedRecordsOfProblems).\
                    filter_by(problemId = self.problemNum,
                              courseId = self.courseNum).\
                    update(dict(sumOfSubmissionCount = SubmittedRecordsOfProblems.sumOfSubmissionCount + 1,
                                sumOfRuntimeErrorCount = SubmittedRecordsOfProblems.sumOfRuntimeErrorCount + 1))
        
            db_session.commit()
        except Exception as e:
            db_session.rollback()
            self.UpdateServerError(self.stdNum, self.problemNum, self.courseNum, self.submitCount)

    @staticmethod        
    def UpdateServerError(stdNum, problemNum, courseNum, submitCount):
        try :
            db_session.query(Submissions).\
                filter_by(memberId = stdNum,
                          problemId = problemNum,
                          courseId = courseNum,
                          submissionCount = submitCount).\
                update(dict(status = 8,
                            score = 0,
                            runTime = 0,
                            usedMemory = 0))
            db_session.commit()
            print '...server error...'
        except Exception as e:
            db_session.rollback()
            raise e