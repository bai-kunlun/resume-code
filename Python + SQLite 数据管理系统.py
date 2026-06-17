# 导入内置数据库模块
import sqlite3
import pandas as pd

# ========== 1. 连接数据库（不存在则自动创建） ==========
conn = sqlite3.connect("员工信息数据库.db")
cursor = conn.cursor()

# ========== 2. 创建员工信息表（建表语句，SQL基础） ==========
# 如果表已存在，先删除（方便重复测试）
cursor.execute("DROP TABLE IF EXISTS staff;")

# 创建数据表
create_sql = """
CREATE TABLE staff (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    department TEXT,
    salary INTEGER,
    age INTEGER
)
"""
cursor.execute(create_sql)
print("数据表创建成功！")

# ========== 3. 批量插入测试数据（SQL插入） ==========
staff_list = [
    ("张三", "技术部", 8000, 25),
    ("李四", "市场部", 7000, 23),
    ("王五", "技术部", 9500, 28),
    ("赵六", "行政部", 5500, 24),
    ("钱七", "市场部", 6800, 26)
]
insert_sql = "INSERT INTO staff (name, department, salary, age) VALUES (?, ?, ?, ?)"
cursor.executemany(insert_sql, staff_list)
conn.commit()  # 提交事务，保存数据
print("批量插入员工数据完成！")

# ========== 4. 基础查询功能 ==========
# 4.1 查询所有员工
print("\n===== 全部员工信息 =====")
cursor.execute("SELECT * FROM staff;")
all_data = cursor.fetchall()
for row in all_data:
    print(row)

# 4.2 条件查询：查询技术部员工（条件筛选）
print("\n===== 技术部员工 =====")
cursor.execute("SELECT name, salary FROM staff WHERE department = '技术部';")
tech_data = cursor.fetchall()
for row in tech_data:
    print(f"姓名：{row[0]}，薪资：{row[1]}")

# 4.3 范围查询：薪资大于6000的员工
print("\n===== 薪资大于6000的员工 =====")
cursor.execute("SELECT name, department, salary FROM staff WHERE salary > 6000;")
high_salary = cursor.fetchall()
for row in high_salary:
    print(row)

# ========== 5. 修改、删除数据（更新+删除） ==========
# 修改：将李四薪资调整为7500
cursor.execute("UPDATE staff SET salary = 7500 WHERE name = '李四';")
# 删除：删除行政部员工
cursor.execute("DELETE FROM staff WHERE department = '行政部';")
conn.commit()
print("\n数据更新、删除操作执行完成！")

# ========== 6. 数据库数据导出为Excel ==========
df = pd.read_sql("SELECT * FROM staff", conn)
df.to_excel("员工数据导出表.xlsx", index=False)
print("数据库数据已导出至：员工数据导出表.xlsx")

# ========== 7. 关闭连接 ==========
cursor.close()
conn.close()
print("\n数据库连接已关闭")