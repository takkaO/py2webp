import pathlib
import os
import sys
import subprocess

def main(target_list):
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
            print("Press enter to continue.")
            input()
            continue
        os.remove(target)
        print("## ({0}/{1}) Complete!".format(i+1, len(target_list)))
        print("--------------------")

if __name__ == "__main__":
    main(sys.argv[1:])

    print("Press enter...")
    input()