# Global variables. Feel free to play around with these
# but please return them to their original values before you submit.
# HINT: Your code should be using these values, if I change them (and I will)
# your output should change accordingly
a0_weight = 5
a1_weight = 7
a2_weight = 8
term_tests_weight = 20
exam_weight = 45
exercises_weight = 10
quizzes_weight = 5

a0_max_mark = 25
a1_max_mark = 50
a2_max_mark = 100
term_tests_max_mark = 50
exam_max_mark = 100
exercises_max_mark = 10
quizzes_max_mark = 5
exam_pass_mark = 40
overall_pass_mark = 50

def get_max(component_name):
    '''(str) -> float
    Given the name of a course component (component_name),
    return the maximum mark for that component. This is used to allow the GUI
    to display the "out of" text beside each input field.
    REQ: component_name must be one of: a0,a1,a2,exerises,midterm,exam
    >>> get_max('a0')
    25
    >>> get_max('exam')
    100
    REQ: component_name in {'a0', 'a1', 'a2', 'exercises', 'term tests',
    'quizzes', 'exam'}
    '''
    # DO NOT EDIT THIS FUNCTION. This function exists to allow the GUI access
    # to some of the global variables. You can safely ignore this function
    # for the purposes of E2.
    if(component_name == 'a0'):
        result = a0_max_mark
    elif(component_name == 'a1'):
        result = a1_max_mark
    elif(component_name == 'a2'):
        result = a2_max_mark
    elif(component_name == 'exercises'):
        result = exercises_max_mark
    elif(component_name == 'term tests'):
        result = term_tests_max_mark
    elif(component_name == 'quizzes'):
        result = quizzes_max_mark
    else:
        result = exam_max_mark
    return result

def percentage(raw_mark, max_mark):
    ''' (float, float) -> float
    Return the percentage mark on a piece of work that received a mark of
    raw_mark where the maximum possible mark of max_mark.
    REQ: raw_mark >=0
    REQ: max_mark > 0
    REQ: raw_max <= max_mark
    >>> percentage(15, 20)
    75.0
    >>> percentage(4.5, 4.5)
    100.0
    '''
    #Return 
    return raw_mark / max_mark * 100


def contribution(raw_mark, max_mark, weight):
    ''' (float, float, float) -> float
    Given a piece of work where the student earned raw_mark marks out of a
    maximum of max_marks marks possible, return the number of marks it
    contributes to the final course mark if this piece of work is worth weight
    marks in the course marking scheme.
    REQ: raw_mark >=0
    REQ: max_mark > 0
    REQ: weight >= 0
    >>> contribution(13.5, 15, 10)
    9.0
    '''
    # start your own code here
    
    
    
    #Input 2 floats and returns a float    
def percentage(raw_mark, max_mark):
        ''' (float, float) -> float
            Return the percentage mark on a piece of work that received a mark of
            raw_mark where the maximum possible mark of max_mark.
            REQ: raw_mark >=0
            REQ: max_mark > 0
            REQ: raw_max <= max_mark
            >>> percentage(15, 20)
            75.0
            >>> percentage(4.5, 4.5)
            100.0
            '''        
        #Return
        return (((raw_mark)/(max_mark))*100)        
    
    #input 6 floats to return a float 
def term_work_mark(a0,a1,a2,exercises,quiz,term_test):
    '''(float,float,float,float,float,float)->float
        returns term work
        REQ: (a0,a1,a2,exercises,quiz,term_test)>=40
        >>>term_work_mark(25,50,100,10,5,50)
        55.0
        >>>term_work_mark(20,45,70,8,4,40)
        43.9
        '''    
    #calculations to fid the miderm mark for a student 
    Percenta0=(a0/a0_max_mark)*a0_weight
   
    Percenta1=(a1/a1_max_mark)*a1_weight 

    Percenta2=(a2/a2_max_mark)*a2_weight

    PercentE1=(exercises/exercises_max_mark)*exercises_weight

    PercentQ1=(quiz/quizzes_max_mark)*quizzes_weight

    PercentTT=(term_test/term_tests_max_mark)*term_tests_weight

    result=(Percenta0+Percenta1+Percenta2+PercentE1+PercentQ1+PercentTT)
       
    #return a float 
    return result         
        
def final_mark(a0,a1,a2,exercises,quiz,term_test,final_exam):
    '''(float,float,float,float,float,float,float)->float
        returns final mark
        REQ:(a0,a1,a2,exercises,quiz.term_test,final_exam)>=50
        >>>final_mark(25,50,100,10,5,50,100)
        100.0
        >>>final_mark(20, 45, 70, 8, 4, 40, 73)
        76.75
        '''    
    #Calls term work
    term_work_mark(a0,a1,a2,exercises,quiz,term_test)

    #Calculates percentexam
    PercentEXAM=(final_exam/exam_max_mark)*exam_weight
    
    #Calculates Final Mark    
    final_mark=(term_work_mark(a0,a1,a2,exercises,quiz,term_test)+PercentEXAM)
        
    #return
    return final_mark    
    
def is_pass(a0,a1,a2,exercises,quiz,term_test,final_exam):
    '''(float,float,float,float,float,float,float)->bool
       Returns treu if youre your final mark is more than 40% and your term mark is more than 50%
       REQ: final_mark>=40.0, term_mark>=50.0
       >>> is_pass(20, 45, 70, 8, 4, 40, 41)
       True
       >>> is_pass(20, 45, 70, 8, 4, 40, 39)
       False
       >>> is_pass(10, 21, 12, 2, 1, 15, 23)
       False
       '''
    #calls function
    final_mark(a0,a1,a2,exercises,quiz,term_test,final_exam)
    
    #function overall mark is equal to final mark which must be over 50
    final_overall_mark=(final_mark(a0,a1,a2,exercises,quiz,term_test,final_exam)>=overall_pass_mark) 
    
    #final exam mark must be greater than 40
    final_exam_mark= (final_exam>=exam_pass_mark)
     
    
    #boolean
    is_passed=(final_overall_mark and final_exam_mark)
    
    return is_passed