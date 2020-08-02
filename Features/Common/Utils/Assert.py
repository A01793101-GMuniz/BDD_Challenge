class TestAssert:

    def __init__(self):
        self.true_assert_count = 0

    def test_assert_entered_row_data(self, dict1, dict2, msg=None):
        if len(dict1) == len(dict2):
            for key in dict1.keys():
                assert dict1[key] == dict2[key], msg

    def test_assert_row_data_has_changed(self, new_data, old_data, msg=None):
        if len(new_data) == len(old_data):
            for key in new_data.keys():
                # Id is not editable hence It should only enter to increase counter
                assert new_data[key] != old_data[key] or key == "id"

