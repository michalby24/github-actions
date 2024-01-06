import os
import subprocess

def has_helm_files_changed():
    result = subprocess.run(
        ["git", "diff", "--name-only", "HEAD@{1}", "HEAD", "--", "helm/"],
        capture_output=True,
        text=True,
    )
    
    return bool(result.stdout.strip())

def bump_version():
    subprocess.run(["git", "checkout", "-qf", "master"])

    version_result = subprocess.run(
        ["awk", "/version/{print $2; exit}", "./helm/Chart.yaml"],
        capture_output=True,
        text=True,
        cwd="./helm",
    )

    current_version = version_result.stdout.strip()

    new_version_result = subprocess.run(
        [
            "awk",
            "-F.",
            "-v",
            "OFS=",
            '{ $NF++; print }',
        ],
        input=current_version,
        capture_output=True,
        text=True,
    )

    new_version = new_version_result.stdout.strip()

    subprocess.run(
        [
            "stefanzweifel/git-auto-commit-action@v4",
            "--commit-message",
            f"chore(release) bump version to {new_version}",
            "--file-pattern",
            "./helm/Chart.yaml",
        ]
    )

    return new_version

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



if __name__ == "__main__":
    new_version = get_chart_version()
    print(f"Bumped version to {new_version}")