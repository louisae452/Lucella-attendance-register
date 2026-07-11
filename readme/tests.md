# Automated testing.
## Forms.
|Date|Form|Test|Result|Follow-up|
|:----|:----|:------|:------|:-------|
|27/06/2026|StudentForm|Form is valid when fields filled in correctly.|Pass|  |
|27/06/2026|StudentForm|Form is not valid when student_name is missing.|Pass| |
|27/06/2026|StudentForm|Form is not valid when student_surname is missing.|Pass|  |
|27/06/2026|StudentForm|Form is not valid when student_code is missing.|Pass|  |
|27/06/2026|StudentForm|Form is not valid when parent_name is not parent user.|Pass|  |
|27/06/2026|StudentForm|Form is not valid if date_of_birth format is not correct.|Pass|Add help text to form.|
|27/06/2026|StudentForm|Form is not valid if sex code is not correct.|Pass|  |
|27/06/2026|StudentForm|Form is not valid if group code is not correct.|Pass|  |
|27/06/2026|StudentForm|Form is not valid if music_option is not correct.|Pass|  |
|27/06/2026|UserForm|Form is validated if all fields are filled in.|Pass|  |
|27/06/2026|UserForm|Form is not validated if username is empty.|Pass|  |
|27/06/2026|UserForm|Form is not validated if first_name is empty.|Fail|Add required to  first_name in form. Add required to last_name and email in form.|
|27/06/2026|UserForm|Form is not validated if first_name is empty.|Pass|  |
|27/06/2026|UserForm|Form is not validated if last_name is empty.|Pass|  |
|27/06/2026|UserForm|Form is not validated if email is empty.|Pass|  |
|27/06/2026|UserForm|Form is not validated if password is empty.|Pass|  |
|27/06/2026|ParentForm|Form is valid if all fields filled correctly.|Pass|  |
|27/06/2026|ParentForm|Form is not valid if parent_name is not in parent group.|Pass|  |
|27/06/2026|ParentForm|Form is not valid if phone_number is empty.|Pass|  |
|27/06/2026|TeacherForm|Form is valid if all fields are filled correctly|Pass|  |
|27/06/2026|TeacherForm|Form is not valid if teacher_name is not user in teacher group|Pass|  |
|27/06/2026|TeacherForm|Form is not valid if phone_number is not correct|Pass|  |
|27/06/2026|GetregisterForm|Form is valid if all fields are filled correctly.|Pass|  |
|27/06/2026|GetregisterForm|Form is not valid if day option is not correct.|Pass|  |
|27/06/2026|GetregisterForm|Form is not valid if session option is not correct.|Pass|  |
|27/06/2026|GetregisterForm|Form is not valid if subject_name is not valid instance.|Pass|  |
|27/06/2026|RegisterForm|student_code is disabled on initialisation.|Pass|  |
|27/06/2026|RegisterForm|Form is valid if mark entered correctly.|Pass|  |
|27/06/2026|RegisterForm|Form is not valid if student_code is not initial value.|Pass|  |
|27/06/2026|RegisterForm|Form is not valid if mark option is not correct.|Pass|  |
|29/06/2026|SendemailForm|Form is valid if data entered correctly.|Pass|  |
|29/06/2026|SendemailForm|Form is not valid if subject option is not correct.|Pass|  |
|29/06/2026|AbsenceForm|Form is valid if data entered correctly.|Pass|  |
|29/06/2026|AbsenceForm|Form is not valid if date is not entered in the correct format.|Pass|Add help text to date.|
|29/06/2026|AbsenceForm|Form is not valid if reason_for_absence is empty.|Fail|Add required to reason_for_absence in form.|
|29/06/2026|AbsenceForm|Form is not valid if reason_for_absence is empty.|Pass|  |
|29/06/2026|GivereasonForm|Form is valid if filled in correctly.|Pass|  |
|29/06/2026|GivereasonForm|Form is not validated if an instance is not provided.|Fail|Force form to require a saved instance.|
|29/06/2026|GivereasonForm|Form is not validated if an instance is not provided.|Pass|  |
|29/06/2026|GivereasonForm|Form is not validated if reason_for_absence is empty.|Fail|Add required to reason_for_absence in form.|
|29/06/2026|GivereasonForm|Form is not validated if reason_for_absence is empty.|Pass|  |
|29/06/2026|PendingabsenceForm|Form is valid if form is filled correctly.|Pass|  |
|29/06/2026|PendingabsenceForm|Form is not valid if an instance is not provided.|Fail|Force form to require a saved instance.|
|29/06/2026|PendingabsenceForm|Form is not valid if an instance is not provided.|Pass|  |
|29/06/2026|PendingabsenceForm| Form is not valid if status option is not correct.|Pass|  |
|29/06/2026|PendingabsenceForm|Form is not valid if code option is not correct.|Pass|  |
|29/06/2026|GetclassForm|Form is valid when a valid instance is selected.|Pass|  |
|29/06/2026|GetclassForm|Form is not valid when an invalid instance is selected.|Pass|  |
|29/06/2026|RemoveForm|Queryset excludes deregistered students.|Pass|  |
|29/06/2026|RemoveForm|Form is valid when a registered student is selected.|Pass|  |
|29/06/2026|RemoveForm|Form is not valid when a deregistered student is selected.|Pass|  |

