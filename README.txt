Before running program, install Google Client Library with:

pip install --upgrade google-api-python-client google-auth-httplib2 google-auth-oauthlib

*HOW TO GET CREDENTIALS*
1. Go to https://console.developers.google.com/
2. Go to library and search Google Calendar API. Enable the API.
3. Go to your dashboard to create a new project named Gradescope Scheduler.
4. Configure the OAuth consent screen by doing the following:
    Oauth Consent screen
    - App name: Gradescope Scheduler
    - User support email: your-email@gmail.com
    - Developer contact email: your-email@gmail.com

    Scopes
    - Click "Add or remove scopes"
    - Search for the first Google Calendar API and select it

    Test Users
    - Add your-email@gmail.com as a test User
5. Save the OAuth consent screen
6. Go to the credentials tab and select "Create credentials" and choose "OAuth Client ID"
7. Select Desktop App as the application type and name it Gradescope Scheduler
8. Create the credentials and download as a json file with the name "client_id.json"
9. Move file to working directory and run program
10. Running the program will open new window in your web browser, prompting you to choose a Google account for authorization
11. Click "Accept" and when authorization is complete, you can close the window and open your Google calendar.