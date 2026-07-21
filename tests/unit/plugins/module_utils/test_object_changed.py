import unittest

from plugins.module_utils.common import object_changed


class TestObjectChanged(unittest.TestCase):
    def test_scalar_no_change(self):
        self.assertEqual(object_changed({"name": "a"}, {"name": "a"}), [])

    def test_scalar_changed(self):
        self.assertTrue(object_changed({"name": "a"}, {"name": "b"}))

    def test_list_same_length_no_change(self):
        self.assertEqual(
            object_changed({"tags": ["a", "b"]}, {"tags": ["a", "b"]}), []
        )

    def test_list_same_length_changed(self):
        self.assertTrue(
            object_changed({"tags": ["a", "b"]}, {"tags": ["a", "c"]})
        )

    def test_list_grow_does_not_raise(self):
        # desired list longer than existing list must not raise IndexError (issue #52)
        result = object_changed({"tags": ["a"]}, {"tags": ["a", "b"]})
        self.assertTrue(result)

    def test_list_shrink_detected(self):
        # desired list shorter than existing list must be detected as changed (issue #52)
        result = object_changed({"tags": ["a", "b"]}, {"tags": ["a"]})
        self.assertTrue(result)

    def test_list_empty_superset_with_nonempty_subset(self):
        self.assertTrue(object_changed({"tags": []}, {"tags": ["a"]}))

    def test_list_empty_superset_with_empty_subset(self):
        self.assertEqual(object_changed({"tags": []}, {"tags": []}), [])

    def test_list_none_superset_with_nonempty_subset(self):
        self.assertTrue(object_changed({"tags": None}, {"tags": ["a"]}))

    def test_nested_dict_in_list_changed(self):
        result = object_changed(
            {"items": [{"id": 1, "name": "a"}]},
            {"items": [{"id": 1, "name": "b"}]},
        )
        self.assertTrue(result)

    def test_nested_dict_in_list_no_change(self):
        result = object_changed(
            {"items": [{"id": 1, "name": "a"}]},
            {"items": [{"id": 1, "name": "a"}]},
        )
        self.assertEqual(result, [])

    def test_dict_no_change(self):
        self.assertEqual(
            object_changed({"opts": {"a": 1, "b": 2}}, {"opts": {"a": 1}}), []
        )

    def test_dict_changed(self):
        self.assertTrue(
            object_changed({"opts": {"a": 1}}, {"opts": {"a": 2}})
        )

    def test_ignore_value(self):
        self.assertEqual(
            object_changed({"resendInterval": 0}, {"resendInterval": 5}, ignore={"resendInterval": 0}),
            [],
        )


if __name__ == "__main__":
    unittest.main()
