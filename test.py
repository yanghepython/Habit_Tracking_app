import pytest
from unittest.mock import patch
import sqlite3
from datetime import datetime
from db import add_habit, increment_habit,get_habit_tracking_data, get_all_habits,delete_habit
from habit import Habit
from analyse import plot_streaks_as_table  # 假设该函数已经存在


# 设置数据库的模拟数据
@pytest.fixture
def setup_mock_db():
    """Fixture to set up a mock SQLite database and insert mock data."""

    # 连接到 SQLite 内存数据库 (创建临时数据库)
    conn = sqlite3.connect(':memory:')  # 使用内存数据库避免写入文件
    cursor = conn.cursor()

    # 创建习惯表
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS tbl_habit (
            name TEXT PRIMARY KEY,
            frequency TEXT,
            streak INTEGER DEFAULT 0,
            last_completed DATE
        )
        ''')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS tbl_tracker (
            habitname TEXT,
            completed_date DATE,
            FOREIGN KEY (habitname) REFERENCES tbl_habit (name) ON DELETE CASCADE
        )
        ''')


    # 插入模拟数据
    cursor.executemany('''
        INSERT INTO tbl_habit (name, frequency, streak, last_completed)
        VALUES (?, ?, ?, ?)
        ''', [
        ('English learning', 'daily', 30, '2024-11-30'),
        ('Teeth protection with Elmex gelee', 'weekly', 6, '2024-11-27'),
        ('Financial review', 'monthly', 1, '2024-11-01'),
    ])

    cursor.executemany('''
       INSERT INTO tbl_tracker (habitname, completed_date)
       VALUES (?, ?)
       ''',  [
        ('English learning', '2024-11-01'), ('English learning', '2024-11-02'),
        ('English learning', '2024-11-03'), ('English learning', '2024-11-04'),
        ('English learning', '2024-11-05'), ('English learning', '2024-11-06'),
        ('English learning', '2024-11-07'), ('English learning', '2024-11-08'),
        ('English learning', '2024-11-09'), ('English learning', '2024-11-10'),
        ('English learning', '2024-11-11'), ('English learning', '2024-11-12'),
        ('English learning', '2024-11-13'), ('English learning', '2024-11-14'),
        ('English learning', '2024-11-15'), ('English learning', '2024-11-16'),
        ('English learning', '2024-11-17'), ('English learning', '2024-11-18'),
        ('English learning', '2024-11-19'), ('English learning', '2024-11-20'),
        ('English learning', '2024-11-21'), ('English learning', '2024-11-22'),
        ('English learning', '2024-11-23'), ('English learning', '2024-11-24'),
        ('English learning', '2024-11-25'), ('English learning', '2024-11-26'),
        ('English learning', '2024-11-27'), ('English learning', '2024-11-28'),
        ('English learning', '2024-11-29'), ('English learning', '2024-11-30'),
        ('Teeth protection with Elmex gelee', '2024-11-06'),
        ('Teeth protection with Elmex gelee', '2024-11-13'),
        ('Teeth protection with Elmex gelee', '2024-11-20'),
        ('Teeth protection with Elmex gelee', '2024-11-27'),
        ('Financial review', '2024-11-01')
    ])

    conn.commit()
    yield conn  # 返回真实的 SQLite 连接

    # 测试完成后清理数据库
    conn.close()


def test_add_habit(setup_mock_db):
    db = setup_mock_db

    # 测试插入新习惯
    add_habit(db, 'Morning yoga', 'daily')
    cursor = db.cursor()

    cursor.execute("SELECT * FROM tbl_habit WHERE name = 'Morning yoga'")
    new_habit = cursor.fetchone()
    assert new_habit is not None  # 确保新习惯已插入
    assert new_habit[0] == 'Morning yoga'  # 确保习惯名称正确
    assert new_habit[1] == 'daily'  # 确保频率正确

    # 测试插入已存在的习惯
    with pytest.raises(sqlite3.IntegrityError):
        add_habit(db, 'English learning', 'daily')


    # 验证数据库中仍然只有一个 'English learning' 条目
    cursor.execute("SELECT COUNT(*) FROM tbl_habit WHERE name = 'English learning'")
    count = cursor.fetchone()[0]
    assert count == 1  # 确保'English learning' 只存在一个条目

