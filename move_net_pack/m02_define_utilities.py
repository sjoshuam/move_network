'''Defines key function that are useful across the project'''

##### IMPORT CODE DEPENDENCIES

# import settings
from move_net_pack.m01_define_settings import Settings
settings = Settings()

# import built-in packages
import abc, datetime, pathlib



##### DEFINE CLASS TO HOLD REUSABLE FUNCTIONS
class Utilities:
    '''Define reusable @staticmethod functions'''

    def __init__(self, settings=settings):
        pass

    @staticmethod
    def govern_print_verbosity(str_method, settings=settings):
        '''The print strings for functions on this project are relatively
         verbose to facilitate development.  This wrapper provides a centralized
         way to silence those messages once the code is developed.'''

        def silent(*args, **kwargs):
            return ""
        
        if settings.execute_project['verbose']:
            return str_method
        else:
            return silent
        
    @staticmethod
    def time_execution(a_function, settings=settings, *args, **kwargs):
        '''Times the execution of a given function for development purposes.'''

        def exection_timer(*args, **kwargs):
            start_time = datetime.datetime.now()
            output = a_function(*args, **kwargs)
            if settings.execute_project['verbose']:
                end_time = datetime.datetime.now()
                elapsed_time = 'TIME TRIAL ({}): {}\n'.format(
                    a_function.__name__,end_time-start_time)
                print(elapsed_time)
            return output
        return exection_timer

        
##### TEST CLASS INSTANTIATION
if __name__ == '__main__':
    utilities = Utilities()

    ## test verbosity decorator
    @utilities.govern_print_verbosity
    def say_something(n):
        message = 'something\n' * n
        return message
    
    print(say_something(n=2))

    ## test timer decorator
    @utilities.time_execution
    def execute_something(n):
        for i in range(0, 10**n): 1+1
        return f'Executed {10**n} loops'

    execute_something(n=3)

        
##########==========##########==========##########==========##########==========
