-- These are MySQL queries to create a user and give hime privileges.
CREATE USER IF NOT EXISTS "strategize_main_dev"@"localhost" IDENTIFIED BY "strategize_main_pwd";
GRANT ALL ON strategize.* TO "strategize_main_dev"@"localhost";
