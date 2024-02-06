import os
import subprocess

def update_chart_version(new_version):
    chart_path = os.path.join("helm", "Chart.yaml")
    commands = f"""
        sed -i 's/^version:.*/version: {new_version}/' {chart_path};
        sed -i 's/^appVersion:.*/appVersion: {new_version}/' {chart_path};
        git config --global user.email 'github-actions@github.com';
        git config --global user.name 'GitHub Actions';
        git add {chart_path};
        git commit -m 'chore(release): bump version to {new_version}';
        git push origin master;
    """
    subprocess.run(commands, shell=True)

if __name__ == "__main__":
    new_version = os.environ.get('VERSION')
    update_chart_version(new_version)
    print(f"Bumped version to {new_version}")
    print(f"::set-output name=NEW_VERSION::{new_version}")

