'''Defines key function that are useful across the project'''

##### IMPORT CODE DEPENDENCIES

# import settings
from move_net_pack.m02_define_settings import Settings
settings = Settings()

# import built-in packages
import datetime, sys, io
import concurrent.futures as futures


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

    @staticmethod
    def run_in_parallel(iterable, mapper, reducer, cpus=settings.execute_project['cpus']):
        '''Executes task in parallel processes, applying map/reduce approach'''
        splits = min([(cpus//5)*4, int(len(iterable)**0.5)])

        # split up iterable to fascilitate parallelization
        splits = [i%splits for i in range(0,len(iterable))]
        result = [list() for i in range(min(splits), max(splits)+1)]
        for i in range(0, len(iterable)):
            result[splits[i]].append(iterable[i])

        # execute in parallel
        with futures.ProcessPoolExecutor() as executor:
            result = executor.map(mapper, result)
            result = list(result)
        return reducer(result)
    
    @staticmethod
    def capture_output(x) -> str:
            sys.stdout = io.StringIO()
            print(x)
            x = sys.stdout.getvalue()
            sys.stdout = sys.__stdout__
            return x


        
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

    ## tests parallelizer
    def a_mapper(x):
        return [i*10 for i in x]
    a_list = list(range(0, 6))

    a_result = utilities.run_in_parallel(
        iterable=a_list, mapper=a_mapper, reducer=list)
    print(f'{settings.execute_project['cpus']} cpus, {len(a_list)} iterables')
    print(a_result)

        
##########==========##########==========##########==========##########==========
