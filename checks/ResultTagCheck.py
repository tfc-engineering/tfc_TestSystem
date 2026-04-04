import pathlib

from tfc_PyFactory.InputParameters import InputParameters
file_path = str(pathlib.Path(__file__).parent.resolve()) + "/"

import sys
sys.path.append(file_path + "../../")

import tfc_PyFactory
from tfc_PyFactory import *

from .CheckBase import *

import ast

class ResultTagCheck(CheckBase):
    '''Checks for presence or abscence of a string in the output of a test. if
    present a designated word can be stored, along with a tag, as a result.'''
    @staticmethod
    def getInputParameters() -> InputParameters:
        params = CheckBase.getInputParameters()

        params.addRequiredParam("line_key", ParameterType.STRING,
                                "The string to find in order to identify the "
                                "line of interest.")
        params.addRequiredParam("word_number", ParameterType.INTEGER,
                                "The index of the word to turn into a tagged_result")
        params.addRequiredParam("result_tag", ParameterType.STRING,
                                "String name of the tag to which the result will be assigned.")
        params.addOptionalParam("reverse_line_traverse", False,
                                "If true will reverse the traversal of file lines.")

        params.addOptionalParam("fail_if_present", False,
                                "Inverts the check. Fails if the line_key is indeed found.")

        return params


    def __init__(self, params: InputParameters) -> None:
        super().__init__(params)

        self.line_key_ = params.getParam("line_key").getStringValue()

        self.word_number_ = params.getParam("word_number").getIntegerValue()

        self.result_tag_ = params.getParam("result_tag").getStringValue()

        self.reverse_line_traverse_ = \
            params.getParam("reverse_line_traverse").getBooleanValue()

        self.fail_if_present_ = self.reverse_line_traverse_ = \
            params.getParam("fail_if_present").getBooleanValue()
    

    def __auto_convert(self, string_val):
        """
        Converts a string to the relevant literal it represents unless
        it is a string or some other object, which it then just returns.
        """
        try:
            return ast.literal_eval(string_val)
        except (ValueError, SyntaxError):
            return string_val


    def executeCheck(self, config: dict, annotations: list[str]) -> bool:
        out_file_name = config["out_file_name"]
        try:
            out_file = open(out_file_name, "r")
        except Exception as ex:
            message = f'Error opening file "{out_file_name}".'
            annotations.append("Python FileIOError")
            self.failed_ = True
            self.fail_reason_ = message
            return False

        lines = out_file.readlines()
        relevant_line = None

        if not self.reverse_line_traverse_:
            line_num = 0
            for line in lines:
                line_num += 1
                if line.find(self.line_key_) >= 0:
                    relevant_line = line
                    break
        else:
            for line in reversed(lines):
                if line.find(self.line_key_) >= 0:
                    relevant_line = line
                    break

        if relevant_line != None:
            word_id = self.word_number_
            words = relevant_line.split()
            if word_id >= len(words):
                message = f'Found line containing "{self.line_key_}", ' + \
                          f'i.e. line {relevant_line}. ' + \
                          f'but the number of words is less than the ' + \
                          f'requested word number ({word_id}) to process.'
                self.failed_ = True
                self.fail_reason_ = message
                return False
            
            test = config["test"]
            test.tagged_results_[self.result_tag_] = \
                 self.__auto_convert(words[word_id])

        if not self.fail_if_present_:
            if relevant_line == None:
                message = f'Could not find line containing "{self.line_key_}".'
                self.failed_ = True
                self.fail_reason_ = message
                return False
            else:
                return True
        else:
            if relevant_line == None:
                return True
            else:
                message = f'Found line containing "{self.line_key_}".'
                self.failed_ = True
                self.fail_reason_ = message
                return False



PyFactory.register(ResultTagCheck, "ResultTagCheck")