def test_increment_habit_with_mock_data(setup_mock_db):
    db = setup_mock_db
    today = datetime.now().date()

    # 验证初始 streak 和完成记录数量
    cursor = db.cursor()
    cursor.execute("SELECT streak FROM tbl_habit WHERE name = ?", ('English learning',))
    initial_streak = cursor.fetchone()[0]
    assert initial_streak == 30  # 确保初始 streak 是 mock 数据设置的值

    cursor.execute("SELECT COUNT(*) FROM tbl_tracker WHERE habitname = ?", ('English learning',))
    initial_count = cursor.fetchone()[0]
    assert initial_count == 30  # 确保完成记录数量与 mock 数据一致

    # 测试标记完成习惯
    increment_habit(db, 'English learning')

    # 验证 streak 是否更新
    cursor.execute("SELECT streak FROM tbl_habit WHERE name = ?", ('English learning',))
    updated_streak = cursor.fetchone()[0]
    assert updated_streak == 31

    # 验证 tbl_tracker 中记录是否新增
    cursor.execute("SELECT COUNT(*) FROM tbl_tracker WHERE habitname = ?", ('English learning',))
    updated_count = cursor.fetchone()[0]
    assert updated_count == 31

    cursor.execute("SELECT * FROM tbl_tracker WHERE habitname = ? AND completed_date = ?", ('English learning', today))
    new_record = cursor.fetchone()
    assert new_record is not None
    assert new_record[1] == str(today)

    # 测试重复完成同一天
    increment_habit(db, 'English learning')
    cursor.execute("SELECT COUNT(*) FROM tbl_tracker WHERE habitname = ?", ('English learning',))
    repeated_count = cursor.fetchone()[0]
    assert repeated_count == 31

def test_get_habit_tracking_data(setup_mock_db):
    db = setup_mock_db

    # 测试获取 'English learning' 习惯的所有完成日期
    result = get_habit_tracking_data(db, 'English learning')

    # 验证返回的数据
    assert len(result) == 30  # 应该返回30天的记录
    assert result[0][0] == '2024-11-01'  # 第一个完成日期应该是 '2024-11-01'
    assert result[-1][0] == '2024-11-30'  # 最后一个完成日期应该是 '2024-11-30'
    assert result == [("2024-11-" + str(i).zfill(2),) for i in range(1, 31)]  # 完成日期应该按顺序排列

    # 测试获取 'Teeth protection with Elmex gelee' 习惯的所有完成日期
    result = get_habit_tracking_data(db, 'Teeth protection with Elmex gelee')

    # 验证返回的数据
    assert len(result) == 4  # 应该返回4个记录
    assert result[0][0] == '2024-11-06'  # 第一个完成日期应该是 '2024-11-06'
    assert result[-1][0] == '2024-11-27'  # 最后一个完成日期应该是 '2024-11-27'

    # 测试获取不存在的习惯
    result = get_habit_tracking_data(db, 'Non-existent habit')
    assert result == []  # 应该返回空列表

def test_get_all_habits(setup_mock_db):
    db = setup_mock_db

    # 测试获取所有习惯的数据
    result = get_all_habits(db)

    # 验证返回的数据
    assert len(result) == 3  # 应该返回 3 个习惯
    # 验证 'English learning' 习惯的值
    english_learning = next(habit for habit in result if habit[0] == 'English learning')
    assert english_learning[0] == 'English learning'  # 名称
    assert english_learning[1] == 'daily'  # 频率
    assert english_learning[2] == 30  # streak
    assert english_learning[3] == 30  # completed (30 completed dates)
    assert english_learning[4] == '2024-11-30'  # last_completed


    Elmex_gelee = next(habit for habit in result if habit[0] == 'Teeth protection with Elmex gelee')
    assert Elmex_gelee[0] == 'Teeth protection with Elmex gelee'  # 名称
    assert Elmex_gelee[1] == 'weekly'
    assert Elmex_gelee[2] == 6  # streak
    assert Elmex_gelee[3] == 4  # completed (4 completed dates)
    assert Elmex_gelee[4] == '2024-11-27'  # last_completed


    financial_review = next(habit for habit in result if habit[0] == 'Financial review')
    assert financial_review[0] == 'Financial review'
    assert financial_review[1] == 'monthly'
    assert financial_review[2] == 1  # streak
    assert financial_review[3] == 1  # completed (1 completed date)
    assert financial_review[4] == '2024-11-01'  # last_completed


    habit_names = [habit[0] for habit in result]
    assert habit_names == sorted(habit_names)  # 应该按习惯名称排序

