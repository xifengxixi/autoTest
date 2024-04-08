import inspect, os

# 定义一个类装饰器
def get_doc_info(cls):
    # 获取类中每个方法的方法描述
    methods = inspect.getmembers(cls, predicate=inspect.isfunction)
    method_descriptions = {}

    for name, method in methods:
        if name.startswith("__") and name.endswith("__"):
            continue
        if isinstance(inspect.getattr_static(cls, name), staticmethod):
            continue
        method_descriptions[name] = inspect.getdoc(method)

    # 修改原始类的方法行为
    for name in method_descriptions:
        method = getattr(cls, name)
        setattr(cls, name, decorate_method(method, method_descriptions[name]))
    return cls

# 辅助函数：装饰单个方法
def decorate_method(method, description):
    def wrapper(*args, **kwargs):
        if description:
            os.environ.update({'api_doc': description})
        return method(*args, **kwargs)

    return wrapper