## Views

|Date|View|Test|Result|Follow-up|
|:----|:----|:------|:------|:-------|
|30/06/2026|HomeView|homeview loads successfully|Pass||
|30/06/2026|landing_router|Teacher is redirected to teachers' page|Fail|Use method decorator o request user login in landingview|
|30/06/2026|landing_router|Teacher is redirected to teacher's page|Pass| |
|30/06/2026|landing_router|Parent is redirected to parent's page|Pass| |
|30/06/2026|landing_router|Wrong user gets redirected home|Pass| |
|30/06/2026|LandingView|Non user is redirected|Pass| |
|30/06/2026|LandingView|Teacher user gets access to teacher's page|Pass| |
|30/06/2026|children_lsit|Non user cannot access parent's page|Pass| |
|30/06/2026|children_lsit|Parent user gets access and only registered children belonging to parent appear on list|Pass| |
|30/06/2026|students_list|Non user is redirected|Pass| |
|30/06/2026|students_list|Teacher user gets access and only registered children appear on list|Pass| |
|01/07/2026|add_parent|Non user is rejected|Pass| |
|01/07/2026|add_parent|Non admissions_officer user is rejected|Pass| |
|01/07/2026|add_parent|Admissions_officer user gets access to page.|Pass| |
|01/07/2026|add_parent|Form is submitted successfully|Pass| |
|01/07/2026|add_parentdata|Non user is rejected|Pass| |
|01/07/2026|add_parentdata|Non admissions_officer user is rejected|Pass| |
|01/07/2026|add_parentdata|Admissions_officer user gets access to page|Pass| |
|01/07/2026|add_parentdata|Form is submitted successfullty|Pass| |
|01/07/2026|add_student|Non user is rejected|Pass| |
|01/07/2026|add_student|Non admissions_officer user is rejected|Pass| |
|01/07/2026|add_student|Admissions_officer gets access to page|Pass| |
|01/07/2026|add_student|Form is submitted successfully|Pass| |
|01/07/2026|add_teacher|Non user is rejected| Pass| |
|01/07/2026|add_teacher|Non admissions_officer user is rejected|Pass| |
|01/07/2026|add_teacher|Admissions_officer gets access to page|Pass| |
|01/07/2026|add_teacher|Form is submitted successfully|Pass| |
|01/07/2026|add_teacherdata|Non user is rejected|Pass| |
|01/07/2026|add_teacherdata|Non admissions_officer user is rejected|Pass| |
|01/07/2026|add_teacherdata|Admissions_officer gets access to page|Pass| |
|01/07/2026|add_teacherdata|Form is submitted correctly|Pass| |
|01/07/2026|get_register|Non user is rejected|Pass| |
|01/07/2026|get_register|Non teacher user is rejected|Pass| |
|01/07/2026|get_register|Teacher user gets access to page|Pass|Do manual tests to check form is submitted correctly|
|02/07/2026|saveregister|Non user is rejected|Pass| |
|02/07/2026|saveregister|Non teacher user is rejected|Pass|Do manual tests to check teacher user gets access and form is submitted correctly |
|02/07/2026|student_detail|Non user is rejected|Pass| |
|02/07/2026|student_detail|Non attendance_officer user is rejected|Pass| |
|02/07/2026|student_detail|Attendance_officer gets access to page|Pass| |
|02/07/2026|sendemail|Non user is rejected|Pass| |
|02/07/2026|sendemail|Non attendance_officer user is rejected|Pass| |
|02/07/2026|sendemail|Attendance_officer gets access to page|Pass|Do manual tests to check email is sent correctly|
|02/07/2026|givereason|Non user is rejected|Pass| |
|02/07/2026|givereason|Non parent user is rejected|Pass| |
|02/07/2026|givereason|Parent user gets access to page|Pass|Do manual tests to check form is submitted correctly|
|02/06/2026|child_timetable|Non user is rejected|Pass| |
|02/07/2026|child_timetable|Non parent user is rejected|Pass |Do manual tests to check parent user gets access and timetable is displayed correctly|
|02/07/2026|report_absence|Non user is rejected|Pass| |
|02/07/2026|report_absence|Non parent user is rejected|Pass|Do manual tests to check parent user gets access and form is submitted correctly|
|02/07/2026|child_record|Non user is rejected|Pass| |
|02/07/2026|child_record|Non parent user is rejected|Pass|Do manual tests to check parent user gets access|
|02/07/2026|pending_absences|Non user is rejected|Pass| |
|02/07/2026|pending_absences|Non admissions_officer user is rejected|Pass| |
|02/-7/2026|pending_absences|Admissions_officer gets access to page|Pass|Do manual tests to check links redirect to correct page|
|02/07/2026|absence_detail|Non user is rejected|Pass| |
|02/07/2026|absene_detail|Non attendance_officer user is rejected|Pass|Do manual tests to check attendance_officer user gets access to page, form is submitted correctly and email is sent if appropriate|
|02/07/2026|get_class|Non user is rejected|Pass| |
|02/07/2026|get_class|Non teacher user is rejected|Pass| |
|02/07/2026|get_class|Teacher user gets access to page|Pass|Do manual tests to check llinks redirect to correct page|
|02/07/2026|class_detail|Non user is rejected|Pass| |
|02/07/2026|class_detail|Non teacher user is rejected|Pass| |
|02/07/2026|class_detail|Teacher user gets access to page|Pass| |
|02/07/2026|truanting_list|Non User is rejected|Pass| |
|02/07/2026|truanting_list|Non attendance_user is rejected|Pass| |
|02/07/2026|truanting_list|Attendance_officer gets access to page|Pass|Do manual tests to check emails are sent correctly|
|02/07/2026|remove_student|Non user is rejected|Pass| |
|02/07/2026|remove_student|Non admissions_officer is rejected|Pass| |
|02/07/2026|remove_student|Admissions_officer get access to page|Pass|Do manual tests to check form is submitted correctly|


