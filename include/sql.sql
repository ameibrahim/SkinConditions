-- TEACHER SIDE

-- count total courses
SELECT count(*)
FROM courses
WHERE creatorID = "?"

-- count total students
SELECT COUNT(*)
FROM courses
INNER JOIN subscriptions ON subscriptions.courseID = courses.id
WHERE courses.creatorID = "?"

-- count total exams
SELECT COUNT(*)
FROM courses
INNER JOIN exam ON exam.courseID = courses.id
WHERE creatorID = "ef87w9r42rbw"


-- STUDENT SIDE

-- count total course subscribed to
SELECT COUNT(*) as courses
FROM `subscriptions`
INNER JOIN courses ON courses.id = subscriptions.courseID
WHERE subscriptions.userID = 'ef87w9r42rbw' AND status = 'true'

-- .... something for checking if a course is coming within the 
-- next 7 days (NOT WORKING)
SELECT *
FROM schedules
WHERE DATE(LEFT(schedules.timeStart,10)) <= ( NOW() + INTERVAL 10 DAY)

-- counting exams that are available ... NOT WORKING
SELECT COUNT(*)
FROM exam
INNER JOIN subscriptions ON subscriptions.courseID = exam.courseID
INNER JOIN examGrades ON examGrades.userID = examGrades.userID
WHERE subscriptions.userID = "ef87w9r42rbw" AND examGrades.status != "Done"
GROUP BY exam.id

        SELECT *
        FROM exam
        INNER JOIN subscriptions ON subscriptions.courseID = exam.courseID
        WHERE subscriptions.userID = "ef87w9r42rbw"
