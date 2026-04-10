import pathlib

from tfc_PyFactory.InputParameters import InputParameters
file_path = str(pathlib.Path(__file__).parent.resolve()) + "/"

import sys
sys.path.append(file_path + "../../")

import tfc_PyFactory
from tfc_PyFactory import *

from .CheckBase import *

import ast
import re

class ResultTagRegExCheck(CheckBase):
    '''Checks for presence or abscence of a string in the output of a test. if
    present a designated word can be stored, along with a tag, as a result.'''
    @staticmethod
    def getInputParameters() -> InputParameters:
        params = CheckBase.getInputParameters()

        params.addRequiredParam("reg_ex", ParameterType.STRING,
                                "The regular expression to be executed on each line.")
        params.addOptionalParam("group", int(0),
                                "The regular expression capture group number.")
        params.addRequiredParam("result_tag", ParameterType.STRING,
                                "String name of the tag to which the result will be assigned.")
        params.addOptionalParam("reverse_line_traverse", False,
                                "If true will reverse the traversal of file lines.")

        params.addOptionalParam("fail_if_present", False,
                                "Inverts the check. Fails if the line_key is indeed found.")

        return params


    def __init__(self, params: InputParameters) -> None:
        super().__init__(params)

        self.reg_ex_ = params.getParam("reg_ex").getStringValue()

        self.group_number_ = params.getParam("group").getIntegerValue()

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
        result = None

        if not self.reverse_line_traverse_:
            line_num = 0
            for line in lines:
                line_num += 1
                match = re.search(self.reg_ex_, line)
                if match:
                    result = match.group(self.group_number_)
                    break
        else:
            for line in reversed(lines):
                match = re.search(self.reg_ex_, line)
                if match:
                    result = match.group(self.group_number_)
                    break

        if result != None:
            test = config["test"]
            test.tagged_results_[self.result_tag_] = \
                 self.__auto_convert(result)

        if not self.fail_if_present_:
            if result == None:
                message = f'Could not find line containing "{self.reg_ex_}".'
                self.failed_ = True
                self.fail_reason_ = message
                return False
            else:
                return True
        else:
            if result == None:
                return True
            else:
                message = f'Found line containing "{self.reg_ex_}".'
                self.failed_ = True
                self.fail_reason_ = message
                return False



PyFactory.register(ResultTagRegExCheck, "ResultTagRegExCheck")
