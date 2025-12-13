from os.path import dirname, abspath


def get_project_dir():
    current_path = dirname(abspath(__file__))
    # 获取当前脚本所在的项目根目录
    root_path = dirname(current_path)
    # print("项目根目录路径：", root_path)
    return root_path
