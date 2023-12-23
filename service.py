import os
import time
import argparse
import logging
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import boto3
import sys
from apscheduler.schedulers.background import BackgroundScheduler


def list_bucket():
    try:
        s3 = boto3.client('s3')
        response = s3.list_buckets()
        if response:
            print('Buckets exist..')
            for bucket in response['Buckets']:
                print(f'  {bucket["Name"]}')
    except Exception as e:
        logging.error(e)
        return False
    return True


def parse_arguments():
    parser = argparse.ArgumentParser(
        description='Automatic file synchronization from a local directory to AWS S3')
    parser.add_argument('-f', '--folder', required=True,
                        help='Path to the local folder to synchronize')
    parser.add_argument('-t', '--interval', type=int, default=60,
                        help='Synchronization interval (seconds)')
    parser.add_argument('-u', '--username', required=True,
                        help='AWS access key ID')
    parser.add_argument('-p', '--password', required=True,
                        help='AWS secret access key')
    parser.add_argument('-b', '--bucket', required=True,
                        help='S3 bucket name')
    parser.add_argument('--prefix', default='',
                        help='Prefix for keys on S3')
    return parser.parse_args()


class MyHandler(FileSystemEventHandler):
    def __init__(self, args):
        super().__init__()
        self.args = args
        self.s3 = boto3.client(
            's3', aws_access_key_id=args.username, aws_secret_access_key=args.password)
        
def synchronize_folder(args):
    try:
        command = [
            'aws',
            's3',
            'sync',
            args.folder,
            f's3://{args.bucket}/{args.prefix}',
            '--delete',
            '--exclude', '"*"',  # Exclude nothing, effectively syncing everything
            '--include', '"*"',  # Include everything
        ]
        os.system(' '.join(command))
    except Exception as e:
        logging.error(e)


def main():
    try:
        args = parse_arguments()
        logging.basicConfig(level=logging.INFO)
        event_handler = MyHandler(args)
        observer = Observer()
        observer.schedule(event_handler, path=args.folder, recursive=True)
        observer.start()

        # Setup periodic scheduler
        scheduler = BackgroundScheduler()
        scheduler.add_job(synchronize_folder, 'interval',
                          seconds=args.interval, args=[args])
        scheduler.start()

        while True:
            time.sleep(1)

    except KeyboardInterrupt:
        observer.stop()
        observer.join()


if __name__ == '__main__':
    try:
        main()
    except Exception as e:
        print(f'Error: {e}')
        sys.exit(1)
