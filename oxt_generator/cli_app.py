import typer
import oxt_generator

app = typer.Typer()

@app.command()
def new_oxt(path_to_wordfilelist: str, filename: str = "AE"):
    """ Generates a new `.oxt` file in the current working directory, from the wordlist file specified.
        The final file will have a filename: `en_US_{filename}.oxt
    """
    oxt_generator.create_oxt(wordfile=path_to_wordfilelist, filename=filename)