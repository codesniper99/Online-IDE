import os
import sys
import filecmp
import re
import subprocess
from subprocess import CalledProcessError, TimeoutExpired
from django.http import FileResponse, HttpResponse, Http404, HttpResponseNotFound



STATUS_CODES = {
    200: 'OK',
    201: 'ACCEPTED',
    400: 'WRONG ANSWER',
    401: 'COMPILATION ERROR',
    402: 'RUNTIME ERROR',
    403: 'INVALID FILE',
    404: 'FILE NOT FOUND',
    408: 'TIME LIMIT EXCEEDED'
}


class Program:
    """ Class that handles all the methods of a user program """

    def __init__(self, filename, inputfile, timelimit, expectedoutputfile):
        """Receives a name of a file from the userIt must be a valid c, c++, java file """
        self.fileName = filename  # Full name of the source code file
        self.language = None  # Language
        self.name = None  # File name without extension
        self.inputFile = inputfile  # Input file
        self.expectedOutputFile = expectedoutputfile  # Expected output file
        self.actualOutputFile = "outputn.txt"  # Actual output file
        self.timeLimit = timelimit  # Time limit set for execution in seconds
        
        # print(str(self.fileName))
        # print(str(self.language))
        # print(str(self.inputFile))
        # print(str(self.expectedOutputFile))

    def isvalidfile(self):
        """ Checks if the filename is valid """
        # print(str(self.fileName))
        # try:
        #     print(str(self.fileName))
        # except CalledProcessError as e:
        #     print(e.output)
        validfile = re.compile("^(\S+)\.(java|cpp|c|py)$")

        matches = validfile.match(self.fileName)
        # print(matches.group(0))
        if matches:
            self.name, self.language = matches.groups()
            return True
        return False

    def compile(self):
        """ Compiles the given program, returns status code and errors """

        # Remove previous executables
        dir_path = os.path.dirname(os.path.realpath(__file__))
        lenth =len(dir_path)
        root_path1=dir_path[0:lenth-4]
        path = root_path1+"media/documents/"
        print(os.getcwd())

        os.chdir(path)
        print(os.getcwd())
        # print("\n\n")
        if os.path.isfile(self.name):
            os.remove(self.name)

        # Check if files are present
        if not os.path.isfile(self.fileName):
            print(os.path.isfile("hello.cpp"))
            # path2 = "C:\\Users\\Admin\\Desktop\\LMSWeb\\"
            # os.chdir(path2)
            return 404, 'Missing file'

        # Check language
        cmd = None
        if self.language == 'java':
            cmd = ["javac",self.fileName]#'javac {}'.format(self.fileName)
        elif self.language == 'c':
            cmd = ["gcc","-o",self.name,self.fileName]#'gcc -o {0} {1}'.format(self.name, self.fileName)
        elif self.language == 'cpp':
            cmd = ["g++","-o",self.name,self.fileName]#'g++ -o {0} {1}'.format(self.name, self.fileName)

        # Invalid files
        if cmd is None:
            # path2 = "C:\\Users\\Admin\\Desktop\\LMSWeb\\"
            # os.chdir(path2)
            return 403, 'File is of invalid type'

        try:
                
            proc = subprocess.run(
                cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                universal_newlines=True
            )

            # print(proc.args)
            # Check for errors
            if proc.returncode != 0:
                # path2 = "C:\\Users\\Admin\\Desktop\\LMSWeb\\"
                # os.chdir(path2)
                return 401, proc.stderr
            else:
                # path2 = "C:\\Users\\Admin\\Desktop\\LMSWeb\\"
                # os.chdir(path2)
                return 200, None
        except CalledProcessError as e:
            print(e.output)

    def run(self):
        """ Runs the executable, returns status code and errors """

        # Check if files are present
        print("\n")
        print(os.getcwd())
        print("\n")
        if not os.path.isfile(self.fileName) :
            dir_path = os.path.dirname(os.path.realpath(__file__))
            lenth =len(dir_path)
            root_path1=dir_path[0:lenth-4]
            path2 = root_path1+"media/documents/"
            os.chdir(path2)
            return 404, 'Missing executable file'

        # Check language
        cmd = None
        if self.language == 'java':
            cmd = 'java {}'.format(self.name)
        elif self.language in ['c', 'cpp']:
            cmd = self.name
        elif self.language == 'py':
            cmd = 'python {}'.format(self.fileName)

        # Invalid files
        if cmd is None:
            dir_path = os.path.dirname(os.path.realpath(__file__))
            lenth =len(dir_path)
            root_path=dir_path[0:lenth-4]
            
            path2 = root_path+"media/documents/"
            os.chdir(path2)
            return 403, 'File is of invalid type'

        try:
            with open('outputn.txt', 'w') as fout:
                fin = None
                if self.inputFile and os.path.isfile(self.inputFile):
                    fin = open(self.inputFile, 'r')
                proc = subprocess.run(
                    cmd,
                    stdin=fin,
                    stdout=fout,
                    stderr=subprocess.PIPE,
                    timeout=float(self.timeLimit),
                    universal_newlines=True
                )

            # Check for errors
            if proc.returncode != 0:
                dir_path = os.path.dirname(os.path.realpath(__file__))
                lenth =len(dir_path)
                root_path=dir_path[0:lenth-4]
                path2 = root_path+"media/documents/"
                os.chdir(path2)
                return 402, proc.stderr
            else:
                dir_path = os.path.dirname(os.path.realpath(__file__))
                lenth =len(dir_path)
                root_path=dir_path[0:lenth-4]
                path2 = root_path+"media/documents/"
                os.chdir(path2)
                return 200, None
        except TimeoutExpired as tle:
            # print(tle.output)
            dir_path = os.path.dirname(os.path.realpath(__file__))
            lenth =len(dir_path)
            root_path=dir_path[0:lenth-4]
            path2 = root_path+"media/documents/"
            os.chdir(path2)
            return 408, tle
        except CalledProcessError as e:
            print(e.output)

        # Perform cleanup
        if self.language == 'java':
            os.remove('{}.class'.format(self.name))
        elif self.language in ['c', 'cpp']:
            os.remove(self.name)

    def match(self):      
        dir_path = os.path.dirname(os.path.realpath(__file__))
        lenth =len(dir_path)
        root_path=dir_path[0:lenth-4]
        path2 = root_path+"media/documents/"
        os.chdir(path2)
        print(str(os.path.isfile(self.actualOutputFile))+"\n")
        print(str(os.path.isfile(self.expectedOutputFile)))
        print(os.getcwd()+"\n")
        print(str((self.actualOutputFile))+"\n")
        print(str((self.expectedOutputFile)))
            
        if os.path.isfile(self.actualOutputFile) and os.path.isfile(self.expectedOutputFile):
            result = filecmp.cmp(self.actualOutputFile, self.expectedOutputFile)
            if result:
                dir_path = os.path.dirname(os.path.realpath(__file__))
                lenth =len(dir_path)
                root_path=dir_path[0:lenth-4]
                path2 = root_path+"media/documents/"
                os.chdir(path2)
                return 201, None
            else:
                dir_path = os.path.dirname(os.path.realpath(__file__))
                lenth =len(dir_path)
                root_path=dir_path[0:lenth-4]
                path2 = root_path+"media/documents/"
                os.chdir(path2)
                return 400, None
        else:
            print((self.actualOutputFile))
            print("\n")
            print(str(self.expectedOutputFile))
            dir_path = os.path.dirname(os.path.realpath(__file__))
            lenth =len(dir_path)
            root_path=dir_path[0:lenth-4]
            path2 = root_path+"media/documents/"
            os.chdir(path2)
            print(os.getcwd()+"\n")
            return 404, 'Missing output files1'


