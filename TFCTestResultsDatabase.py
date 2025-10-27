import yaml

class TFCTestResultsDatabase:
    def writeResultsDatabase(self):
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

            database.append(test_data)

        yaml.dump(database, db_file, sort_keys=False)

        db_file.close()
