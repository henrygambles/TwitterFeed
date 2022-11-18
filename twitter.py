from term_image.image import from_url
import re, twint, argparse, asyncio, nest_asyncio

users = [ # 👇 Users you wish to follow
        'ringostarrmusic',
        'georgeharrison',
        'paulmccartney',
        'johnlenmon',
         ]

nest_asyncio.apply()

parser = argparse.ArgumentParser(description="Twitter Search")
parser.add_argument('search', help="What you'd like to search", nargs='?')
parser.add_argument('-s', '--since', help="The date from which to search", nargs='?')
parser.add_argument('-u', '--user', help="A user's tweets you'd like to display", nargs='?')
parser.add_argument('-m', '--max', help="How many tweets you'd like to fetch", nargs='?')
parser.add_argument('-t', '--top', help="How many tweets you'd like to print", nargs='?')
parser.add_argument('-w', '--who', help="Who's who? (Displays profiles of users being followed)", action='store_true')
parser.add_argument('-b', '--backwards', help="Reverse order of tweets", action='store_true')
parser.add_argument('-c', '--conversation', help="See replies", action='store_true')
parser.add_argument('-l', '--likes', help="Sort by most liked", action='store_true')
parser.add_argument('-r', '--retweets', help="Sort by most retweeted", action='store_true')
args = parser.parse_args()

config = twint.Config(Username = args.user, Limit = args.max, Hide_output = True, Store_object = True, Since = args.since)
if args.search: config.Search = args.search

async def search(user, profile_lookup = False):
    c = twint.Config(Username = user, Limit = args.max, Hide_output = True, Store_object = True, Since = args.since)
    if args.search: c.Search = args.search
    twint.run.Lookup(c) if profile_lookup else twint.run.Search(c)
    print(f"@{user} ✅")

async def main():
    if args.user == 'all':
        print("🐣 Gathering tweets...\n")
        await asyncio.gather(*(search(user) for user in users))
    if args.who:
        print("🙆‍♂️ Fetching profiles...\n")
        await asyncio.gather(*(search(user, True) for user in users))
        user_list = sorted(twint.output.users_list, key=lambda x: x.followers, reverse = args.backwards)
        for user in user_list:
            print(from_url(user.avatar, scale = (0.1, 0.1)))
            print(f"\n{user.name} (@{user.username}) %s\nJoined {user.join_date}\nFollowers:{user.followers} | Following:{user.following}\n{user.bio}\n" %("✅" if user.is_verified else ""))
    else:
        twint.run.Search(config)

asyncio.run(main())

tweets = twint.output.tweets_list
print(f"\nFound {len(twint.output.tweets_list)} tweets.\n")
if args.likes: tweets.sort(key=lambda x: x.likes_count, reverse = args.backwards)
elif args.retweets: tweets.sort(key=lambda x: x.retweets_count, reverse = args.backwards)
else: tweets.sort(key=lambda x: x.datetime, reverse = args.backwards)
if args.top: tweets = tweets[:int(args.top)] if args.backwards else tweets[-int(args.top):]

for tweet in tweets:
    if args.conversation and tweet.quote_url:
        print(f"@{tweet.username} replying to @{tweet.quote_url.split('?')[0].split('/')[3]}")
        print("Fetching original tweet...")
        con = twint.Config(Hide_output = True, Store_object = True, Username = tweet.quote_url.split('?')[0].split('/')[3])
        twint.run.Search(con)
        t = next(x for x in twint.output.tweets_list if str(x.id) == str(tweet.quote_url[-19:]))
        tweet.quote_url = None; tweets.insert(0, tweet); tweet = t
    print(f"{tweet.name} - @{tweet.username} | {tweet.datestamp} {tweet.timestamp}")
    if tweet.urls: tweet.tweet = re.sub(r'http\S+', ', '.join(tweet.urls), tweet.tweet)
    print(tweet.tweet)
    if tweet.thumbnail: print(from_url(tweet.thumbnail, scale = (0.25, 0.25)))
    print(f"❤️  {tweet.likes_count} 🔁 {tweet.retweets_count}", tweet.link, "\n")