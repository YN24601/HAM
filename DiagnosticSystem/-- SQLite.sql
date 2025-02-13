-- -- SQLite
-- DROP TABLE user_user;
-- DROP TABLE django_migrations;
-- DROP TABLE django_content_type;

-- SELECT * FROM user_doctor;

SELECT * FROM user_patient;
-- 修改所有用户头像
UPDATE user_patient SET avatar = 'avatars/patients/default_patient.jpg' WHERE id > 0;



