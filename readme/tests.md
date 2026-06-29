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
