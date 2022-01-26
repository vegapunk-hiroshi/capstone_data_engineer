class CreateTable():
    def __init__(self):
        self.staging = """
        CREATE IF NOT EXISTS staging_cleansed_logs(
            job_id int NOT NULL,
            project_id int NOT NULL,
            user_id int NOT NULL,
            ground_profile char(10),
            bt_clss_profile char(10),
            resolution char(5),
            noise_profile char(5),
            noise_type bool,
            remove_dup bool,
            airbone_laser bool,
            class_grdonly bool,
            nextcore bool,
            switch_xy bool,
            create_at timestamp,
            updated_at timestamp,
            upload_time timestamp,
            user_id int NOT NULL,
            email char(100),
            plan int
        )"""
        self.auto_classification_logs = """
        CREATE IF NOT EXISTS auto_classification_logs(
            job_id int NOT NULL,
            project_id int NOT NULL,
            user_id int NOT NULL,
            ground_profile char(10),
            bt_clss_profile char(10),
            resolution char(5),
            noise_profile char(5),
            noise_type bool,
            remove_dup bool,
            airbone_laser bool,
            class_grdonly bool,
            nextcore bool,
            switch_xy bool,
            create_at timestamp,
            duration timestamp
        )"""
        self.users = """
        CREATE IF NOT EXISTS users(
            user_id int NOT NULL,
            email char(100),
            plan char(20)
        )"""
        self.projects = """
        CREATE IF NOT EXISTS projects(
            project_id int NOT NULL,
            project_name char(50),
            date timestamp,
            summary varchar
        )"""
        self.time = """
        CREATE IF NOT EXISTS time(
            created_at timestamp NOT NULL,
            hour int,
            day int,
            week int,
            month int,
            year int,
            weekday int
        )"""
        
    def create_tables(self):
        return f'{self.staging} ¥n {self.auto_classification_logs} ¥n {self.users} ¥n {self.projects} ¥n {self.time} ¥n '
        