# Manual testing

|10/07/2026| pending absence detail.  form crashes when the dropbox is filled with ---- Eliminate that forom dropbox menu. (eliminate blank=True from model)| Form can only be filled with a proper choice.

## Security

|Date|Test|Method|Expected result|Result|Follow up|
|:--|:--|:--|:--|:--|:--|
|10/07/2026|User is logged off when browser is closed|Open browser. Navigate to app. Log in. Close browser. Open it again. Navigate to app.|Should be logged off|Pass|--|
|10/07/2026|Landing page not accessible for non users|In browser, type landing page address on address bar|Home page loads|Pass|--|
|10/07/2026|Student page not accessible for non users|In browser, type student page address on address bar|Blank page with 'Main menu' button appears. 'Main menu' button leads to home page|Pass--|
|10/07/2026|Individual student page not accessible for non users|In browser, type individual existing student page.|430.html appears. 'Main menu' button leads to home page|Pass|--|
|10/07/2026|Newparent page not accessible to non user|In browser, type newparent page address on address bar|403.html appears.'Main menu' button leads to home page|Pass|--|
|10/07/2026|Newstudent page not accessible to non user|In browser, type newstudent page address on address bar|403.hml appears. 'Main menu'button leads to home page|Pass|--|
|10/07/2026|Remove page not accessible for non users|In browser, type remove page address on address bar|403.html appears. 'Main menu' button leads to home page|Pass|--|
|10/07/2026|Newteacher page not accessible for non users|In browsesr, type newteacher page address on address bar|403.html appears. 'Main menu' button leads to home page|Pass|--|
|10/07/2026|Getregister page not accessible for non users|In browser, type getregister page address on address bar|403.html appears. 'Main menu' button leads to home page|Pass|--|



