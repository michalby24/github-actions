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

# def bump_version():
#     subprocess.run(["git", "checkout", "-qf", "master"])

#     version_result = subprocess.run(
#         ["awk", "/version/{print $2; exit}", "./helm/Chart.yaml"],
#         capture_output=True,
#         text=True,
#         cwd="./helm",
#     )

#     current_version = version_result.stdout.strip()

#     new_version_result = subprocess.run(
#         [
#             "awk",
#             "-F.",
#             "-v",
#             "OFS=",
#             '{ $NF++; print }',
#         ],
#         input=current_version,
#         capture_output=True,
#         text=True,
#     )

#     new_version = new_version_result.stdout.strip()

#     subprocess.run(
#         [
#             "stefanzweifel/git-auto-commit-action@v4",
#             "--commit-message",
#             f"chore(release) bump version to {new_version}",
#             "--file-pattern",
#             "./helm/Chart.yaml",
#         ]
#     )

#     return new_version

# if __name__ == "__main__":
#     if has_helm_files_changed():
#         new_version = bump_version()
#         print(f"Bumped version to {new_version}")
#     else:
#         print("No changes in the helm directory.")

def get_chart_version():
    chart_path = os.path.join("helm", "Chart.yaml")

    with open(chart_path, "r") as chart_file:
        for line in chart_file.readlines():
            if line.startswith("version:"):
                version = line.split(":")[1].strip()
                return version

    return ""

def bump_version_segments(version, condition_index=2):
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


def change_version_in_chart(version):
    chart_path = os.path.join("helm", "Chart.yaml")
    temp_chart_path = os.path.join("helm", "Chart_temp.yaml")

    found_version_line = False

    with open(chart_path, "r") as input_file, open(temp_chart_path, "w") as output_file:
        for line in input_file:
            if line.startswith("version:") and not found_version_line:
                output_file.write(f"version: {version}\n")
                found_version_line = True
            else:
                output_file.write(line)

    shutil.move(temp_chart_path, chart_path)


def change_version_in_chart2(new_version):
    chart_path = os.path.join("helm", "Chart.yaml")

    # Use sed to replace the version line
    subprocess.run(["sed", "-i", f"s/^version: .*/version: {new_version}/", chart_path])
    subprocess.run(["git", "add", chart_path])
    subprocess.run(["git", "commit", "-m", f"chore(release): bump version to {new_version}"])

# if __name__ == "__main__":
#     new_version = get_chart_version()
#     print(f"Bumped version to {new_version}")

if __name__ == "__main__":
    github_token = os.environ.get("GITHUB_TOKEN")
    if True:
        new_version = bump_version_segments(get_chart_version(), 1) 
        change_version_in_chart2(new_version)
        print(f"Bumped version to {new_version}")
    else:
        print("No changes in the helm directory.")