import argparse
import json 
import os
import docker

# TODO THE TODOLIST
# TODO Notifier
# parser = argparse.ArgumentParser(description='Process some integers.')
# parser.add_argument('integers', metavar='N', type=int, nargs='+',
#                     help='an integer for the accumulator')
# parser.add_argument('--sum', dest='accumulate', action='store_const',
#                     const=sum, default=max,
#                     help='sum the integers (default: find the max)')

# args = parser.parse_args()
# print(args.accumulate(args.integers))


def cli():
    parser = argparse.ArgumentParser()
    parser.add_argument("tz", help="The timezone")
    parser.add_argument(
        "-r",
        "--repeat",
        help="number of times to repeat the greeting",
        default=1,
        type=int,
    )
    parser.add_argument(
        "-i",
        "--interval",
        help="time in seconds between iterations",
        default=3,
        type=int,
    )
    args = parser.parse_args()
    
    # greet(args.tz, args.repeat, args.interval)
    
    print(os.getenv('topic'))
    
    
    ### Docker info and cli
    try:
        client = docker.from_env()
        for image in client.images.list():
            print(image.id)
    except:
        print("An exception occurred")
    
    username = input("Enter username:")
    print("Username is: " + username)
    