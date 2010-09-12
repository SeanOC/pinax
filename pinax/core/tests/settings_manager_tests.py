import unittest

from pinax.core.settings_managers import BaseSettingsManager

class SimpleSampleManager(BaseSettingsManager):
    test_value_1 = 'one'
    test_value_2 = 'two'
    

class TestBaseSettingsManager(unittest.TestCase):
    
    def get_delete_safe_simple_manager_class(self):
        class SimpleDeleteSampleManager(BaseSettingsManager):
            test_value_1 = 'one'
            test_value_2 = 'two'
            
        return SimpleDeleteSampleManager

    def len_test(self, expected, manager):
        result = len(manager)
        self.assertEquals(expected, result)
        
    def test_simple_len(self):
        manager = SimpleSampleManager()
        self.len_test(expected=2, manager=manager)
        
        
    def get_item_test(self, key, manager):
        expected = getattr(manager, key)
        result = manager[key]
        self.assertEquals(expected, result)
        
    def get_missing_item_test(self, key, manager):
        self.assertRaises(KeyError, manager.__getitem__, key)
    
    def test_simple_get_item(self):
        manager = SimpleSampleManager()

        self.get_item_test(key='test_value_1', manager=manager)
        self.get_item_test(key='test_value_2', manager=manager)
        
    def test_simple_get_missing_item(self):
        manager = SimpleSampleManager()
        
        self.get_missing_item_test(key="test_value_3", manager=manager)
    
    def get_keys_test(self, expected, manager):    
        # Put results into sets since we don't care about order
        expected = set(expected)
        result = set(manager.keys())
        self.assertEquals(expected, result)
        
    def test_simple_get_keys(self):
        manager = SimpleSampleManager()
        expected = ['test_value_1', 'test_value_2']
        self.get_keys_test(expected=expected, manager=manager)
        
        
    def get_items_test(self, expected, manager):    
        # Put results into sets since we don't care about order
        expected = set(expected)
        result = set(manager.items())
        self.assertEquals(expected, result)
        
    def test_simple_get_items(self):
        manager = SimpleSampleManager()
        expected = [
            ('test_value_1', manager.test_value_1), 
            ('test_value_2', manager.test_value_2)
        ]
        self.get_items_test(expected=expected, manager=manager)
        
    def set_item_test(self, manager):
        expected = 'three'
        
        manager['test_value_3'] = expected
        
        self.assertEquals(expected, manager['test_value_3'])
        self.assertEquals(expected, manager.test_value_3)
        
    def test_simple_set_items(self):
        manager = SimpleSampleManager()
        self.set_item_test(manager)
        
    def del_item_test(self, to_delete, manager):
        exists = hasattr(manager, to_delete)
        self.assertTrue(exists, "Can't test deleting '%s' because it doesn't exist." % to_delete)
        
        del manager[to_delete]
        
        exists = hasattr(manager, to_delete)
        self.assertFalse(exists, "Failed to delete '%s'." % to_delete)
        
    def del_missing_item_test(self, to_delete, manager):
        self.assertRaises(KeyError, manager.__delitem__, to_delete)
        
    def test_simple_del_class_item(self):
        SimpleDeleteSampleManager = self.get_delete_safe_simple_manager_class()
        manager = SimpleDeleteSampleManager()
        self.del_item_test(to_delete='test_value_1', manager=manager)
        
    def test_simple_del_instance_item(self):
        manager = SimpleSampleManager()
        manager.test_value_3 = 'three'
        self.del_item_test(to_delete='test_value_3', manager=manager)
        
    def test_simple_del_missing_class_item(self):
        manager = SimpleSampleManager()
        self.del_missing_item_test(to_delete='test_value_3', manager=manager)
        
    def test_simple_del_missing_instance_item(self):
        manager = SimpleSampleManager()
        manager.test_value_3 = 'three'
        self.del_missing_item_test(to_delete='test_value_4', manager=manager)
        
    def iterator_test(self, expected, manager):
        # Put results into sets since we don't care about order
        expected = set(expected)
        result = set()
        
        for setting in manager:
            result.add(setting)
        
        self.assertEquals(expected, result)
        
    def test_simple_iterator(self):
        manager = SimpleSampleManager()
        expected = ['test_value_1', 'test_value_2']
        self.iterator_test(expected, manager)
        
    def values_test(self, expected, manager):
        # Puts results into sets sicne we don't care about order
        expected = set(expected)
        result = set(manager.values())
        
        self.assertEquals(expected, result)
        
    def test_simple_values(self):
        manager = SimpleSampleManager()
        expected = ['one', 'two']
        
        self.values_test(expected, manager)
        
    def has_key_test(self, target, expected, manager):
        result = manager.has_key(target)
        self.assertEquals(expected, result)
        
    def test_has_key_simple_class_property(self):
        manager = SimpleSampleManager()
        
        self.has_key_test(
            target='test_value_1', expected=True, manager=manager
        )
        self.has_key_test(
            target='test_value_3', expected=False, manager=manager
        )

    def test_has_key_simple_class_property(self):
        manager = SimpleSampleManager()
        manager.test_value_3 = 'three'
        
        self.has_key_test(
            target='test_value_3', expected=True, manager=manager
        )
        self.has_key_test(
            target='test_value_4', expected=False, manager=manager
        )
        
    def test_contains(self):
        manager = SimpleSampleManager()
        self.assertTrue('test_value_1' in manager)
        self.assertFalse('test_value_3' in manager)
        
    def get_test(self, key, default, expected, manager):
        result = manager.get(key, default)
        self.assertEquals(expected, result)
        
    def test_simple_get_hit(self):
        manager = SimpleSampleManager()
        self.get_test(
            key = 'test_value_1',
            default = None,
            expected = 'one',
            manager = manager,
        )
        
    def test_simple_get_miss(self):
        manager = SimpleSampleManager()
        self.get_test(
            key = 'test_value_3',
            default = 'default',
            expected = 'default',
            manager = manager,
        )
        
    def clear_test(self, manager):
        keys = manager.keys()
        
        manager.clear()
        
        for key in keys:
            self.assertFalse(hasattr(manager, key))
            self.assertFalse(key in manager)
            
    def test_simple_clear(self):
        SimpleDeleteSampleManager = self.get_delete_safe_simple_manager_class()
        
        manager = SimpleDeleteSampleManager()
        self.clear_test(manager)
        
    def setDefault_test(self, key, default, expected, manager):
        result = manager.setDefault(key, default)
        self.assertEquals(expected, result)
        if result == default:
            self.assertEquals(expected, manager[key])
            
    def test_simple_setDefault_hit(self):
        manager = SimpleSampleManager()
        self.setDefault_test(
            key = 'test_value_1',
            default = None,
            expected = 'one',
            manager = manager,
        )
        self.setDefault_test(
            key = 'new_key_1',
            default = 'default',
            expected = 'default',
            manager = manager,
        )
        
    def itervalues_test(self, expected, manager):
        expected = set(expected)
        result = set()
        
        for value in manager.itervalues():
            result.add(value)
            
        self.assertEquals(expected, result)
        
    def test_simple_itervalues(self):
        manager = SimpleSampleManager()
        expected = ['one', 'two']
        self.itervalues_test(expected, manager)
        
    def pop_test(self, key, default, expected, manager):
        result = manager.pop(key, default)
        self.assertEquals(expected, result)
        self.assertFalse(hasattr(manager, key))
        self.assertFalse(key in manager)
        
    def test_simple_pop_hit(self):
        SimpleDeleteSampleManager = self.get_delete_safe_simple_manager_class()
        
        manager = SimpleDeleteSampleManager()
        self.pop_test(
            key = 'test_value_1',
            default = None,
            expected = 'one',
            manager = manager,
        )
    
    def test_simple_pop_miss(self):
        manager = SimpleSampleManager()
        
        self.pop_test(
            key = 'test_value_3',
            default = 'default',
            expected = 'default',
            manager = manager,
        )
        
    def popitem_test(self, key, default, expected, manager):
        expected = (key, expected)
        result = manager.popitem(key, default)
        self.assertEquals(expected, result)
        self.assertFalse(hasattr(manager, key))
        self.assertFalse(key in manager)
        
    def test_simple_popitem_hit(self):
        SimpleDeleteSampleManager = self.get_delete_safe_simple_manager_class()
        
        manager = SimpleDeleteSampleManager()
        self.popitem_test(
            key = 'test_value_1',
            default = None,
            expected = 'one',
            manager = manager,
        )
    
    def test_simple_popitem_miss(self):
        manager = SimpleSampleManager()
        
        self.popitem_test(
            key = 'test_value_3',
            default = 'default',
            expected = 'default',
            manager = manager,
        )
        
    def copy_test(self, target, manager):
        self.assertFalse(hasattr(manager, target), "Target '%s' cannot exist on the manager before copy_test is called." % target)
        
        result = manager.copy()
        manager[target] = 'test'
        self.assertEquals(getattr(manager, target), 'test')
        self.assertFalse(hasattr(result, target))
        
    def test_simple_copy(self):
        manager = SimpleSampleManager()
        
        self.copy_test(target='test_value_3', manager=manager)
        
    def update_test(self, updates, expected, manager):
        manager.update(updates)
        
        # Check both ways to ignore order but catch missing entries
        for key, value in expected.iteritems():
            self.assertEquals(value, manager[key])
        
        for key, value in manager.iteritems():
            self.assertEquals(value, expected[key])
            
    def test_simple_update(self):
        manager = SimpleSampleManager()
        updates = {
            'test_value_1': 'new value',
            'test_value_3': 'three',
        }
        expected = {
            'test_value_1': 'new value',
            'test_value_2': 'two',
            'test_value_3': 'three',
        }
        
        self.update_test(updates, expected, manager)


if __name__ == '__main__':
    unittest.main()