"""Facebook Friend/Unfriend Finder using the Graph API."""

import os
import sys
import facebook
import gflags

FLAGS = gflags.FLAGS

gflags.DEFINE_string(
    'history_file',
    '%s/.unfriender' % os.getenv('HOME'),
    'location of file for storing history')


def main(argv):
    """Main entry point for the application."""
    try:
        argv = FLAGS(argv)  # parse flags
    except gflags.FlagsError, err:
        print '%s\\nUsage: %s token\\n%s' % (err, sys.argv[0], FLAGS)
        sys.exit(1)

    if len(argv) != 2:
        print 'Usage: %s token\\n' % (sys.argv[0])

    old_friends = set()
    if os.path.exists(FLAGS.history_file):
        with open(FLAGS.history_file) as hf:
            for line in hf:
                old_friends.add(line.strip())

    fb = facebook.GraphAPI(argv[1])
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
