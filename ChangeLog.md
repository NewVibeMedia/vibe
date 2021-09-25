* [TODO] delete post only for only own posts
* [TODO] delete mood, for only own mood
* [TODO] validate mood on the same date

* [TODO] Login failed but without error message
* [TODO] Admin (is_super_user) can edit any user's posts
* [TODO] Sign up validation for max length 150 characters

v0.4 25-Sep-2021

* Run server in different mode (development,production) with different database, using DJANGO_ENV to control
* Add date_posted on edit Post form, but not saved yet
* Add date_posted on edit Mood form, but not saved yet
* Edit mood (with date field)
* After creating multiple posts, sign out, the login page displays multiple "Post created successfuly" alert messages
* Display post type in heading, such "My Question Posts"
* Delete post
* Post options (delete, edit) only show for posts created by user
* Delete mood


* v 0.3.1 24-Sep-2021
* Login required for calendar
* Reformat login page to be same as rails

v 0.3.0  24-Sep-2021
* Deployment with NGINX webserver on port 80
* Mood form adjusted
* HighCharts mood chart now displays under Calendar

v 0.2.2  24-Sep-2021
* Changed wording of navbar

v 0.2.1  24-Sep-2021
* Moved CSS files to public/static to be accessed globally

v 0.2  24-Sep-2021
* Login moved to NavBar
* Django message displays correctly
* Unauthenticated user gets redirected

v 0.1 23-Sep-2021

* Port from Ruby on Rails and React version
