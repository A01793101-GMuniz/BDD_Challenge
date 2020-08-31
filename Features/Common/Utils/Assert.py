
class TestAssert:

    def test_assert_equal_entered_row_data(self, dict1, dict2, msg=None):
        if len(dict1) == len(dict2):
            for key in dict1.keys():
                assert dict1[key] == dict2[key], msg

    def test_assert_not_equal_row_data_has_changed(self, new_data, old_data, msg=None):
        if len(new_data) == len(old_data):
            for key in new_data.keys():
                # Id is not editable hence It should only enter to increase counter
                assert new_data[key] != old_data[key] or key == "id"

    def test_assert_type_string(self, data, msg):
        assert isinstance(data, str), msg

    def test_assert_type_int(self, data, msg):
        assert isinstance(data, int), msg

    def test_assert_type_list_elements(self, data, msg):
        for dt in data:
            if isinstance(dt, int):
                self.test_assert_type_int(dt, msg + f"{type(dt)}")
            elif isinstance(dt, str):
                self.test_assert_type_string(dt, msg + f"{type(dt)}")
            else:
                assert False, msg



