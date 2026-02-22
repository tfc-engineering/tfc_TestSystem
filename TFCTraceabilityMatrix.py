import yaml
from typing import Tuple, List

#####################################################################
def coloredText(color:str, text:str) -> str:
    "Simple macro to provide html coloring within markdown text."
    return f'<span style="color:{color}">{text}</span>'

#####################################################################
def parseMarkdownMetadata(filepath, lines) -> dict:
    """
    Finds the lines block by opening "---" and closing "---" and
    converts them, as yaml, to a dictionary
    """
    # Markdown metadata is a somewhat unofficial means
    # to add file properties, basically:
    # - First line of the md file starting with "---" up till the next
    #   line containing "---". Everything in-between is parsed as yaml.
    md_metadata = {}
    yaml_block = ""
    if len(lines) > 0 and lines[0].strip()[0:3] == "---":
        # Find the closing "---"
        k = 1
        while k < len(lines):
            if lines[k].strip()[0:3] == "---":
                yaml_block = ''.join(lines[1:k])
                break
            k += 1

    # Process the metadata
    if yaml_block != "":
        print(f'*** MetaData for "{filepath}":')
        print(yaml_block)
        print("***")

        md_metadata = yaml.safe_load(yaml_block)

    return md_metadata


#####################################################################
def lineHasTag(line : str, tag : str) -> bool:
    """
    Determines if the line has the syntax "<!--tag ..."
    """
    strip_line = line.strip()
    commented_tag =f'<!--{tag}'
    tag_length = len("<!--") + len(tag)
    if strip_line[0:tag_length] == commented_tag:
        return True

    return False


#####################################################################
def tagValue(line : str, tag : str) -> str:
    """
    Determines the value from a line with syntax syntax "<!--tag value-->".
    """
    strip_line = line.strip()
    commented_tag =f'<!--{tag}'
    tag_length = len("<!--") + len(tag)
    if not strip_line[0:tag_length] == commented_tag:
        return ""

    value = strip_line[tag_length:].replace("-->","").strip()

    return value


#####################################################################
def processTopicLine(lines, line_id) -> str:
    """
    A topic tag-line has the format "<!--topic topic_name-->".
    Following the tag-line is the topic line with format
    "## 9. Text for the topic"

    This function strips the level 2 section marks (##) and the numbering part
    ("9.") and return the "Text for the topic" part.
    """
    # Extract the first sentence from the paragraph following the
    # tag by reading all the text up the next blank line.
    text = ""
    k = line_id + 1
    while k < len(lines):
        line = lines[k].strip()
        if len(line.split()) == 0 or line[0:4] == "<!--":
            break

        prefix = "" if text == "" else " "
        text += f'{prefix}{line}'
        k += 1

    strip_text = text.strip()
    if strip_text[0:2] == "##":
        strip_text = strip_text[2:].strip()
    period_loc = strip_text.find(".")
    if strip_text[0:period_loc].isdigit():
        strip_text = strip_text[period_loc+1:].strip()

    return strip_text


#####################################################################
def processRequirementLine(lines, line_id) -> tuple[str,str]:
    """
    A requirement has the format "Req XX Stuff in here.".

    This function extracts the XX and "Stuff in here." part and returns them
    as two separate values. The XX part is stripped of commas and periods.
    """
    # Extract the first sentence from the paragraph following the
    # tag by reading all the text up the next blank line.
    text = ""
    k = line_id
    while k < len(lines):
        line = lines[k].strip()

        if len(line.split()) == 0: break

        prefix = "" if text == "" else " "
        text += f'{prefix}{line}'
        k += 1

    strip_text = text.strip()
    words = strip_text.split()

    if not words[0] == "Req" or len(words) < 3:
        print(f'ERROR: Failed to parse requirement "{text}"')
        return "", ""

    tag = words[1].replace(".","").replace(",","")
    tag_end = strip_text.find(words[1]) + len(words[1])
    text = strip_text[tag_end:].strip()

    return tag, text


#####################################################################
class TopicBlock:
    """
    Simple data structure to hold a topic block and its associated requirements
    """
    def __init__(self, tag, text):
        self.tag = tag
        self.text = text
        self.requirement_strings = {}


