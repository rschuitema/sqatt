"""Unit test for the resharper profile functions."""
from unittest.mock import Mock, patch, mock_open, call

import xmltodict


from src.resharper.resharper_profile import create_report_directory, determine_projects, determine_issue_types, \
    determine_issue_category, determine_issues_per_project, determine_issues_per_category, \
    determine_issues_per_issuetype, save_issues_per_project, save_issues_per_issue_type, save_issues_per_category, \
    save_issues


@patch('os.path.exists')
def test_create_report_directory_directory_exists(path_exists_mock):
    """Test that the create report directory does not create the directory when it already exists."""

    # arrange

    directory = r"c:\temp\reports"
    path_exists_mock.return_value = True

    # act
    report_dir = create_report_directory(directory)

    # assert
    assert directory == report_dir
    path_exists_mock.assert_called_once()


@patch('os.makedirs')
@patch('os.path.exists')
def test_create_report_directory_directory_created(path_exists_mock, makedirs_mock):
    """Test that the create report directory creates the directory when it does not exist."""

    # arrange

    directory = r"c:\temp\reports"
    path_exists_mock.return_value = False

    # act
    report_dir = create_report_directory(directory)

    # assert
    assert directory == report_dir
    path_exists_mock.assert_called_once()
    makedirs_mock.assert_called_once()


def test_determine_projects_returns_two_projects():
    """Test that determine projects returns two projects."""

    # arrange
    xml_to_read = r'<?xml version="1.0" encoding="utf-8"?>' \
                  r'<Report>' \
                  r'<Issues>' \
                  r'<Project Name="ABC">' \
                  r'</Project>' \
                  r'<Project Name="DEF">' \
                  r'</Project>' \
                  r'</Issues>' \
                  r'</Report>'

    doc = xmltodict.parse(xml_to_read)

    # act
    projects = determine_projects(doc)

    # assert
    assert len(projects) == 2
    assert projects[0]['@Name'] == "ABC"
    assert projects[1]['@Name'] == "DEF"


def test_determine_issue_types_returns_two_issue_types():
    """Test that determine issue type return 2 issue types."""

    # arrange
    xml_to_read = r'<?xml version="1.0" encoding="utf-8"?>' \
                  r'<Report>' \
                  r'<IssueTypes>' \
                  r'<IssueType Id="AccessToDisposedClosure" Category="Potential Code Quality Issues" CategoryId=' \
                  r'"CodeSmell" Description="Access to disposed closure" Severity="WARNING" WikiUrl="https://www.' \
                  r'jetbrains.com/resharperplatform/help?Keyword=AccessToDisposedClosure" />' \
                  r'<IssueType Id="AccessToModifiedClosure" Category="Potential Code Quality Issues" CategoryId=' \
                  r'"CodeSmell" Description="Access to modified closure" Severity="WARNING" WikiUrl="https://www.' \
                  r'jetbrains.com/resharperplatform/help?Keyword=AccessToModifiedClosure" />' \
                  r'</IssueTypes>' \
                  r'</Report>'

    doc = xmltodict.parse(xml_to_read)

    # act
    issue_types = determine_issue_types(doc)

    # assert
    assert len(issue_types) == 2
    assert issue_types[0]['@Id'] == "AccessToDisposedClosure"
    assert issue_types[1]['@Id'] == "AccessToModifiedClosure"


def test_determine_issue_category_returns_correct_category():
    """Test that determine issue category returns the correct category."""

    # arrange
    xml_to_read = r'<?xml version="1.0" encoding="utf-8"?>' \
                  r'<Report>' \
                  r'<IssueTypes>' \
                  r'<IssueType Id="AccessToDisposedClosure" Category="Potential Code Quality Issues" CategoryId=' \
                  r'"CodeSmell" Description="Access to disposed closure" Severity="WARNING" WikiUrl="https://www.' \
                  r'jetbrains.com/resharperplatform/help?Keyword=AccessToDisposedClosure" />' \
                  r'<IssueType Id="AccessToStaticMemberViaDerivedType" Category="Common Practices and Code ' \
                  r'Improvements" CategoryId="BestPractice" Description="Access to a static member of a type via a ' \
                  r'derived type" Severity="WARNING" WikiUrl="https://www.jetbrains.com/resharperplatform/help?' \
                  r'Keyword=AccessToStaticMemberViaDerivedType" />' \
                  r'</IssueTypes>' \
                  r'</Report>'

    doc = xmltodict.parse(xml_to_read)
    issue_types = determine_issue_types(doc)

    # act
    category = determine_issue_category('AccessToDisposedClosure', issue_types)

    # assert
    assert category == 'Potential Code Quality Issues'