Further security tests can be seen in automated tests.



## Home page
|Date|Test|Method|Expected result|Result|Follow up|
|:--|:--|:--|:--|:--|:--|
|10/07/2026|Navigates to log in page|Open app. Click on 'log in' button|Log in page appears|Pass|--|
|10/07/2026|Email link directs to email program|Open app. Click on email link on footer|Email program opens. New email opens. School address is on address bar|Pass|--|


## Login page
|Date|Test|Method|Expected result|Result|Follow up|
|:--|:--|:--|:--|:--|:--|
|10/07/2026|Correct sign in|In login page, enter existing teacher Username and password|Teacher landing page opens|Pass|--|
|10/07/2026|Correct sign in|In login page, enter existing parent Username and password|Parent landing page opens|Pass|--|
|10/07/2026|Correct sign in |In login page, enter existing Username and incorrect password|Page resets|Pass|--|
|10/07/2026|Correct sign in|In login page, enter incorrect Username and password|Page resets|Pass|--|

## Teacher landing page.
|Date|Test|Method|Expected result|Result|Follow up|
|:--|:--|:--|:--|:--|:--|
|10/07/2026|Not accessible for non users|In browser, type page address on address bar|Home page loads|Pass|--|
|10/07/2026|Success log in message|Sign in with teacher credentials|Teacher landing appears. Successfully signed in message appears|Pass|--|
|10/07/2026|'Student' list button directs to student page|Click on student list button|Student page appears|Pass|--|
|10/07/2026|Individual student is blocked|On student page, click on any student|403.html page appears|Pass|--|
|10/07/2026|'Main menu' button on individual student page redirects to correct landing page|From individual student 403 page, click on 'Main menu' button|Redirects to teacher landing page|Pass|--|
|10/07/2026|'Add parent' button|On teacher landing, click on 'Add parent' button. 'Main menu' button leads back to teacher landing|403.html appears|Pass|--|
|10/07/2026|'Add student' button|On teacher landing, click on 'Add student' button|403.html appears. 'Main menu'button leads back to teacher landing|Pass|--|
|10/07/2026|'Remove student' button|On teacher landing, click on 'Remove student'button|430.html appears. 'Main menu' button leads back to teacher landing|Pass|--|
|10/07/2026|'Add teacher' button|On teacher landing, click on 'Add teacher' button|403.html appears. 'Main menu' button leads to teacher landing page|Pass|--|
|10/07/2026|Register page loads for teacher user|On teacher landing, clik on 'Register' button|Getregister page appears|Pass|--|


# User experience.

The following issues were reported by users.

|Date|Issue|Template|View|Action taken|
|:--|:--|:--|:--|:--|
|10/07/2026|'Home' button in parents pages is misleading|child_record.html, child_timetable.html, give_reason.html, report_absence.html|--|The text in the button was changed to 'Main menu'|
|10/07/2026|There is no way to get out of givereason page unless saving|give_reason.html|--|'Back to absence record' and 'Main menu' buttons were added|
|10/07/2026|In the reportabsence page, when the date does not match the session, after attempting to save, the user is redirected to the timetable page|report_absence.html|report_absence|The redirect was changed to go back to the reportabsence page|
