import psycopg2
import sys
import click


@click.group()
@click.version_option("0.1.0")
def main():
    # CLI for control the last watched series
    pass


if __name__ == '__main__':
    args = sys.argv
    main()
