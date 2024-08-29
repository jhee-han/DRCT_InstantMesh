import os
import shutil

def clear_directory_contents(directory):
    if os.path.exists(directory):
        # 디렉토리 안의 모든 파일과 서브디렉토리를 삭제
        for item in os.listdir(directory):
            item_path = os.path.join(directory, item)
            if os.path.isfile(item_path) or os.path.islink(item_path):
                os.unlink(item_path)
            elif os.path.isdir(item_path):
                shutil.rmtree(item_path)
        print(f"Cleared contents of directory: {os.path.abspath(directory)}")
    else:
        print(f"Directory does not exist: {os.path.abspath(directory)}")

def main():
    # 내부 콘텐츠를 삭제할 디렉터리 목록 (상대 경로로 지정)
    directories_to_clear = [
        "./DRCT/datasets",
        "./DRCT/results",
        "./IPG/imgs",
        "./IPG/results"
    ]
    
    # 디렉터리 내부의 파일과 폴더들만 삭제
    for directory in directories_to_clear:
        clear_directory_contents(directory)

if __name__ == "__main__":
    main()
