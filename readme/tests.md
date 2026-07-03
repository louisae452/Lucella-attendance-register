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