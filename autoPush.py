import os
import subprocess
import time

def git_add_commit_push():
    try:
        # 获取脚本所在目录并切换到该目录
        script_dir = os.path.dirname(os.path.abspath(__file__))
        os.chdir(script_dir)
        print(f"当前工作目录: {script_dir}")
        
        # 检查是否有未提交的更改
        status = subprocess.run(['git', 'status', '--porcelain'], capture_output=True, text=True, check=True)
        if status.stdout:
            # 如果有更改，先stash保存
            subprocess.run(['git', 'stash'], check=True)
            print("已暂存当前更改")
        
        # Git 操作
        subprocess.run(['git', 'add', '.'], check=True)
        commit_message = f"Auto commit at {time.strftime('%Y-%m-%d %H:%M:%S')}"
        subprocess.run(['git', 'commit', '-m', commit_message], check=True)
        subprocess.run(['git', 'push'], check=True)
        
        # 恢复之前暂存的更改
        if status.stdout:
            subprocess.run(['git', 'stash', 'pop'], check=True)
            print("已恢复暂存的更改")
            
        print("成功推送到git仓库")
        
    except subprocess.CalledProcessError as e:
        print(f"Git操作失败: {str(e)}")

if __name__ == "__main__":
    git_add_commit_push()

