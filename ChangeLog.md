TODO List:
[TODO] Fully remove personal reflective posts
[TODO] Add Pseudo Identifiers to posts

v 0.6.4 07-Oct-2021
* Search is now limited to 24 hours and by the same author as the user
* Landing page is no longer empty - has daily tasks and links to key page features

v 0.6.3 07-Oct-2021
* Other users are now anonymous
* Anonymised names are fruits

v 0.6.2 07-Oct-2021
* Post detail page has unsave and unhide
* Removed add entry button on my saved and hidden posts page

v 0.6.1 07-Oct-2021
* Convention, id should be unique and not repeated. Changed id to name for save-btn
* Added edit and trash icons for post detail page to be like mood list icons

V 0.6.0 06-Oct-2021
* Navbar links are no longer accessible to unauthenticated users (except login/sign up)
* Renaming Question to Reflection
* Mood calendar is now only linked from Mood page
* Changed banner and background colour

v 0.5.7 05-Oct-2021
* Added user post history page
* Added feedback messages for save and hide buttons
* Added unsave button on saved posts in the feed
* Moved some navbar buttons into the user dropdown
* Save and hide buttons redirect to appriopriate places

v 0.5.6 05-Oct-2021
* New Entry button is split for gratitude and question post list pages
* Navbar highlighted correctly for page currently on

v 0.5.5 04-Oct-2021
* Fixed post ordering for hidden and saved posts

v 0.5.3 04-Oct-2021
* Further remove personal reflective posts, only remains in logic-statements now
* Success URL redirects to feed user was on for saving posts
* Added shortcut to saving posts from list pages
* Login required to view posts
* Fixed footer so that DJANGO_ENV displays properly now

v 0.5.2 03-Oct-2021
* Users can now save and hide posts (along with unsave and unhide)

v 0.5.1
* Made mood's reflection field mandatory
* Removed link to create new personal post
* Added landing page
* Personal posts cannot be created

v 0.5.0 01-Oct-2021
* Mood now has a daily reflection associated with it
* Fixed mood permission denied message error
* Split Log In and Sign Up links on Navbar when unauthenticated

v 0.4.9 29-Sep-2021
* Fixed mood deletion now displays success message
* Fixed post edit now displays success message
* Fixed users can no longer view other user's personal posts

v 0.4.8 27-Sep-2021
* Fixed admin can now bypass 24 hour filter 

v 0.4.7 27-Sep-2021
* Search only searches own posts

v 0.4.6 27-Sep-2021
* Public Post entry is limited 24 hours for public 
* Sign up validation for max length 150 characters

v 0.4.5 26-Sep-2021
* delete post only for only own posts
* delete mood, for only own mood

v 0.4.4 26-Sep-2021
* Add user feedback for editing and deleting posts and moods

v 0.4.3
* Validate mood on the same date,  using function instead class way to handle mood creation
* Enter new mood shall take input as date, default to today, good for testing. 
* Search now working

v0.4.2

* Reset DB (/reset) works (for testing, only in development and integration mode)
* When login failed error message is displayed

v0.4.1

* Guest unable view Personal posts
* Admin 'vibeadmin' (is_super_user) can edit any user's posts
* Admin (is_super_user) can view other's personal posts

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
