import sys
import click
import pandas as pd
import pathlib

PATH_TO_OUTPUT = "output/"
FILE_NAME = "out.csv"


@click.group()
@click.version_option("0.1.0")
def main():
    # CLI for control the last watched series
    pass


# Add new title to the list
@main.command()
@click.argument("name")
@click.argument("path")
def add(name, path):
    """
    Add new title to the list
    """
    # Create series
    s = create_correct_s(name, path)
    # Load the dataframe
    loaded_df = load_df()

    # Check is dataframe loaded successfully
    if isinstance(loaded_df, int):
        df = pd.DataFrame(s).T
    else:
        df = add_s_to_df(s, loaded_df)

    # Save the result data frame
    save_df(df)
    click.echo("Successfully added")


# Remove title from the list by id
@main.command()
@click.argument("title_id", type=click.INT)
def remove(title_id):
    """
    Remove title from list by id.
    id can be name of title or id.
    """

    # Load the dataframe
    loaded_df = load_df()
    # Check is dataframe loaded successfully
    if isinstance(loaded_df, int) or loaded_df.empty:
        click.echo("There are currently no any titles")
    else:
        # Check if this title is in the list
        if title_id in loaded_df.index:

            # Remove this title
            loaded_df = loaded_df.drop(index=title_id)

            # Save new dataframe
            save_df(loaded_df)

            # Print results
            click.echo("Successfully removed")
            if not loaded_df.empty:
                click.echo(loaded_df)
        else:
            # Print error
            click.echo("Can't find title with id = %d" % title_id)


# Print all titles, paths and series
@main.command()
def show():
    """
    Show all titles
    """
    # Load the dataframe
    loaded_df = load_df()
    # Check is dataframe loaded successfully
    if isinstance(loaded_df, int) or loaded_df.empty:
        click.echo("There are currently no any titles")
    else:
        click.echo(loaded_df.to_string())


# Create new series with name, path, and series columns
def create_correct_s(name, path):
    return pd.Series([name, path, 1], index=["name", "path", "series"])


# Add series to the existing dataframe
def add_s_to_df(s, df):
    df = pd.concat([df, s.to_frame().T], ignore_index=True)
    return df


# Load csv from PATH_TO_OUTPUT
# Return 0 if file not found
def load_df():
    try:
        return pd.read_csv(PATH_TO_OUTPUT + FILE_NAME,  index_col=0)
    except FileNotFoundError:
        return 0


# Save df dataframe to PATH_TO_OUTPUT path
def save_df(df):
    try:
        df.to_csv(PATH_TO_OUTPUT + FILE_NAME)
    except FileNotFoundError:
        pathlib.Path(PATH_TO_OUTPUT).mkdir(parents=True, exist_ok=True)
        df.to_csv(PATH_TO_OUTPUT + FILE_NAME)
        return 0


# Main method
if __name__ == '__main__':
    args = sys.argv
    main()
