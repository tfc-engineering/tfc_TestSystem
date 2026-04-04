import yaml

class TFCTestResultsDatabase:
    def writeResultsDatabase(self):
        """
        Writes the results database to a designated file as a YAML
        formatted file.
        """
        db_filename = self.test_results_database_outputfile_

        db_file = open(db_filename, "w")

        database = []

        # Now we loop over the tests
        test_objects = self.tests_
        for test_object in test_objects:
            test_data = {}
            test_data["name"] = test_object.name_
            test_data["requirements"] = test_object.requirements_
            test_data["passed"] = test_object.passed_
            test_data["annotations"] = test_object.test_result_annotation_
            test_data["test_doc_page"] = test_object.test_doc_page_
            test_data["tagged_results"] = test_object.tagged_results_
            database.append(test_data)

        yaml.dump(database, db_file, sort_keys=False)

        db_file.close()
