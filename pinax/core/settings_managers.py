'''
Settings managers provide a backwards-compatible wrapper around Django's
builtin settings handling.  Once setup, settings managers offer a more
flexible, class-based, API for defining settings.  Additionally they provide
hooks to allow for local settings to build upon all previously defined
settings and for pinax to build settings on those local settings.
'''
from copy import copy

class BaseSettingsManager(object):
    '''
    Provides the basic settings manager functionality.
    '''
    
    def __len__(self):
        return len(self.keys())
    
    def __getitem__(self, key):
        not_found = False
        item = None
        
        try:
            item = getattr(self, key)
        except AttributeError:
            not_found = True
            
        if key not in self.keys():
            not_found = True
            
        if not_found:
            raise KeyError("'%s' settings manager has no setting '%s'" % (self.__class__.__name__, key))
        
        return item
    
    def __setitem__(self, key, value):
        setattr(self, key, value)
        
    def __delitem__(self, key):
        # Decide what type of property key is to decide how to delete:
        # Class properties need to be deleted from the class
        # Instance properties need to be deleted from the instance
        if hasattr(self.__class__, key):
            delattr(self.__class__, key)
        else:
            try:
                delattr(self, key)
            except AttributeError:
                raise KeyError("'%s' settings manager has no setting '%s'" % (self.__class__.__name__, key))
            
    def __iter__(self):
        return self.iterkeys()
        
    def __contains__(self, key):
        return self.has_key(key)
        
    def iterkeys(self):
        settings = self.keys()
        for setting in settings:
            yield setting
            
    def itervalues(self):
        values = self.values()
        for value in values:
            yield value
            
    def iteritems(self):
        settings = self.keys()
        for setting in settings:
            yield (setting, self.__getitem__(setting))
            
    def items(self):
        items = []
        for item in self.iteritems():
            items.append(item)
            
        return items
    
    def keys(self):
        settings = []
        for setting in dir(self):
            if not (setting.startswith('_') or setting in dir(BaseSettingsManager)):
                settings.append(setting)
        
        return settings
        
    def values(self):
        values = []
        for key in self.keys():
            values.append(self.__getitem__(key))
            
        return values
        
    def has_key(self, key):
        return key in self.keys()
        
    def get(self, key, default=None):
        value = default
        try:
            value = self.__getitem__(key)
        except KeyError:
            value = default
            
        return value
        
    def clear(self):
        for key in self.keys():
            self.__delitem__(key)
            
    def setDefault(self, key, default=None):
        try:
            value = self.__getitem__(key)
        except KeyError:
            value = default
            self.__setitem__(key, value)
            
        return value
        
    def pop(self, key, default=None):
        value = self.get(key, default)
        try:
            self.__delitem__(key)
        except KeyError:
            pass
        
        return value
        
    def popitem(self, key, default=None):
        value = self.pop(key, default)
        
        return (key, value,)
        
    def copy(self):
        return copy(self)
        
    def update(self, updates):
        for key, value in updates.iteritems():
            self.__setitem__(key, value)