def test_delete_habit(setup_mock_db):
    db = setup_mock_db


    habits_before_delete = get_all_habits(db)
    assert len(habits_before_delete) == 3  # 确保有 3 个习惯

    tracking_data_before_delete = get_habit_tracking_data(db, 'English learning')
    assert len(tracking_data_before_delete) == 30  # 'English learning' 应该有 30 天的跟踪数据


    delete_habit(db, 'English learning')


    habits_after_delete = get_all_habits(db)
    assert len(habits_after_delete) == 2
    assert not any(habit[0] == 'English learning' for habit in habits_after_delete)  # 确保 'English learning' 不在习惯列表中


    tracking_data_after_delete = get_habit_tracking_data(db, 'English learning')
    assert len(tracking_data_after_delete) == 0  # 'English learning' 的跟踪数据应该被删除


    try:
        delete_habit(db, 'Non-existing habit')
    except Exception as e:
        pytest.fail(f"Unexpected error: {e}")

    habits_after_invalid_delete = get_all_habits(db)
    assert len(habits_after_invalid_delete) == 2

def test_mark_completed_with_mock_data(setup_mock_db):
    db = setup_mock_db
    habit = Habit(name="English learning", frequency="daily")

    # 初始值，假设已经完成了30天
    habit.streak = 30
    habit.completed_dates = ['2024-11-' + str(i) for i in range(1, 31)]
    habit.last_completed = '2024-11-30'
    habit.completed_tasks = 30

    habit.mark_completed(db)

    assert habit.completed_tasks == 31  # 完成的任务数应增加1
    assert len(habit.completed_dates) == 31  # 完成日期列表长度应增加1
    assert habit.streak == 31  # 连续完成天数应增加1
    assert habit.last_completed == datetime.now().date()  # The last completion date should be updated to today

 # Verify the number of consecutive completion days returned
def test_get_current_streak_with_mock_data(setup_mock_db):
    db = setup_mock_db
    habit = Habit(name="Teeth protection with Elmex gelee", frequency="weekly", streak=6)
    streak = habit.get_current_streak()
    assert streak == habit.streak

def test_get_last_completed_with_mock_data(setup_mock_db):
    db = setup_mock_db
    habit = Habit(name="Financial review", frequency="monthly", last_completed='2024-11-01')

    last_completed = habit.get_last_completed()
    assert last_completed == habit.last_completed  # 返回值应该是 habit 对象中的 last_completed


def test_plot_streaks_as_table(setup_mock_db, capfd):
    db = setup_mock_db

    with patch('db.get_habit_tracking_data') as mock_get_habit_tracking_data, \
            patch('db.get_all_habits') as mock_get_all_habits, \
            patch('matplotlib.pyplot.show') as mock_show:

        mock_get_habit_tracking_data.side_effect = [
            [('2024-11-01'), ('2024-11-02'), ('2024-11-03')],
            [('2024-11-06'), ('2024-11-13')],
            [('2024-11-01')]
        ]

        mock_get_all_habits.return_value = [
            ('English learning', 'daily', 30, '2024-11-30'),
            ('Teeth protection with Elmex gelee', 'weekly', 6, '2024-11-27'),
            ('Financial review', 'monthly', 1, '2024-11-01')
        ]

        plot_streaks_as_table(db)

        print("mock_get_all_habits call count:", mock_get_all_habits.call_count)

        captured = capfd.readouterr()

        assert "Habit" in captured.out
        assert "English learning" in captured.out
        assert "Teeth protection with Elmex gelee" in captured.out
        assert "Financial review" in captured.out
        assert "Total Streak (Days)" in captured.out
        assert "Longest Streak (Days)" in captured.out
