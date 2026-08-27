import yaml


class TFCTestResultsDatabase:
    def _include_in_results_database(self, test_object) -> bool:
        return bool(
            getattr(test_object, "ran_", False))

    def _testResultMetadata(self, test_object) -> dict:
        """Return application-specific metadata for a test result."""
        return {}

    def _testResultData(self, test_object) -> dict:
        test_data = {
            "name": test_object.name_,
        }

        test_data.update(self._testResultMetadata(test_object))

        test_data.update({
            "requirements": test_object.requirements_,
            "passed": test_object.passed_,
            "annotations": test_object.test_result_annotation_,
            "test_doc_page": test_object.test_doc_page_,
            "tagged_results": test_object.tagged_results_,
        })

        return test_data

    def _mergeResultsDatabase(self,
                              database: list[dict],
                              merge_file: str) -> list[dict]:

        with open(merge_file, "r", encoding="utf-8") as db_file:
            existing = yaml.safe_load(db_file) or []

        merged = []
        updates = {entry["name"]: entry for entry in database}
        seen = set()

        for entry in existing:
            if not isinstance(entry, dict) or "name" not in entry:
                continue

            name = entry["name"]

            if name in updates:
                merged.append(updates[name])
            else:
                merged.append(entry)

            seen.add(name)

        for entry in database:
            if entry["name"] not in seen:
                merged.append(entry)

        return merged

    def writeResultsDatabase(self):
        """
        Write the results database to a YAML-formatted file.
        """
        database = []

        for test_object in self.tests_:
            if not self._include_in_results_database(test_object):
                continue

            database.append(self._testResultData(test_object))

        merge_file = getattr(self, "merge_results_file_", "")
        if merge_file:
            database = self._mergeResultsDatabase(database, merge_file)

        with open(self.test_results_database_outputfile_, "w") as db_file:
            yaml.dump(database, db_file, sort_keys=False)
