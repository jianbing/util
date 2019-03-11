class Adict(dict):

    def __getattr__(self, name):
        try:
            return self[name]
        except KeyError:
            raise self.__attr_error(name)

    def __setattr__(self, name, value):
        self[name] = value

    def __delattr__(self, name):
        try:
            del self[name]
        except KeyError:
            raise self.__attr_error(name)

    def __attr_error(self, name):
        return AttributeError(
            "type object '{subclass_name}' has no attribute '{attr_name}'".format(subclass_name=type(self).__name__,
                                                                                  attr_name=name))

    def copy(self):
        return Adict(self)

    @staticmethod
    def load_dict(target_dict):
        import copy
        return Adict._do_load_dict(copy.deepcopy(target_dict))

    @staticmethod
    def _do_load_dict(raw_dict):
        for key, value in raw_dict.items():
            if isinstance(value, dict):
                raw_dict[key] = Adict(value)
                Adict._do_load_dict(raw_dict[key])
            if isinstance(value, list):
                for index, i in enumerate(value):
                    if isinstance(i, dict):
                        value[index] = Adict(i)
                        Adict._do_load_dict(value[index])
        return Adict(raw_dict)


