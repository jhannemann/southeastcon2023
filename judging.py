import subprocess
import os.path
import glob

PROGRAM = 'problem1'
TEAM = 1

# paths are expected to be absolute
PROGRAMS_PATH = '/Users/jh/Developer/SoutheastCon2023/solutions/programs'
INPUTS_PATH = '/Users/jh/Developer/SoutheastCon2023/solutions/input'
SOLUTIONS_PATH = '/Users/jh/Developer/SoutheastCon2023/solutions/output'
OUTPUT_PATH = '/Users/jh/Developer/SoutheastCon2023/output'


def main():
    language, program = findProgrammingLanguage(PROGRAM, PROGRAMS_PATH)
    if language.compile_command is not None:
        print('Compiling ' + language.name + ' program ' + program)
        program = language.compile_program(program, OUTPUT_PATH)
        language.run_program(program, INPUTS_PATH, OUTPUT_PATH)
    else:
        language.run_program(program, INPUTS_PATH, OUTPUT_PATH)


class ProgrammingLanguage:
    name = None
    extension = None
    compile_command = None
    run_command = None

    def compile_program(program, output_path):
        assert False, 'compile_program not implemented'

    def run_program(self, program, input):
        assert False, 'run_program not implemented'


class CPP(ProgrammingLanguage):
    name = 'C++'
    extension = 'cpp'
    compile_command = 'g++'

    def compile_program(filename, output_path):
        path, file = os.path.split(filename)
        file_base_name = os.path.splitext(file)[0]
        output_file_name = os.path.join(output_path, file_base_name)
        command = [CPP.compile_command]
        command.append('-o')
        command.append(output_file_name)
        command.append(filename)
        for term in command:
            print(term, end=' ')
        print()
        output = subprocess.run(command, capture_output=True, check=True)
        return output_file_name

    def run_program(filename, input_path, output_path):
        files = glob.glob('input_*.txt', root_dir=input_path)
        path, file = os.path.split(filename)
        file_base_name = os.path.splitext(file)[0]
        output_file_name = os.path.join(output_path, file_base_name)
        for infile in files:
            input_file_name = os.path.join(input_path, infile)
            outfile = infile.replace('input', 'output')
            output_file_name = os.path.join(output_path, outfile)
            print(filename, '<', infile, '>', outfile)
            command = [filename]
            with open(input_file_name, 'r') as in_f, open(output_file_name,
                                                          'w') as out_f:
                output = subprocess.run(command, check=True, stdin=in_f,
                                        stdout=out_f)


class Java(ProgrammingLanguage):
    name = 'Java'
    extension = 'java'
    compile_command = 'javac'
    run_command = 'java'

    def compile_program(filename, output_path):
        path, file = os.path.split(filename)
        file_base_name = os.path.splitext(file)[0]
        output_file_name = os.path.join(output_path, file_base_name)
        command = [Java.compile_command]
        command.append('-d')
        command.append(output_path)
        command.append(filename)
        for term in command:
            print(term, end=' ')
        print()
        output = subprocess.run(command, capture_output=True, check=True)
        return output_file_name+'.class'

    def run_program(filename, input_path, output_path):
        files = glob.glob('input_*.txt', root_dir=input_path)
        path, file = os.path.split(filename)
        file_base_name = os.path.splitext(file)[0]
        output_file_name = os.path.join(output_path, file_base_name)
        for infile in files:
            input_file_name = os.path.join(input_path, infile)
            outfile = infile.replace('input', 'output')
            output_file_name = os.path.join(output_path, outfile)
            print(filename, '<', infile, '>', outfile)
            file_base_name = os.path.splitext(filename)[0]
            command = [Java.run_command, '-cp', path, os.path.splitext(file)[0]]
            with open(input_file_name, 'r') as in_f, open(output_file_name,
                                                          'w') as out_f:
                output = subprocess.run(command, check=True, stdin=in_f,
                                        stdout=out_f)


class Python(ProgrammingLanguage):
    name = 'Python'
    extension = 'py'
    run_command = 'python3'

    def run_program(filename, input_path, output_path):
        files = glob.glob('input_*.txt', root_dir=input_path)
        path, file = os.path.split(filename)
        file_base_name = os.path.splitext(file)[0]
        output_file_name = os.path.join(output_path, file_base_name)
        for infile in files:
            input_file_name = os.path.join(input_path, infile)
            outfile = infile.replace('input', 'output')
            output_file_name = os.path.join(output_path, outfile)
            print(filename, '<', infile, '>', outfile)
            command = [Python.run_command, filename]
            with open(input_file_name, 'r') as in_f, open(output_file_name,
                                                          'w') as out_f:
                output = subprocess.run(command, check=True, stdin=in_f,
                                        stdout=out_f)


PROGRAMMING_LANGUAGES = [Java]


def findProgrammingLanguage(filename, path):
    assert (os.path.exists(path))
    name = filename.strip()
    for language in PROGRAMMING_LANGUAGES:
        full_path = os.path.join(path, name + '.' + language.extension)
        print(full_path)
        if os.path.exists(full_path):
            return language, full_path
    assert False, 'Language not found'


if __name__ == '__main__':
    main()
