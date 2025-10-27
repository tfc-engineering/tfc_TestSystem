
class TFCTraceabilityMatrix:
    @staticmethod
    def parseRequirementDocument(filepath: str) -> dict:
        """Parses a requirements document that has a particular syntax and
           stores it into a dictionary structure."""
        requirements_block = dict(filepath=filepath,
                                  category="General",
                                  requirements=[])

        in_file = open(filepath, "r")

        lines = in_file.readlines()

        THIRD = 2

        within_a_req = False
        current_requirement = {}
        for line in lines:
            words = line.split()
            line_has_open_tag = (line.find("## Requirement") == 0)
            line_has_close_tag = (line.find("<!--endreq-->") == 0)

            # ============================= Process first line
            if line == lines[0] and line.find("# ") == 0:
                requirements_block["category"] = line[2:]

            # ============================= Process requirement begin
            if line_has_open_tag and len(words) >= 3:
                # Determine the id_tag, basic title
                id_tag = words[THIRD].replace(":", "")
                basic_title = ""
                for w in range(3, len(words)):
                    if words[w] != "-" and words[w] != ":":
                        basic_title += words[w] + " "

                # Determine the section link
                section_link = filepath + "#"
                section_link += line[3:].lower().strip().replace(" ", "-")

                # Initialize current requirement
                current_requirement["id_tag"] = id_tag
                current_requirement["basic_title"] = basic_title
                current_requirement["text"] = ""
                current_requirement["section_link"] = section_link

                within_a_req = True

                continue # We should be done with this line

            # ============================= Process requirement end
            if line_has_close_tag:
                requirements_block["requirements"].append(current_requirement)
                current_requirement = {}
                within_a_req = False

            # ============================= Process items between a requirement block
            if within_a_req:
                if len(words) == 0 and current_requirement["text"] == "":
                    pass
                else:
                    current_requirement["text"] += line

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

        # Now we loop over the tests
        test_objects = self.tests_
        for test_object in test_objects:
            requirements_strings = test_object.requirements_
            for requirement_str in requirements_strings:
                if not requirement_str in req2map:
                    requirements_to_test_mapping[requirement_str] = []

                requirements_to_test_mapping[requirement_str].append(test_object)

        #======================================== Write the matrix
        req_block_id = 0
        for req_block in req_blocks:
            req_block_id += 1
            filepath = req_block["filepath"]
            category = req_block["category"]

            outstr = ""
            outstr += f'# {req_block_id} {category}\n'
            outstr += f'[Requirement Specification]({filepath})\n'

            requirements = req_block["requirements"]
            sub_req_id = 0
            for requirement in requirements:
                sub_req_id += 1
                id_tag = requirement["id_tag"]
                basic_title = requirement["basic_title"]
                section_link = requirement["section_link"]
                text = requirement["text"]

                outstr += f'## {req_block_id}.{sub_req_id} Requirement "{id_tag}" - {basic_title}\n'
                outstr += text

                # Write out test coverage
                outstr += '\n**Test coverage:**\n'
                if not id_tag in requirements_to_test_mapping:
                    outstr += f'<span style="color:orange">**NO TEST COVERAGE**</span>\n'
                    continue

                test_objects = requirements_to_test_mapping[id_tag]
                for test_object in test_objects:
                    annotation = test_object.test_result_annotation_
                    pass_fail = "Pass" if test_object.passed_ else "Fail"
                    pass_fail_color = "green" if test_object.passed_ else "red"

                    pass_fail_str = f'<span style="color:{pass_fail_color}">**{pass_fail}**</span>'
                    annotation_str = f'<span style="color:cyan">{annotation}</span>'

                    outstr += f'  - {test_object.name_} {annotation_str} {pass_fail_str}\n'

            outstr += '\n\n\n\n'

            rtmfile.write(outstr)
        rtmfile.close()
