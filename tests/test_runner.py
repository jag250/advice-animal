import pytest
import re
from pathlib import Path
import subprocess
from advice_animal.runner import Runner, Mode, FixConfidence

def test_inplace(tmp_git):
    Path("README.txt").write_text("Hello")
    Path("pyproject.toml").write_text("foo")
    r = Runner(
        Path(__file__).parent / "advice",
        inplace=True,
        mode=Mode.apply,
    )
    with pytest.raises(ValueError):
        results = r.run(tmp_git, FixConfidence.UNSET, preview_filter=False,
        name_filter=re.compile(r".*"))
        print(results)

    subprocess.check_call(["git", "commit", "-a", "-m", "foo"])

    results = r.run(tmp_git, FixConfidence.UNSET, preview_filter=False,
    name_filter=re.compile(r".*"))

    assert results["shouty"].success


def test_git(tmp_path):
    (tmp_path / "README.txt").write_text("Hello")
    (tmp_path / "pyproject.toml").write_text("")
    subprocess.check_call(["git", "init", "--initial-branch", "fancy-branch"],
    cwd=tmp_path)
    subprocess.check_call(["git", "add", "-A"], cwd=tmp_path)
    subprocess.check_call(["git", "commit", "-m", "foo"], cwd=tmp_path)
    r = Runner(
        Path(__file__).parent / "advice",
        inplace=True,
        mode=Mode.apply,
    )
    results = r.run(tmp_path, FixConfidence.UNSET, preview_filter=False,
    name_filter=re.compile(r".*"))
    assert results["shouty"].success
