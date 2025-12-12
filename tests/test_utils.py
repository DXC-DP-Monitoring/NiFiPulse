import pytest
import os
from unittest.mock import patch
from nifipulse.utils import abs_ff_path, path_tofile, path_tofolder, _csv_has_rows

# TEST abs_ff_path()

def test_abs_ff_path_returns_absolute_path(tmp_path):
    rel = "testfile.txt"
    abs_path = abs_ff_path(rel)
    assert os.path.isabs(abs_path)


# TEST path_tofile()

def test_path_tofile_true(tmp_path):

    file = tmp_path / "file.txt"
    file.write_text("hello")
    assert path_tofile(str(file)) is True


def test_path_tofile_false(tmp_path):
  
    fake_file = tmp_path / "nofile.txt"
    assert path_tofile(str(fake_file)) is False


# TEST path_tofolder()

def test_path_tofolder_true(tmp_path):
    
    folder = tmp_path / "subfolder"
    folder.mkdir()

    assert path_tofolder(str(folder)) is True


def test_path_tofolder_false(tmp_path):

    fake_folder = tmp_path / "does_not_exist"
    assert path_tofolder(str(fake_folder)) is False


# TEST _csv_has_rows()

def test_csv_has_rows_true(tmp_path):

    csvfile = tmp_path / "data.csv"
    csvfile.write_text("col1,col2\n1,2\n")
    assert _csv_has_rows(str(csvfile)) is True


def test_csv_has_rows_false_empty(tmp_path):

    csvfile = tmp_path / "empty.csv"
    csvfile.write_text("col1,col2\n")
    assert _csv_has_rows(str(csvfile)) is False


def test_csv_has_rows_missing_file():
 
    assert _csv_has_rows("missing.csv") is False

