# Soundcloud-ID-Scraper
Minimalistic and simple tool for quickly grabbing user IDs of desired soundclouds.
-------------------------------------------------------------------------
Supports (and is recommended) using multiple accounts to avoid rate limit. The more IDs you need, the more accounts you should have to use. (Proxy support could also easily be implemented to further prevent limits (Not in current tool)).
Utilizes Souncloud OAuth tokens to make requests. 

OAuth tokens can be grabbed via http request capture software like fiddler, burpsuite, caido, etc. Alternatively, navigating to dev tools on a logged in soundcloud browser profile, and visiting the 'application tab' will show the OAuth code and its value.

auths.txt -> OAuth tokens
usernames.txt -> Soundcloud usernames that you wish to check IDs for
validsouncclouds.json -> stores results of IDs for users
