class CreateTable():
    def __init__(self):
        self.staging = """
        DROP TABLE IF EXISTS staging_cleansed_logs;
        CREATE TABLE IF NOT EXISTS staging_cleansed_logs(
            job_id int NOT NULL,
            project_id int NOT NULL,
            project_name varchar(max),
            date varchar,
            summary varchar(max),
            ground_profile char(20),
            bt_clss_profile char(20),
            resolution char(5),
            noise_profile char(5),
            noise_type char(20),
            remove_dup int,
            airbone_laser int,
            ground_grndonly	int,
            class_grdonly int,
            nextcore int,
            switch_xy int,
            created_at datetime,
            updated_at datetime,
            upload_time char(20),
            user_id int NOT NULL,
            email_encrypted char(150),
            plan_id int
        );"""
        self.auto_classification_logs = """
        DROP TABLE IF EXISTS auto_classification_logs;
        CREATE TABLE IF NOT EXISTS auto_classification_logs(
            job_id int NOT NULL,
            project_id int NOT NULL,
            user_id int NOT NULL,
            ground_profile char(10),
            bt_clss_profile char(10),
            resolution char(5),
            noise_profile char(5),
            noise_type char(20),
            remove_dup int,
            airbone_laser int,
            class_grdonly int,
            nextcore int,
            switch_xy int,
            created_at datetime,
            upload_time char(30)
        );"""
        self.users = """
        DROP TABLE IF EXISTS users;
        CREATE TABLE IF NOT EXISTS users(
            user_id int NOT NULL,
            email_encrypted char(150),
            plan_id char(20)
        );"""
        self.projects = """
        DROP TABLE IF EXISTS projects;
        CREATE TABLE IF NOT EXISTS projects(
            project_id int NOT NULL,
            project_name varchar(max),
            date varchar,
            summary varchar(max)
        );"""
        self.time = """
        DROP TABLE IF EXISTS time;
        CREATE TABLE IF NOT EXISTS time(
            created_at timestamp NOT NULL,
            hour int,
            day int,
            week int,
            month int,
            year int,
            weekday int
        );"""
        
    def create_tables(self):
        return f'{self.staging} {self.auto_classification_logs} {self.users} {self.projects} {self.time}'
        