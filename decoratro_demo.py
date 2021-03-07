def decorator_main_plure_status(input_function):
    plure_list = ['1', 2, 3]
    status_list = ['1', 2, 3]
    for plure in plure_list:
        for status in status_list:
            def wrapper_function(*args, **kwargs):
                return input_function(*args, **kwargs)
    return wrapper_function


@decorator_main_plure_status
def my_func(age, name):
    print(age, name)


if __name__ == '__main__':
    my_func('hi', 'my')