from pathlib import Path

import yaml

class TFCTestResultsDatabase:
    def _include_in_results_database(self, test_object) -> bool:
        return bool(getattr(test_object, "ran_", False) or getattr(test_object, "skip_", ""))

    def _extract_vnv_metadata(self, test_name: str) -> dict[str, str]:
        parts = Path(test_name).parts
        marker = ("test", "vnv", "cases")

        for i in range(len(parts) - len(marker) + 1):
            if parts[i:i + len(marker)] != marker:
                continue
            if i + 4 >= len(parts):
                break

            return {
                "vnv_type": parts[i + 3],
                "case_type": parts[i + 4],
                "case_name": parts[i + 5] if i + 5 < len(parts) else "",
                "input_file": parts[i + 6] if i + 6 < len(parts) else "",
            }

        return {
            "vnv_type": "",
            "case_type": "",
            "case_name": Path(test_name).stem,
            "input_file": Path(test_name).name,
        }

    def _testResultData(self, test_object) -> dict:
        test_data = {}
        test_data["name"] = test_object.name_
        test_data.update(self._extract_vnv_metadata(test_object.name_))
        test_data["requirements"] = test_object.requirements_
        test_data["passed"] = test_object.passed_
        test_data["annotations"] = test_object.test_result_annotation_
        test_data["test_doc_page"] = test_object.test_doc_page_
        test_data["tagged_results"] = test_object.tagged_results_
        return test_data


    def _mergeResultsDatabase(self, database: list[dict], merge_file: str) -> list[dict]:
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
        Writes the results database to a designated file as a YAML
        formatted file.
        """
        db_filename = self.test_results_database_outputfile_

        database = []

        # Now we loop over the tests
        test_objects = self.tests_
        for test_object in test_objects:
            if not self._include_in_results_database(test_object):
                continue
            database.append(self._testResultData(test_object))

        merge_file = getattr(self, "merge_results_file_", "")
        if merge_file:
            database = self._mergeResultsDatabase(database, merge_file)

        with open(db_filename, "w", encoding="utf-8") as db_file:
            yaml.dump(database, db_file, sort_keys=False)
