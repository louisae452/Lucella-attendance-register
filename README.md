# Lucella High School Attendance Register.

Have you ever been late for your 10:00 am meeting because you were dealing with a message from school asking where your child is, when you clearly communicated at 7:00 am that they were unwell and spending the day at home being looked after by their grandparents?

Have you received messages from disgrunted parents asking why you have not yet authorised their very justified child's absence?

Attendance is a masive subject in school and a system that allows clear and easy communication between partents and school is paramamount in order not to create resentment and animosity between them.

This project has been drawn out of my own experiences as a parent, Head of a school department and school governor.

Many school apps to communicate with parents such as Class Charts or Arbor rely on school sending information out to parents without expecting any feedback from them, with the result that parents have to use emails, text messages or phone recordings to report a school abscence. 

Those messages then have to be read and recorded on the appropriate way by a member of staff that will most likely be rushed by the normal issues concerning the start of the day in a busy school. Reading messages will be the last point on the to-do list while dealing with other more pressing matters.

This results on school systems sending automated messages to parents, parents not knowing if their message was received and general pandemonium.

Taking into account that keeping accurate records of which students are in school at all times is not only a legal matter, but also a safeguarding one, it is imperative that communication on attendance is run seamlesly between school and parents.

Lucella High School Attendance Register will provide an easy way for parents to access their child's register, log in abscences and their reason, and be able to see when the absence has been authorised.
School staff will be able to see when a student has been reported as absent by their parent, while the School's Attendance officer will be able to authorise or unauthorise absences. Parents will receive an automated message when their child's abscence has been unauthorised.


## Business goals.

- To create a single point of communication between parents and school on the matter of absences.
- To provide a way for parents to easily report an absence.
- To provide a way for teachers to easily see which students have been reported absent.
- To provide a way for the Attendance Officer to easily communicate whether an absence has been authorised.
- To enhance home-school relationships by seamlessly implementing the above.

## User needs.

### School staff needs.

- To be able to see which students have been reported as absent.
- To be able to  authorise absences.
- To be able to communicate unauthorised absences to parents.
- To be able to accurately report missing students to parents.

### Parents needs.

- To have a single point of communication to report an absence.
- To be able to see whether an absence has been authorised.
- To be able to see their child’s attendance record.
- To be quickly and accurately informed when their child is missing.
- To be informed when an absence has been unauthorised.

## User stories.
- As a user I want to be able to log onto the site so that I can see the appropriate pages.
- As an Admission's Officer I want to be able to see the list of all registered students so that if I click on one I can see their details.
- As an Admissions Officer I want to be able to register a student so that they are on the register.
- As an Admission's Officer I want to be able to deregister a studentgit  so that records are kept up to date.
- As a teacher I want to be able to see the list of students in my class so that I can mark them on the register.
- As a teacher I want to be able to see the class attendance over the year so that I can target students with low attendance.
- As a parent I want to be able to see my child's timetable so that they are prepared for the day ahead.
- As a parent I want to be able to see my child's attendance record so that I know if I am likely to get fined by school.
- As a parent I want to be able to record my child's absence so that it can be authorised by the school.
- As a parent I want to be informed when my child's absence has been unauthorised so that I can provide more information to get it authorised.
- As a parent I want to be informed when my child is missing from school so that I can find where they are.
- As an Attendance Officer I want to be able to see a record of all students' attendance so that I can target students with critical attendance.
- As an Attendance Officer I want to see all unclassified absences so that I can authorise/un-authorise them.

## Fixed bugs.

Student_detail stopped working. Was fixed by reorganising the url order, ensuring that paths with a fixed name were first on the list and variable based ones were last.



## Frameworks, packages and libraries.

Git hub
Heroku

- Django 
- Gunicorn

- To choose icons: [Font Awesome](https://fontawesome.com/).
- To convert image to webp: [ToWebP](https://towebp.io/)


- Django docs.
- Group permissions https://www.geeksforgeeks.org/python/python-user-groups-custom-permissions-django/
- To make models https://sentry.io/answers/difference-between-onetoonefield-and-foreign-key-django/
- To write listview as function https://www.geeksforgeeks.org/python/list-view-function-based-views-django/
- To check if user belongs to group. [Stack Overflow]( https://stackoverflow.com/questions/34571880/how-to-check-in-template-if-user-belongs-to-a-group) 
- To create custom tags. https://www.geeksforgeeks.org/python/how-to-create-custom-template-tags-in-django/
- To filter users by group. [StackOverflow](https://stackoverflow.com/questions/11118179/django-filter-users-by-group-in-a-model-foreign-key)
- Formsets [Geeksforgeeks]( https://www.geeksforgeeks.org/python/django-modelformsets/)
- To send emails [Geeksforgeeks](https://www.geeksforgeeks.org/python/setup-sending-email-in-django-project/)
- Annotate: (https://www.geeksforgeeks.org/python/aggregate-vs-annotate-in-django/)(https://www.geeksforgeeks.org/python/filter-objects-with-count-annotation-in-django/)
- Atomic transactions [Geeksforgeeks](https://www.geeksforgeeks.org/python/transaction-atomic-with-django/)