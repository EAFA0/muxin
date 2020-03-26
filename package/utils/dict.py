def merge(obj1, obj2):

    def merge_rule(obj1, obj2):
        '''
        不同类型的 merge 规则不一样:
            list 会以 + 的形式合并
            dict 会被迭代
            其余类型的, obj2 覆盖 obj1
        '''
        if type(obj1) == type(obj2):
            if isinstance(obj1, list):
                return obj1 + obj2
            elif isinstance(obj1, dict):
                return merge(obj1, obj2)

        return obj2

    result = obj1.copy()
    result.update(obj2)
    result.update((key, merge_rule(obj1[key], obj2[key]))
                  for key in set(obj1).intersection(obj2))
    return result
