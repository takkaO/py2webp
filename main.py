import pathlib
import os
import sys
import subprocess

def main(target_list):
    err = False
    sorted(target_list)
    cwebp = str(pathlib.Path(sys.argv[0]).with_name("cwebp.exe"))

    for i, target in enumerate(target_list):
        print("## ({0}/{1}) Processing".format(i+1, len(target_list)))

        fpath = pathlib.Path(target)
        if (fpath.suffix).lower() == ".webp":
            print("## ({0}/{1}) Skip".format(i+1, len(target_list)))
            print("--------------------")
            continue
        
        lossless = ""
        if (fpath.suffix).lower() == ".png":
            lossless = "-lossless"
        
        output = str(fpath.with_suffix('.webp'))
        command = "{0} \"{1}\" {2} -o \"{3}\"".format(cwebp, target, lossless, output)
        try:
            subprocess.run(command, stdout=subprocess.PIPE, check=True).stdout.decode('cp932')
        except:
            import traceback
            traceback.print_exc()
            print("===============")
            print(command)
            print("===============")
            print("Error occurred!")
            #print("Press enter to continue.")
            #input()
            err = True
            continue
        os.remove(target)
        print("## ({0}/{1}) Complete!".format(i+1, len(target_list)))
        print("--------------------")
    return err

def list_files(path: str, depth: int = -1) -> list:
    """
    指定されたパスがファイルならそのファイルのみをリストで返し、
    ディレクトリなら指定の深さまで再帰的にファイルを取得する。

    :param path: 絶対パスのファイルまたはディレクトリ
    :param depth: 探索する階層の深さ（-1 の場合は無制限）
    :return: ファイルパスのリスト
    """
    if os.path.isfile(path):
        return [path]  # ファイルならそのままリストで返す
    
    file_list = []
    base_depth = path.rstrip(os.sep).count(os.sep)

    for root, _, files in os.walk(path):
        current_depth = root.count(os.sep) - base_depth
        if 0 <= depth < current_depth:
            continue  # 指定の深さを超えたらスキップ
        for file in files:
            file_list.append(os.path.join(root, file))
    
    return file_list

if __name__ == "__main__":
    target_path_list = []
    input_path = sys.argv[1:]
    try:    
        for path  in input_path:
            target_path_list += list_files(path)
        err = main(target_path_list)

        if err is True:
            print("Error occurred!")
            print("Please check the log above.")
            print("Press enter...")
            input()
    except Exception as e:
        print(f"An error occurred: {e}")
        print("Press enter...")
        input()