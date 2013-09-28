"""Facebook Friend/Unfriend Finder using the Graph API."""

import os
import sys
import facebook
import gflags

FLAGS = gflags.FLAGS

gflags.DEFINE_string(
    'api_token_file',
    '/Users/blanders/.fbtoken',
    'location of file containing Facebook API token')

gflags.DEFINE_string(
    'history_file',
    '/Users/blanders/.unfriender',
    'location of file for storing history')


def main(argv):
    """Main entry point for the application."""
    try:
        argv = FLAGS(argv)  # parse flags
    except gflags.FlagsError, err:
        print '%s\\nUsage: %s ARGS\\n%s' % (err, sys.argv[0], FLAGS)
        sys.exit(1)

    with open(FLAGS.api_token_file) as tf:
        token = tf.read().strip()

    old_friends = set()
    if os.path.exists(FLAGS.history_file):
        with open(FLAGS.history_file) as hf:
            for line in hf:
                old_friends.add(line.strip())

    fb = facebook.GraphAPI(token)
    friends = fb.get_connections('me', 'friends')

    new_friends = set()
    with open(FLAGS.history_file, 'w') as hf:
        for friend in sorted(friends['data'], key=lambda x: x['name']):
            new_friends.add(friend['name'])
            if friend['name'] not in old_friends:
                print 'NEW: %s' % friend['name']
            hf.write('%s\n' % friend['name'])

    for friend in old_friends:
        if friend not in new_friends:
            print 'UNFRIEND: %s' % friend


if __name__ == '__main__':
    main(sys.argv)
