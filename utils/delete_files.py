import os
import shutil
def clean_directory(target_dir):
    # 验证目标目录是否存在
    if not os.path.exists(target_dir):
        raise FileNotFoundError(f"目标目录不存在: {target_dir}")

    deleted_files = 0
    deleted_dirs = 0

    for entry in os.listdir(target_dir):
        full_path = os.path.join(target_dir, entry)

        try:
            if os.path.isfile(full_path) or os.path.islink(full_path):
                os.remove(full_path)  # 删除文件和符号链接
                deleted_files += 1
            elif os.path.isdir(full_path):
                shutil.rmtree(full_path)  # 递归删除子目录
                deleted_dirs += 1
        except Exception as e:
            print(e)
