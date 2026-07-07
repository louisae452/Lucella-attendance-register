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

## Design

Since its conception, Lucella High School Attendance Regiter has been designed to be used in an office environment and as such, its design reflects the need for it to show information in a clear way, free of distractions and with easy navigation.

As such, navigation panels are clear on what they do, and unnecesary distractions have been kept away. It is possible to return to the main landing page from all pages.

Lucella High School is part of the Piggy Before The Infection Started. For this reason, the design has been kept consistent with the series trademark's colour scheme.

Fonts have been kept simple and professional.

## Access to the site.

Lucella High School Attendance Register is intended to be used only by registered users. It has two main type of users, parents of a student and staff members. Furthermore, users cannot register themselves as they require to be members of the organisation. On registration of a parent or teacher as a user by the Admissions Officer, they will be given the appropriate password.

On login onto the site, users will be redirected to one of two landing pages so that parents will never get access to the staff's side of the site, and staff will not get access to the parents' side of the site. Staff who are also parents would require two different login credentials.

On the staff's pages, three types of permissions have been given, teacher, Admissions Officer and Attendance officer. All users have teacher access, with the Admissions Officer and Attendance Officer having additional access to the funtionality referring to their roles.

## Features

On arriving to the home page, users are directed to log in.

PICTURE

Teachers are directed to the landing teacher page, which presents them with a menu of activities.

PICTURE

Student list shows a list of all the studnents. Only the Attendance Officer has access to this page.

PCITURE + REFUSED PICTURE

From that page, the attendance officer can email the appropriate parent.

PICTURES

Add parent button creates a parent user. On saving, it allows to enter the parent's additional information.

PCTURES X 3

The add student button adds a new student once their parent has been registered as a user.

PICTURES X2

The add teacher button allows the Admissions Officer to add a new teacher. On saving, a new page to enter additional data for the teacher opens.

PICTURES X 3S

The register button allows a teacher to input the session's details to get their register up.

NEED TO DO BOX BEFORE TAKING PICTURES.

Pending absences pulls out a list of all the pending absences so that the Attendance Officer can review them. Clicking on a student pulls out the record for the absence.

PICTURES X 3

Truanting students


Get my class allows the teacher to see the overal attendance of their students in a class, ass well as see the attendance record of an individual student.

PICTUE X 4

Once logged in, a parent is presented with a list of their children registered at the school.

PICTURE









## The logic

## Testing

## Deployment

## Languages used


## Fixed bugs.

Student_detail stopped working. Was fixed by reorganising the url order, ensuring that paths with a fixed name were first on the list and variable based ones were last.



## Frameworks, packages and libraries.

Git hub
Heroku

- Django 
- Gunicorn
- Witenoise

- To override the browser's default blue colour in dropdown menues: Choice.js
- To choose icons: [Font Awesome](https://fontawesome.com/).
- To convert image to webp: [ToWebP](https://towebp.io/)
- To convert logo to svg: [Kittl}(https://www.kittl.com/tools/svg-converter)]


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

## Media

## Acknoledgements