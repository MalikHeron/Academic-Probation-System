from swiplserver import PrologMQI, PrologThread, create_posix_path

# pip install git+https://github.com/yuce/pyswip@master
# python.exe -m pip install --upgrade pip

with PrologMQI() as mqi:
    with mqi.create_thread() as prolog_thread:
        path = create_posix_path(
            "../prolog/knowledge_base.pl")  # Replace with your file path
        prolog_thread.query(f'consult("{path}").')
        prolog_thread.query_async("default_gpa(GPA)", find_all=False)
        while True:
            result = prolog_thread.query_async_result()
            if result is None:
                break
            else:
                print(result)