def test_determine_issue_category_returns_none_when_category_not_found():
    """Test that determine issue category returns none when the category is not found."""

    # arrange
    xml_to_read = r'<?xml version="1.0" encoding="utf-8"?>' \
                  r'<Report>' \
                  r'<IssueTypes>' \
                  r'<IssueType Id="AccessToDisposedClosure" Category="Potential Code Quality Issues" CategoryId=' \
                  r'"CodeSmell" Description="Access to disposed closure" Severity="WARNING" WikiUrl="https://www.' \
                  r'jetbrains.com/resharperplatform/help?Keyword=AccessToDisposedClosure" />' \
                  r'<IssueType Id="AccessToStaticMemberViaDerivedType" Category="Common Practices and Code ' \
                  r'Improvements" CategoryId="BestPractice" Description="Access to a static member of a type via a ' \
                  r'derived type" Severity="WARNING" WikiUrl="https://www.jetbrains.com/resharperplatform/help?' \
                  r'Keyword=AccessToStaticMemberViaDerivedType" />' \
                  r'</IssueTypes>' \
                  r'</Report>'

    doc = xmltodict.parse(xml_to_read)
    issue_types = determine_issue_types(doc)

    # act
    category = determine_issue_category('ABC', issue_types)

    # assert
    assert category is None


def test_determine_issues_per_project_return_correct_values():
    """Test that the issues per project returns the correct values."""

    # arrange
    xml_to_read = r'<?xml version="1.0" encoding="utf-8"?>' \
                  r'<Report>' \
                  r'<Issues>' \
                  r'<Project Name="ABC">' \
                  r'<Issue TypeId="UnusedMember.Global" File="a\b\c\
                  d.cs" Offset="1238-1256" Line="27" Message="Property \'' \
                  r'AccelerationSensor\' is never used" />' \
                  r'<Issue TypeId="UnusedMember.Global" File="a\b\c\
                  d.cs" Offset="1584-1614" Line="38" Message="Property \'' \
                  r'ActiveVibrationIsolationModule\' is never used" />' \
                  r'<Issue TypeId="MemberCanBePrivate.Global" File="a\b\
                  c\dGen.cs" Offset="2268-2277" Line="48" Message=' \
                  r'"Field \'_logger\' can be made private" /> ' \
                  r'</Project>' \
                  r'<Project Name="DEF">' \
                  r'<Issue TypeId="UnusedMember.Global" File="a\b\c\
                  d.cs" Offset="1238-1256" Line="27" Message="Property \'' \
                  r'AccelerationSensor\' is never used" />' \
                  r'<Issue TypeId="UnusedMember.Global" File="a\b\c\
                  d.cs" Offset="1584-1614" Line="38" Message="Property \'' \
                  r'ActiveVibrationIsolationModule\' is never used" />' \
                  r'</Project>' \
                  r'</Issues>' \
                  r'</Report>'

    doc = xmltodict.parse(xml_to_read)

    # act
    issues_per_project = determine_issues_per_project(doc)

    # assert
    assert len(issues_per_project) == 2
    assert issues_per_project['ABC'] == 3
    assert issues_per_project['DEF'] == 2


def test_determine_issues_per_category_one_category_correct_count():
    """Test that the count for issues per category is correct."""

    # arrange
    xml_to_read = r'<?xml version="1.0" encoding="utf-8"?>' \
                  r'<Report>' \
                  r'<IssueTypes>' \
                  r'<IssueType Id="UnusedMember.Global" Category="Potential Code Quality Issues" CategoryId=' \
                  r'"CodeSmell" Description="Access to disposed closure" Severity="WARNING" WikiUrl="https://www.' \
                  r'jetbrains.com/resharperplatform/help?Keyword=AccessToDisposedClosure" />' \
                  r'<IssueType Id="AccessToModifiedClosure" Category="Potential Code Quality Issues" CategoryId=' \
                  r'"CodeSmell" Description="Access to modified closure" Severity="WARNING" WikiUrl="https://www.' \
                  r'jetbrains.com/resharperplatform/help?Keyword=AccessToModifiedClosure" />' \
                  r'</IssueTypes>' \
                  r'<Issues>' \
                  r'<Project Name="ABC">' \
                  r'<Issue TypeId="UnusedMember.Global" File="a\b\c\
                  d.cs" Offset="1238-1256" Line="27" Message="Property \'' \
                  r'AccelerationSensor\' is never used" />' \
                  r'<Issue TypeId="UnusedMember.Global" File="a\b\c\
                  d.cs" Offset="1584-1614" Line="38" Message="Property \'' \
                  r'ActiveVibrationIsolationModule\' is never used" />' \
                  r'</Project>' \
                  r'<Project Name="DEF">' \
                  r'<Issue TypeId="UnusedMember.Global" File="a\b\c\
                  d.cs" Offset="1238-1256" Line="27" Message="Property \'' \
                  r'AccelerationSensor\' is never used" />' \
                  r'<Issue TypeId="UnusedMember.Global" File="a\b\c\
                  d.cs" Offset="1584-1614" Line="38" Message="Property \'' \
                  r'ActiveVibrationIsolationModule\' is never used" />' \
                  r'</Project>' \
                  r'</Issues>' \
                  r'</Report>'

    doc = xmltodict.parse(xml_to_read)

    # act
    issues_per_category = determine_issues_per_category(doc)

    # assert
    assert len(issues_per_category) == 1
    assert issues_per_category['Potential Code Quality Issues'] == 4


