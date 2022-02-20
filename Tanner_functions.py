import inspect

def retrieve_name(var):
    callers_local_vars = inspect.currentframe().f_back.f_locals.items()
    return [var_name for var_name, var_val in callers_local_vars if var_val is var]


def mod_retrieve_name(var):
    callers_local_vars = inspect.currentframe().f_back.f_back.f_locals.items()
    return [var_name for var_name, var_val in callers_local_vars if var_val is var]


def print_label_and_value(var):
    var_name = mod_retrieve_name(var)
    var_name = var_name[0]
    print(f"{var_name}:",var)

def print_len_label_val(var):
    var_name = mod_retrieve_name(var)
    var_name = var_name[0]
    print(f"{var_name}:")
    print("Length:", len(var))
    print(f"{var_name}:", var)
    print("\n")