# This system is responsible for parsing requirement documents and mapping
# them to the test system results so that a requirements traceability matrix
# can be established.
class TFCTraceabilityMatrix:
    """
    Parent of TFCTestSystem only. This class adds just the requirements
    system.
    """

    #################################################################
    @staticmethod
    def parseRequirementDocument(filepath: str) -> dict:
        """Parses a requirements document that has a particular syntax and
           stores it into a dictionary structure."""

        requirements_block = dict(filepath=filepath,
                                  category="General",
                                  link="",
                                  topics={})

        try:
            in_file = open(filepath, "r")
        except Exception as e:
            print(f'\033[31mERROR: {e}\033[0m')
            return

        lines = in_file.readlines()

        # ======================================= Parse the metadata
        md_metadata = parseMarkdownMetadata(filepath, lines)

        # ======================================= Process category
        if "title" in md_metadata:
            requirements_block["category"] = md_metadata["title"]
        if "link" in md_metadata:
            requirements_block["link"] = md_metadata["link"]

        # ======================================= Process file
        topic_block = None
        topics_block = requirements_block["topics"] # Short-hand

        for line_id,line in enumerate(lines):
            stripped_line = line.strip()

            if lineHasTag(line, "topic"):
                topic_block = TopicBlock(tag=tagValue(line, "topic"),
                                         text=processTopicLine(lines, line_id))
                topics_block[topic_block.tag] = topic_block

            if stripped_line[0:4] == "Req ":
                tag_value, text = processRequirementLine(lines, line_id)
                topic_block.requirement_strings[tag_value] = text


        in_file.close()

        return requirements_block


    #################################################################
    def writeRequirementsTraceabilityMatrix(self) -> None:
        """Cleverly writes the requirements traceability matrix."""
        rtmfile = open(self.requirements_matrix_outputfile_, "w")
        req_blocks = self.requirement_blocks_

        #======================================== Determine test subscriptions
        requirements_to_test_mapping = {}
        req2map = requirements_to_test_mapping # shorthand name

        # Loop over tests, for each requirement they list,
        # build an inverse map
        test_objects = self.tests_
        for test_object in test_objects:
            for requirement_str in test_object.requirements_:
                if not requirement_str in req2map:
                    req2map[requirement_str] = []

                req2map[requirement_str].append(test_object)

        #======================================== Determine test integrity
        # First build a list of registered requirements
        reqistered_requirements = []
        for req_block in req_blocks:
            for topic_tag,topic_block in req_block["topics"].items():
                for req_tag, req_string in topic_block.requirement_strings.items():
                    topic_req_tag = f'{topic_tag}.{req_tag}'
                    reqistered_requirements.append(topic_req_tag)

        # Now check each test
        invalid_tests = {}
        for test_object in test_objects:
            test_invalid_reqs = []
            for requirement_str in test_object.requirements_:
                if requirement_str not in reqistered_requirements:
                    test_invalid_reqs.append(requirement_str)
            if len(test_invalid_reqs) > 0:
                invalid_tests[test_object.name_] = test_invalid_reqs

        integrity = ""
        integrity += "# Test Integrity\n"
        integrity += "\n"

        if len(invalid_tests) == 0:
            integrity += "There are no tests that reference unregistered " + \
                         "requirements."
        else:
            integrity += f'Number of tests that reference ' + \
                         f'unregistered requirements = {len(invalid_tests)}:\n\n'
            for test_name, invalid_reqs in invalid_tests.items():
                integrity += f'- {test_name}: '
                for id, req in enumerate(invalid_reqs):
                    integrity += coloredText("red", req)
                    if id < len(invalid_reqs)-1: integrity += ", "

                integrity += "\n"

        rtmfile.write(integrity)
        rtmfile.write("\n\n")


        #======================================== Internal routine to write
        #                                         test block
        def writeTestBlockCoverage(test_object):
            coverage = ""
            annotation = test_object.test_result_annotation_
            pass_fail = "Pass" if test_object.passed_ else "Fail"
            pass_fail_color = "green" if test_object.passed_ else "red"

            pass_fail_str = coloredText(pass_fail_color, pass_fail)

            annotation_str = "" if annotation == "" else \
                             f' ({coloredText("cyan", annotation)})'

            coverage += f'- {test_object.name_}'
            coverage += annotation_str
            coverage += f' {pass_fail_str}<br>\n'

            return coverage

        #======================================== Write the matrix
        req_block_id = 0
        for req_block in req_blocks:
            req_block_id += 1
            filepath = req_block["filepath"]
            category = req_block["category"]
            link = req_block["link"]

            outstr = ""
            outstr += f'# {req_block_id} {category}\n'
            if link != "":
                outstr += f'[Requirement Specification]({link})\n'

            sub_req_id = 0
            for topic_tag,topic_block in req_block["topics"].items():
                sub_req_id += 1
                basic_title = topic_block.text

                outstr += f'## {req_block_id}.{sub_req_id} {basic_title} [{topic_tag}]\n'
                outstr += "\n"
                for req_tag, req_string in topic_block.requirement_strings.items():
                    topic_req_tag = f'{topic_tag}.{req_tag}'

                    # Determine coverage
                    coverage = ""
                    status = ""
                    if not topic_req_tag in requirements_to_test_mapping:
                        status = f'{coloredText("orange", "No tests")}\n'
                        coverage += f'{coloredText("orange", "NO TEST COVERAGE")}\n'
                        coverage += "<br>"
                        coverage += "\n"
                    else:
                        status = f'{coloredText("red", "Failures")}\n'

                        test_objects = requirements_to_test_mapping[topic_req_tag]
                        num_tests_failed = 0
                        for test_object in test_objects:
                            coverage += writeTestBlockCoverage(test_object)
                            # coverage += "\n" # needed for FORD
                            if not test_object.passed_:
                                num_tests_failed += 1

                        if num_tests_failed == 0:
                            status = f'{coloredText("green", "OK")}\n'

                    req_tag_str = f'{req_tag}.' if req_tag.isdigit() else req_tag

                    # Write it out
                    outstr += "<details>\n"
                    outstr += "  <summary>"
                    outstr += f'Req {req_tag_str} {req_string} {status}'
                    outstr += "  </summary>\n"
                    outstr += "\n"

                    outstr += '\n<strong>Test coverage:</strong><br>\n'
                    outstr += "\n"
                    outstr += coverage
                    outstr += "<br>"
                    outstr += "\n"


                    outstr += "</details>\n"
                outstr += '\n\n\n\n'

            rtmfile.write(outstr)
        rtmfile.close()
