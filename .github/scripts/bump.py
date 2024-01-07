import os
import subprocess
import fileinput
import shutil

def has_helm_files_changed():
    result = subprocess.run(
        ["git", "diff", "--name-only", "HEAD@{1}", "HEAD", "--", "helm/"],
        capture_output=True,
        text=True,
    )
    
    return bool(result.stdout.strip())

def get_chart_version():
    chart_path = os.path.join("helm", "Chart.yaml")

    with open(chart_path, "r") as chart_file:
        for line in chart_file.readlines():
            if line.startswith("version:"):
                version = line.split(":")[1].strip()
                return version

    return ""

def bump_version_segments2(version, condition_index=2):
    # Split the version into segments
    segments = version.split(".")

    # Check if the condition_index is within the valid range
    if 0 <= condition_index < len(segments):
        # Increment the specified segment by 1
        segments[condition_index] = str(int(segments[condition_index]) + 1)

        # Join the segments to get the new version
        new_version = ".".join(segments)
        return new_version
    else:
        print(f"Invalid condition_index: {condition_index}")
        return version

def change_version_in_chart(new_version):
    chart_path = os.path.join("helm", "Chart.yaml")
    github_token = os.environ.get("GITHUB_TOKEN") 
    # Use sed to replace the version line
    subprocess.run(["sed", "-i", f"s/^version: .*/version: {new_version}/", chart_path])
    subprocess.run(["git", "config", "--global", "user.email", "github-actions@github.com"])
    subprocess.run(["git", "config", "--global", "user.name", "GitHub Actions"])
    subprocess.run(["git", "add", chart_path])
    subprocess.run(["git", "commit", "-m", f"chore(release): bump version to {new_version}"])
    subprocess.run(["git", "fetch"])
    subprocess.run(["git", "merge", "--ff-only", "origin/master"])
    subprocess.run(["git", "push", "origin", "master"])


def bump_version_segments(version, condition_index=2):
    # Split the version into segments
    segments = list(map(int, version.split(".")))

    # Check if the condition_index is within the valid range
    if 0 <= condition_index < len(segments):
        # Increment the specified segment by 1
        segments[condition_index] += 1

        # Check if the incremented segment reaches 9, reset to 0 and bump the next segment
        if segments[condition_index] == 10:
            segments[condition_index] = 0
            if condition_index + 1 < len(segments):
                segments[condition_index + 1] += 1

        # Convert segments back to string and join to get the new version
        new_version = ".".join(map(str, segments))
        return new_version
    else:
        print(f"Invalid condition_index: {condition_index}")
        return version


if __name__ == "__main__":
    if True:
        new_version = bump_version_segments(get_chart_version(), 2) 
        change_version_in_chart(new_version)
        print(f"Bumped version to {new_version}")
    else:
        print("No changes in the helm directory.")