def codechecker(filename, inputfile, expectedoutput, timeout=1, check=True):

    # print(str(filename))
    # print(str(inputfile))
    # print(str(expectedoutput))
    dir_path = os.path.dirname(os.path.realpath(__file__))
    lenth =len(dir_path)
    root_path1=dir_path[0:lenth-4]
    newprogram = Program(
        filename=filename,
        inputfile=inputfile,
        timelimit=timeout,
        expectedoutputfile=expectedoutput,
       
    )


    if newprogram.isvalidfile():
        print('Executing code checker...')
        # print(newprogram.language)
        if newprogram.language != 'py':
            # Compile program
            compileResult, compileErrors = newprogram.compile()
            print('Compiling... {0}({1})'.format(STATUS_CODES[compileResult], compileResult), flush=True)
            if compileErrors is not None:
                sys.stdout.flush()
                print(compileErrors, file=sys.stderr)
                exit(0)

        # Run program
        runtimeResult, runtimeErrors = newprogram.run()
        print('Running... {0}({1})'.format(STATUS_CODES[runtimeResult], runtimeResult), flush=True)

        if runtimeErrors is not None:
            sys.stdout.flush()
            print(runtimeErrors, file=sys.stderr)
            exit(0)

        if check:
            # Match expected output
            matchResult, matchErrors = newprogram.match()
            print('Verdict2... {0}({1})'.format(STATUS_CODES[matchResult], matchResult), flush=True)
            if matchErrors is not None:
                sys.stdout.flush()
                print(matchErrors, file=sys.stderr)
                exit(0)
            return STATUS_CODES[matchResult]
    else:
        print('FATAL: Invalid file', file=sys.stderr)


if __name__ == '__main__':

    codechecker(
        filename='yahoo.cpp',               # Source code file
        inputfile='input.txt',                  # Input file
        expectedoutput='output.txt',         # Expected output
        timeout=1,                              # Time limit
        check=True   ,                           # Set to true to check actual output against expected output
        
    )
