import os
import subprocess

def get_chart_version():
    path = 'package.json'

    with open(path, "r") as file:
        for line in file:
            if '"version"' in line:
                print("Line detected:", line.strip())
                parts = line.split(":")
                if len(parts) >= 2:
                    #print(parts[1])
                    version = parts[1]
                    #print("Extracted version:", version)
                    #print(version)
                    return version
                #else:
                    #print("Unexpected line format:", line.strip())
        #print("No line starting with 'version' found.")
    return None

                
    raise Exception('Error with chart version')

def update_chart_version(new_version):
    print(new_version)
    chart_path = os.path.join("helm", "Chart.yaml")
    commands = f"""
        version_1=$(echo {new_version} | tr -d '"')
        sed -i 's/^version:.*/version: {version_1}/' {chart_path};
        sed -i 's/^appVersion:.*/appVersion: {version_1}/' {chart_path};
        git config --global user.email 'github-actions@github.com';
        git config --global user.name 'GitHub Actions';
        git add {chart_path};
        git commit -m 'chore(release): bump version to {version_1}';
        git push origin master;
    """

    subprocess.run(commands, shell=True)

if __name__ == "__main__":
    # new_version =  os.environ['VERSION']
    # if(new_version):
    #     update_chart_version(new_version)
    # else:
    #     update_chart_version(get_chart_version())
   # new_version=get_chart_version()
    michs = get_chart_version()
    # print(michs.strip('"'))
    update_chart_version(michs)
    #update_chart_version("2.8.2")
    #print(f"Bumped version to {new_version}")
    #print(f"::set-output name=NEW_VERSION::{new_version}")