def test_determine_issues_per_category_one_issue_in_category_count_is_one():
    """Test that the count is one if there is only one issue in the category."""

    # arrange
    xml_to_read = r'<?xml version="1.0" encoding="utf-8"?>' \
                  r'<Report>' \
                  r'<IssueTypes>' \
                  r'<IssueType Id="UnusedMember.Global" Category="Potential Code Quality Issues" CategoryId=' \
                  r'"CodeSmell" Description="Access to disposed closure" Severity="WARNING" WikiUrl="https://www.j' \
                  r'etbrains.com/resharperplatform/help?Keyword=AccessToDisposedClosure" />' \
                  r'<IssueType Id="AccessToModifiedClosure" Category="Potential Code Quality Issues" CategoryId=' \
                  r'"CodeSmell" Description="Access to modified closure" Severity="WARNING" WikiUrl="https://www.' \
                  r'jetbrains.com/resharperplatform/help?Keyword=AccessToModifiedClosure" />' \
                  r'</IssueTypes>' \
                  r'<Issues>' \
                  r'<Project Name="ABC">' \
                  r'<Issue TypeId="UnusedMember.Global" File="a\b\c\
                  d.cs" Offset="1238-1256" Line="27" Message="Property \'' \
                  r'AccelerationSensor\' is never used" />' \
                  r'</Project>' \
                  r'</Issues>' \
                  r'</Report>'

    doc = xmltodict.parse(xml_to_read)

    # act
    issues_per_category = determine_issues_per_category(doc)

    # assert
    assert len(issues_per_category) == 1
    assert issues_per_category['Potential Code Quality Issues'] == 1


def test_determine_issues_per_type_one_issuetype_count_correct():
    """Test that the count of the issues per issuetype is correct."""

    # arrange
    xml_to_read = r'<?xml version="1.0" encoding="utf-8"?>' \
                  r'<Report>' \
                  r'<IssueTypes>' \
                  r'<IssueType Id="UnusedMember.Global" Category="Potential Code Quality Issues" CategoryId=' \
                  r'"CodeSmell" Description="Access to disposed closure" Severity="WARNING" WikiUrl="https://www.' \
                  r'jetbrains.com/resharperplatform/help?Keyword=AccessToDisposedClosure" />' \
                  r'<IssueType Id="AccessToModifiedClosure" Category="Potential Code Quality Issues" CategoryId="' \
                  r'CodeSmell" Description="Access to modified closure" Severity="WARNING" WikiUrl="https://www.' \
                  r'jetbrains.com/resharperplatform/help?Keyword=AccessToModifiedClosure" />' \
                  r'</IssueTypes>' \
                  r'<Issues>' \
                  r'<Project Name="ABC">' \
                  r'<Issue TypeId="UnusedMember.Global" File="a\b\c\
                  d.cs" Offset="1238-1256" Line="27" Message="Property \'' \
                  r'AccelerationSensor\' is never used" />' \
                  r'<Issue TypeId="UnusedMember.Global" File="a\b\c\
                  d.cs" Offset="1238-1256" Line="27" Message="Property \'' \
                  r'AccelerationSensor\' is never used" />' \
                  r'</Project>' \
                  r'<Project Name="DEF">' \
                  r'<Issue TypeId="UnusedMember.Global" File="a\b\c\
                  d.cs" Offset="1238-1256" Line="27" Message="Property \'' \
                  r'AccelerationSensor\' is never used" />' \
                  r'<Issue TypeId="UnusedMember.Global" File="a\b\c\
                  d.cs" Offset="1584-1614" Line="38" Message="Property \'' \
                  r'ActiveVibrationIsolationModule\' is never used" />' \
                  r'</Project>' \
                  r'</Issues>' \
                  r'</Report>'

    doc = xmltodict.parse(xml_to_read)

    # act
    issues_per_issue_type = determine_issues_per_issuetype(doc)

    # assert
    assert len(issues_per_issue_type) == 1
    assert issues_per_issue_type['UnusedMember.Global'] == 4


