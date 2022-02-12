class SqlQueries:
    
    autoclassifcation_logs_table_insert = ("""
        SELECT
            job_id,
            project_id,
            user_id,
            ground_profile,
            bt_clss_profile,
            resolution,
            noise_profile,
            noise_type,
            remove_dup,
            airbone_laser,
            class_grdonly,
            nextcore,
            switch_xy,
            created_at,
            upload_time
        FROM staging_cleansed_logs;
    """)

    users_table_insert = ("""
        SELECT DISTINCT 
            user_id, 
            email_encrypted, 
            plan_id
        FROM staging_cleansed_logs;
    """)

    projects_table_insert = ("""
        SELECT DISTINCT 
            project_id,
            project_name,
            date,
            summary
        FROM staging_cleansed_logs;
    """)

    time_table_insert = ("""
        SELECT created_at, extract(hour from created_at), extract(day from created_at), extract(week from created_at), 
               extract(month from created_at), extract(year from created_at), extract(dayofweek from created_at)
        FROM staging_cleansed_logs;
    """)


