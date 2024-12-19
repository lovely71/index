import os
import subprocess
import time

def git_push_with_retry():
    max_retries = 50
    retry_delay = 10
    for attempt in range(max_retries):
        try:
            subprocess.run(['git', 'push'], check=True)
            print("成功推送到git仓库")
            return True
        except subprocess.CalledProcessError as push_error:
            if attempt < max_retries - 1:
                print(f"推送失败，{retry_delay}秒后重试 (尝试 {attempt + 1}/{max_retries})")
                time.sleep(retry_delay)
            else:
                raise push_error

def git_add_commit_push():
    try:
        # 获取脚本所在目录并切换到该目录
        script_dir = os.path.dirname(os.path.abspath(__file__))
        os.chdir(script_dir)
        print(f"当前工作目录: {script_dir}")
        
        # 检查是否有未提交的更改
        status = subprocess.run(['git', 'status', '--porcelain'], capture_output=True, text=True, check=True)
        
        # 检查是否有未推送的提交
        unpushed = subprocess.run(['git', 'status'], capture_output=True, text=True, check=True)
        if "Your branch is ahead of" in unpushed.stdout:
            print("检测到未推送的提交，尝试推送...")
            git_push_with_retry()
            return
        
        if not status.stdout:
            print("没有需要提交的更改")
            return
        
        # Git 操作
        subprocess.run(['git', 'add', '.'], check=True)
        commit_message = f"Auto commit at {time.strftime('%Y-%m-%d %H:%M:%S')}"
        subprocess.run(['git', 'commit', '-m', commit_message], check=True)
        
        # 使用重试机制进行推送
        git_push_with_retry()
        
    except subprocess.CalledProcessError as e:
        print(f"Git操作失败: {str(e)}")

if __name__ == "__main__":
    git_add_commit_push()