def test_determine_issues_per_issuetype_one_issue_in_issuetype_count_is_one():
    """Test that count is one if there is on issue in issuetype."""

    # arrange
    xml_to_read = r'<?xml version="1.0" encoding="utf-8"?>' \
                  r'<Report>' \
                  r'<IssueTypes>' \
                  r'<IssueType Id="UnusedMember.Global" Category="Potential Code Quality Issues" CategoryId=' \
                  r'"CodeSmell" Description="Access to disposed closure" Severity="WARNING" WikiUrl="https://www.' \
                  r'jetbrains.com/resharperplatform/help?Keyword=AccessToDisposedClosure" />' \
                  r'<IssueType Id="AccessToModifiedClosure" Category="Potential Code Quality Issues" CategoryId=' \
                  r'"CodeSmell" Description="Access to modified closure" Severity="WARNING" WikiUrl="https://www.' \
                  r'jetbrains.com/resharperplatform/help?Keyword=AccessToModifiedClosure" />' \
                  r'</IssueTypes>' \
                  r'<Issues>' \
                  r'<Project Name="ABC">' \
                  r'<Issue TypeId="UnusedMember.Global" File="a\b\c\
                  d.cs" Offset="1238-1256" Line="27" Message="Property \'' \
                  r'AccelerationSensor\' is never used" />' \
                  r'</Project>' \
                  r'</Issues>' \
                  r'</Report>'

    doc = xmltodict.parse(xml_to_read)

    # act
    issues_per_issue_type = determine_issues_per_issuetype(doc)

    # assert
    assert len(issues_per_issue_type) == 1
    assert issues_per_issue_type['UnusedMember.Global'] == 1


@patch('src.resharper.resharper_profile.save_issues')
def test_save_issues_per_project(save_issues_mock):
    """Test that the issues can be saver per project."""

    # arrange
    report_dir = r'C:\temp'
    issues_per_project = {}

    expected_file = r'C:\temp\issues_per_project.csv'
    expected_item_name = r'Project'

    # act
    save_issues_per_project(issues_per_project, report_dir)

    # assert
    save_issues_mock.assert_called_once()
    save_issues_mock.assert_called_with(issues_per_project, expected_file, expected_item_name)


@patch('src.resharper.resharper_profile.save_issues')
def test_save_issues_per_issue_type(save_issues_mock):
    """Test that the issues can be saver per type."""

    # arrange
    report_dir = r'C:\temp'
    issues_per_project = {}

    expected_file = r'C:\temp\issues_per_issue_type.csv'
    expected_item_name = r'Issue Type'

    # act
    save_issues_per_issue_type(issues_per_project, report_dir)

    # assert
    save_issues_mock.assert_called_once()
    save_issues_mock.assert_called_with(issues_per_project, expected_file, expected_item_name)


@patch('src.resharper.resharper_profile.save_issues')
def test_save_issues_per_category(save_issues_mock):
    """Test that the issues can be saver per category."""

    # arrange
    report_dir = r'C:\temp'
    issues_per_project = {}

    expected_file = r'C:\temp\issues_per_category.csv'
    expected_item_name = r'Category'

    # act
    save_issues_per_category(issues_per_project, report_dir)

    # assert
    save_issues_mock.assert_called_once()
    save_issues_mock.assert_called_with(issues_per_project, expected_file, expected_item_name)


@patch('src.resharper.resharper_profile.csv')
def test_save_issues(csv_mock):
    """Test that the resulting issues can be saved."""

    items = {'A': 15, 'b': 8}
    csv_mock.writer = Mock(writerow=Mock())
    report_file = r'c:\temp\temp.csv'
    calls = [call.writerow(['caption', 'Number of violations']), call.writerow(['A', 15]), call.writerow(['b', 8])]
    with patch('src.resharper.resharper_profile.open', mock_open()) as mocked_file:
        save_issues(items, report_file, 'caption')

        mocked_file.assert_called_once_with(report_file, 'w')

        csv_mock.writer().assert_has_calls(calls)
