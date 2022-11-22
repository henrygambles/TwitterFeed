# Twitter Feed

Simple command line interface for Twitter using the [twint]("https://github.com/twintproject/twint") library. This isn't designed to be a client which supports logging in - but allows you to fetch, search & sort tweets for any given user, or a list of users.

The main advantage of twint is being able to query Twitter without any rate limitations an fetch large amounts of data quickly. I use this script to follow people/topics I find interesting - as the defualt Twitter feed tends to be clogged up with suggested posts - or only show those which are already popular.

(Warning - this code is 🗑 - I don't write code like this for work 😄)

### Example Usage

```
❱  t --help
usage: twitter.py [-h] [-s [SINCE]] [-u [USER]] [-m [MAX]] [-t [TOP]] [-w] [-b] [-c] [-l] [-r] [search]

Twitter Search

positional arguments:
  search                What you'd like to search

options:
  -h, --help            show this help message and exit
  -s [SINCE], --since [SINCE]
                        The date from which to search
  -u [USER], --user [USER]
                        A user's tweets you'd like to display
  -m [MAX], --max [MAX]
                        How many tweets you'd like to fetch
  -t [TOP], --top [TOP]
                        How many tweets you'd like to print
  -w, --who             Who's who? (Displays profiles of users being followed)
  -b, --backwards       Reverse order of tweets
  -c, --conversation    See replies
  -l, --likes           Sort by most liked
  -r, --retweets        Sort by most retweeted
```

![twitter-demo](https://user-images.githubusercontent.com/47319147/202789433-1a204f2c-2e6a-4c58-ace1-32f3d0dccffc.gif)
